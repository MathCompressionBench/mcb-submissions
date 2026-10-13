#!/usr/bin/env python3
# ABOUTME: Checks a submission branch before you open a pull request: the same rules the organizers apply (added files
# ABOUTME: only, sizes, bundle hash = ID, metadata, metadata.yaml, an accepted task package). Needs only Python 3 and git.
from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
import sys
import tarfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import submission_meta as sm  # noqa: E402  (a copy of lcbench's src/lcbench/submission_meta.py)

SUBMISSION_PATH = re.compile(r"submissions/([a-z0-9][a-z0-9_.-]*)/([0-9a-f]{64})(\.tar\.gz|\.receipt\.json|\.json)")
MAX_BUNDLE_BYTES = 256 << 20
MAX_METADATA_BYTES = 1 << 20
MAX_SUBMISSIONS = 5
META_SCHEMA = "lcbench.intake_submission.v1"
PRIMARY = "expr_nodes_with_levels_v1"
ACCEPTED_FILE = "accepted-packages.json"


def git(repo: Path, *args: str) -> bytes:
    out = subprocess.run(["git", "-C", str(repo), *args], capture_output=True)
    if out.returncode != 0:
        raise SystemExit(f"git {' '.join(args)}: {out.stderr.decode(errors='replace').strip()}")
    return out.stdout


def changes(repo: Path, base: str) -> list[dict]:
    """Files the branch changes compared with where it left the base branch (what the pull request will contain)."""
    merge_base = git(repo, "merge-base", base, "HEAD").decode().strip()
    raw = git(repo, "diff-tree", "-r", "-z", "--no-renames", "--raw", merge_base, "HEAD").split(b"\0")
    out = []
    i = 0
    while i + 1 < len(raw) and raw[i]:
        meta = raw[i].decode().lstrip(":").split()
        blob, status = meta[3], meta[4]
        size = int(git(repo, "cat-file", "-s", blob)) if status != "D" else 0
        out.append({"path": raw[i + 1].decode(errors="replace"), "status": status, "mode": meta[1], "blob": blob,
                    "size": size})
        i += 2
    return out


def blob_sha256(repo: Path, blob: str) -> str:
    h = hashlib.sha256()
    with subprocess.Popen(["git", "-C", str(repo), "cat-file", "blob", blob], stdout=subprocess.PIPE) as p:
        for chunk in iter(lambda: p.stdout.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def accepted_file(repo: Path, base: str) -> dict | None:
    """accepted-packages.json on the base branch (not from your own checkout); None when the base branch has none."""
    out = subprocess.run(["git", "-C", str(repo), "show", f"{base}:{ACCEPTED_FILE}"], capture_output=True)
    return json.loads(out.stdout) if out.returncode == 0 else None


def accepted_packages(repo: Path, base: str) -> dict | None:
    """{task: [{package_sha256, task_sha256, get}]} from the base branch's accepted-packages.json, or None."""
    data = accepted_file(repo, base)
    return None if data is None else data["tasks"]


def bundle_submission(bundle: bytes) -> dict | None:
    """The bundle's submission/SUBMISSION.json, read without extracting anything; None when it has none."""
    try:
        with tarfile.open(fileobj=io.BytesIO(bundle), mode="r:gz") as tar:
            member = tar.getmember("submission/SUBMISSION.json")
            if not member.isfile() or member.size > MAX_METADATA_BYTES:
                return None
            value = json.loads(tar.extractfile(member).read())
    except (tarfile.TarError, KeyError, OSError, EOFError, ValueError, AttributeError):
        return None
    return value if isinstance(value, dict) else None


def bundle_task_sha256(bundle: bytes) -> str | None:
    """The task sha256 in the bundle's submission/SUBMISSION.json."""
    value = (bundle_submission(bundle) or {}).get("task_sha256")
    return value if isinstance(value, str) else None


def bundle_run(bundle: bytes) -> tuple:
    """(track, budget_seconds) of the run the bundle records (SUBMISSION.json metadata.track and metadata.run)."""
    meta = (bundle_submission(bundle) or {}).get("metadata")
    meta = meta if isinstance(meta, dict) else {}
    run = meta.get("run") if isinstance(meta.get("run"), dict) else {}
    return meta.get("track"), run.get("budget_seconds")


def entry_shape(found: list[dict]) -> tuple[dict | None, list[dict], list[str]]:
    """One pull request is one submission: exactly one new entries/<entry>/metadata.yaml beside its bundles. Returns
    (that change with its entry name, the other changes, problems)."""
    entry, rest, problems = None, [], []
    for ch in found:
        path = ch["path"]
        if not path.startswith("entries/"):
            rest.append(ch)
            continue
        m = sm.ENTRY_PATH.fullmatch(path)
        if not m:
            problems.append(f"{path}: under entries/ only entries/<entry>/metadata.yaml may be added (<entry>: "
                            f"lowercase letters, digits, '.', '_' or '-', at most 64)")
        elif ch["status"] != "A":
            problems.append(f"{path}: files may only be added, not changed or deleted; a new submission takes a new "
                            f"entry name")
        elif ch["mode"] != "100644":
            problems.append(f"{path}: must be a regular non-executable file (git mode {ch['mode']})")
        elif ch["size"] > sm.MAX_METADATA_YAML_BYTES:
            problems.append(f"{path}: {ch['size']} bytes, more than the limit of {sm.MAX_METADATA_YAML_BYTES} bytes")
        elif entry is not None:
            problems.append(f"{path}: one pull request is one submission, with one metadata.yaml (it also adds "
                            f"{entry['path']})")
        else:
            entry = dict(ch, name=m.group(1))
    if entry is None and not problems:
        problems.append("the branch adds no entries/<entry>/metadata.yaml: every submission needs one (copy "
                        "templates/metadata.yaml and fill it in)")
    return entry, rest, problems


def package_problem(sid: str, task: str, task_sha: str | None, packages: list[dict],
                    retired: list[dict] | None = None) -> str | None:
    if task_sha is not None and task_sha in {p["task_sha256"] for p in packages}:
        return None
    old = next((r for r in retired or [] if r.get("task_sha256") == task_sha), None)
    listed = "; ".join(f"package sha256 {p['package_sha256']} (task sha256 {p['task_sha256']}"
                       + (f", get it with: {p['get']}" if p.get("get") else "") + ")" for p in packages)
    if old is not None:
        what = (f"the bundle was made from the {task} package {old.get('name') or task_sha}, which the organizers "
                f"have retired; it is replaced by {old.get('replaced_by', 'the package below')}")
    elif task_sha is None:
        what = "the bundle has no readable submission/SUBMISSION.json (use the file ./submit wrote)"
    else:
        what = (f"the bundle was made from a {task} package the organizers do not accept (task sha256 {task_sha}, "
                f"as ./check prints it)")
    return (f"{sid}: {what}. Accepted {task} packages: {listed}. Start a new workspace from an accepted package, "
            f"copy your proof files into it and run ./submit again")


def metadata_problems(meta, task: str, sid: str) -> list[str]:
    if not isinstance(meta, dict):
        return ["the metadata file is not a JSON object"]
    problems = []
    if meta.get("schema") != META_SCHEMA:
        problems.append(f"metadata schema is {meta.get('schema')!r}, expected {META_SCHEMA!r}")
    if meta.get("task") != task:
        problems.append(f"metadata task {meta.get('task')!r} differs from the directory {task!r}")
    if meta.get("submission_id") != sid:
        problems.append("metadata submission_id differs from the file name")
    claimed = (meta.get("claimed") or {}).get(PRIMARY)
    if not isinstance(claimed, int) or isinstance(claimed, bool):
        problems.append(f"metadata claimed.{PRIMARY} must be an integer (the score you report)")
    if not isinstance(meta.get("participant"), str) or not meta["participant"]:
        problems.append("metadata participant must be a non-empty string (your name or team)")
    return problems


def check(repo: Path, base: str) -> list[str]:
    """Every reason the organizers would refuse a pull request from the current commit into `base`."""
    found = changes(repo, base)
    if not found:
        return [f"the branch adds no files compared with {base}"]
    listing = accepted_file(repo, base)
    accepted = None if listing is None else listing["tasks"]
    retired = {} if listing is None else listing.get("retired", {})
    pr_entry, found, problems = entry_shape(found)
    entry_meta = None
    if pr_entry is not None:
        entry_meta, found_problems = sm.loads(git(repo, "cat-file", "blob", pr_entry["blob"]),
                                              None if accepted is None else set(accepted))
        problems += [f"{pr_entry['path']}: {p}" for p in found_problems]
        if not found:
            problems.append("the branch adds no bundle beside its metadata.yaml")
    subs: dict = {}
    for ch in found:
        path = ch["path"]
        m = SUBMISSION_PATH.fullmatch(path)
        if not m:
            problems.append(f"{path}: only entries/<entry>/metadata.yaml and submissions/<task>/<64-hex id>.tar.gz, "
                            f".json and .receipt.json may be added")
            continue
        if ch["status"] != "A":
            problems.append(f"{path}: files may only be added, not changed or deleted")
            continue
        if ch["mode"] != "100644":
            problems.append(f"{path}: must be a regular non-executable file (git mode {ch['mode']})")
            continue
        task, sid, suffix = m.groups()
        if accepted is not None and task not in accepted:
            problems.append(f"{path}: the organizers do not accept the task {task!r} (open tasks: "
                            f"{', '.join(sorted(accepted))})")
            continue
        limit = MAX_BUNDLE_BYTES if suffix == ".tar.gz" else MAX_METADATA_BYTES
        if ch["size"] > limit:
            problems.append(f"{path}: {ch['size']} bytes, more than the limit of {limit} bytes")
            continue
        entry = subs.setdefault(sid, {"task": task, "files": {}})
        if entry["task"] != task:
            problems.append(f"{sid}: submitted under two tasks")
        entry["files"][suffix] = ch
    for sid, entry in sorted(subs.items()):
        files, task = entry["files"], entry["task"]
        for need, what in ((".tar.gz", "bundle"), (".json", "metadata")):
            if need not in files:
                problems.append(f"{sid}: the {what} file submissions/{task}/{sid}{need} is missing")
        if ".tar.gz" in files:
            got = blob_sha256(repo, files[".tar.gz"]["blob"])
            if got != sid:
                problems.append(f"{sid}: the bundle's sha256 {got} differs from its submission ID "
                                f"(the bundle was changed after ./submit, or the file name is wrong)")
            bundle = git(repo, "cat-file", "blob", files[".tar.gz"]["blob"])
            if accepted is not None:
                problem = package_problem(sid, task, bundle_task_sha256(bundle), accepted[task], retired.get(task))
                if problem:
                    problems.append(problem)
            if entry_meta is not None and entry_meta.get("track") in sm.TRACKS:
                problems += [f"{sid}: {p}" for p in sm.run_problems(entry_meta["track"], *bundle_run(bundle))]
        if entry_meta is not None and isinstance(entry_meta.get("tasks"), list) and task not in entry_meta["tasks"]:
            problems.append(f"{sid}: the task {task} is not in the tasks of {pr_entry['path']}")
        if ".json" in files:
            try:
                meta = json.loads(git(repo, "cat-file", "blob", files[".json"]["blob"]))
                problems += [f"{sid}: {p}" for p in metadata_problems(meta, task, sid)]
                if pr_entry is not None and isinstance(meta, dict) and meta.get("entry") != pr_entry["name"]:
                    problems.append(f"{sid}: metadata entry is {meta.get('entry')!r}; it must name this pull "
                                    f"request's entry {pr_entry['name']!r} (lcbench intake add ... --entry "
                                    f"{pr_entry['name']})")
            except ValueError as e:
                problems.append(f"{sid}: the metadata file is not JSON ({e})")
        if ".receipt.json" in files:
            try:
                receipt = json.loads(git(repo, "cat-file", "blob", files[".receipt.json"]["blob"]))
                if not isinstance(receipt, dict) or receipt.get("bundle_sha256") != sid:
                    problems.append(f"{sid}: the self-receipt is for another bundle")
            except ValueError as e:
                problems.append(f"{sid}: the self-receipt is not JSON ({e})")
    if len(subs) > MAX_SUBMISSIONS:
        problems.append(f"{len(subs)} submissions in one pull request; at most {MAX_SUBMISSIONS}")
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Check the current branch of a submissions checkout before you open "
                                             "a pull request. Only committed files are checked.")
    ap.add_argument("--base", default="origin/main", help="the branch the pull request goes into (default: "
                                                          "origin/main)")
    ap.add_argument("--repo", type=Path, default=Path("."), help="the submissions checkout (default: here)")
    args = ap.parse_args(argv)
    pending = git(args.repo, "status", "--porcelain", "--", "submissions", "entries").decode().strip()
    if pending:
        print("note: there are uncommitted files under submissions/ or entries/; only committed files are checked:")
        print(pending)
    problems = check(args.repo, args.base)
    if problems:
        print(f"NOT OK: the pull request would be refused ({len(problems)} problem(s)):")
        for p in problems:
            print(f"- {p}")
        return 1
    print("OK: the pull request has the right shape. Push the branch and open the pull request.")
    print("(The organizers then rebuild and re-score the bundle on their machines.)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
