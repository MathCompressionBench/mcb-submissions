# ABOUTME: Tests of scripts/check_submission.py on real git repositories: a well-formed submission branch passes, and
# ABOUTME: every rule the organizers apply (paths, add-only, modes, hashes, metadata, metadata.yaml, tracks) is enforced.
from __future__ import annotations

import gzip
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_submission.py"
spec = importlib.util.spec_from_file_location("check_submission", SCRIPT)
check_submission = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_submission)

TASK = "toyarith-warm"
TASK_SHA = "8bbd7fdc" + "0" * 56
OTHER_TASK_SHA = "7e04da00" + "0" * 56
ACCEPTED = {"schema": "lcbench.accepted_packages.v1",
            "tasks": {TASK: [{"package_sha256": "1b3f7f03" + "0" * 56, "task_sha256": TASK_SHA,
                              "get": "gh release download preview-toyarith-1 --repo MathCompressionBench/mcb"}]},
            "retired": {TASK: [{"name": "preview-toyarith-0", "package_sha256": "deadbeef" + "0" * 56,
                                "task_sha256": "0123abcd" + "0" * 56, "replaced_by": "preview-toyarith-1"}]}}
IDENT = ["-c", "user.name=test", "-c", "user.email=test@example.invalid"]


ENTRY = "acme-1"
METADATA = f"""\
system: "Acme Prover"
model: example-model-2026-09-01
harness: "example-harness 1.4.2"
reasoning_effort: high
track: open
human_assisted: false
tasks: [{TASK}]
attempts_per_task: 2
contact: "you@example.org"
"""


def make_bundle(label: str = "a bundle written by ./submit", task_sha: str | None = TASK_SHA, track=None,
                budget="unlimited") -> bytes:
    """A deterministic tar.gz shaped like a ./submit bundle: submission/SUBMISSION.json names the task sha256 it was
    made for (task_sha None: no SUBMISSION.json) and the run's track and budget."""
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w") as tar:
        data = json.dumps({"task_sha256": task_sha, "label": label,
                           "metadata": {"track": track, "run": {"budget_seconds": budget}}}).encode()
        info = tarfile.TarInfo("submission/SUBMISSION.json" if task_sha is not None else "submission/OTHER.json")
        info.size = len(data)
        tar.addfile(info, io.BytesIO(data))
    return gzip.compress(raw.getvalue(), mtime=0)


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *IDENT, *args], check=True, capture_output=True,
                          text=True).stdout.strip()


class SubmissionBranch(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "submissions"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        git(self.repo, "symbolic-ref", "HEAD", "refs/heads/main")
        (self.repo / "README.md").write_text("submissions\n")
        (self.repo / "accepted-packages.json").write_text(json.dumps(ACCEPTED))
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "base")
        git(self.repo, "checkout", "-q", "-b", "my-submission")

    def tearDown(self):
        self.tmp.cleanup()

    def add(self, bundle: bytes | None = None, task: str = TASK, sid: str | None = None,
            meta_over: dict | None = None, receipt: dict | None = None, metadata: bool = True) -> str:
        bundle = make_bundle() if bundle is None else bundle
        sid = sid or hashlib.sha256(bundle).hexdigest()
        d = self.repo / "submissions" / task
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{sid}.tar.gz").write_bytes(bundle)
        meta = {"schema": "lcbench.intake_submission.v1", "task": task, "submission_id": sid,
                "participant": "team-test", "track": None, "claimed": {"expr_nodes_with_levels_v1": 8331},
                "entry": ENTRY}
        meta.update(meta_over or {})
        if self.write_entry and not (self.repo / "entries" / ENTRY / "metadata.yaml").exists():
            self.entry(METADATA)
        if metadata:
            (d / f"{sid}.json").write_text(json.dumps(meta))
        if receipt is not None:
            (d / f"{sid}.receipt.json").write_text(json.dumps(receipt))
        return sid

    write_entry = True

    def entry(self, text: str, name: str = ENTRY) -> None:
        (self.repo / "entries" / name).mkdir(parents=True, exist_ok=True)
        (self.repo / "entries" / name / "metadata.yaml").write_text(text)

    def problems(self) -> list[str]:
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "submission")
        return check_submission.check(self.repo, "main")

    def test_bundle_metadata_and_receipt_pass(self):
        sid = self.add()
        other = make_bundle("another bundle")
        self.add(bundle=other, receipt={"bundle_sha256": hashlib.sha256(other).hexdigest()})
        self.assertEqual(self.problems(), [])
        self.assertTrue(sid)

    def test_command_line_reports_ok_and_exit_code(self):
        self.add()
        self.problems()
        out = subprocess.run([sys.executable, str(SCRIPT), "--base", "main"], cwd=self.repo, capture_output=True,
                             text=True)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)
        self.assertIn("OK", out.stdout)

    def test_changed_bundle_is_refused(self):
        self.add(sid="0" * 64, meta_over={"submission_id": "0" * 64})
        self.assertTrue(any("differs from its submission ID" in p for p in self.problems()))

    def test_other_paths_are_refused(self):
        self.add()
        (self.repo / "notes.txt").write_text("hello\n")
        self.assertTrue(any(p.startswith("notes.txt:") for p in self.problems()))

    def test_changing_an_existing_file_is_refused(self):
        self.add()
        (self.repo / "README.md").write_text("changed\n")
        self.assertTrue(any("README.md" in p for p in self.problems()))

    def test_executable_files_are_refused(self):
        sid = self.add()
        os.chmod(self.repo / "submissions" / TASK / f"{sid}.tar.gz", 0o755)
        self.assertTrue(any("non-executable" in p for p in self.problems()))

    def test_missing_or_wrong_metadata_is_refused(self):
        self.add(metadata=False)
        self.add(bundle=make_bundle("second"), meta_over={"task": "another-task"})
        self.add(bundle=make_bundle("third"), meta_over={"claimed": {"expr_nodes_with_levels_v1": "8331"}})
        got = "\n".join(self.problems())
        self.assertIn("metadata file", got)
        self.assertIn("differs from the directory", got)
        self.assertIn("must be an integer", got)

    def test_receipt_for_another_bundle_is_refused(self):
        self.add(receipt={"bundle_sha256": "f" * 64})
        self.assertTrue(any("another bundle" in p for p in self.problems()))

    def test_more_than_five_submissions_are_refused(self):
        for i in range(6):
            self.add(bundle=make_bundle(f"bundle {i}"))
        self.assertTrue(any("at most 5" in p for p in self.problems()))

    def test_bundle_from_a_package_that_is_not_accepted_is_refused(self):
        """Regression for pull request #3: a bundle made from a package the organizers did not accept was found only
        after a verification job. The check names the accepted packages and how to get them."""
        self.add(bundle=make_bundle(task_sha=OTHER_TASK_SHA))
        got = "\n".join(self.problems())
        self.assertIn("7e04da00", got)
        self.assertIn(ACCEPTED["tasks"][TASK][0]["package_sha256"], got)
        self.assertIn(TASK_SHA, got)
        self.assertIn("gh release download preview-toyarith-1", got)

    def test_bundle_from_a_retired_package_names_its_replacement(self):
        self.add(bundle=make_bundle(task_sha="0123abcd" + "0" * 56))
        got = "\n".join(self.problems())
        self.assertIn("preview-toyarith-0", got)
        self.assertIn("retired", got)
        self.assertIn("preview-toyarith-1", got)

    def test_bundle_without_submission_json_is_refused(self):
        self.add(bundle=b"not a tarball")
        self.assertTrue(any("SUBMISSION.json" in p for p in self.problems()))

    def test_task_that_is_not_accepted_is_refused(self):
        self.add(task="ramsey96-warm")
        self.assertTrue(any("do not accept the task 'ramsey96-warm' (open tasks: toyarith-warm)" in p
                            for p in self.problems()))

    def test_no_metadata_yaml_is_refused(self):
        self.write_entry = False
        self.add()
        self.assertTrue(any("adds no entries/<entry>/metadata.yaml" in p for p in self.problems()))

    def test_a_missing_required_field_is_named(self):
        self.entry(METADATA.replace('contact: "you@example.org"\n', ""))
        self.add()
        self.assertIn(f"entries/{ENTRY}/metadata.yaml: contact is missing", "\n".join(self.problems()))

    def test_an_unreadable_metadata_yaml_names_its_line(self):
        self.entry(METADATA.replace("human_assisted: false", "human_assisted: no"))
        self.add()
        self.assertIn("line 6: write true or false", "\n".join(self.problems()))

    def test_one_metadata_yaml_per_pull_request(self):
        self.add()
        self.entry(METADATA, name="acme-2")
        self.assertTrue(any("one pull request is one submission" in p for p in self.problems()))

    def test_an_existing_entry_is_not_changed(self):
        self.entry(METADATA)
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "an earlier submission, merged")
        git(self.repo, "branch", "-f", "main")
        self.entry(METADATA.replace("attempts_per_task: 2", "attempts_per_task: 3"))
        self.add()
        self.assertTrue(any("new entry name" in p for p in self.problems()))

    def test_every_bundle_names_the_entry_and_a_listed_task(self):
        self.add(meta_over={"entry": "someone-else"})
        got = "\n".join(self.problems())
        self.assertIn("it must name this pull request's entry 'acme-1'", got)

    def test_agent_track_rules(self):
        agent60 = METADATA.replace("track: open", "track: agent-60")
        self.entry(agent60)
        self.add(bundle=make_bundle("ok", track="agent", budget=3600))
        self.assertEqual(self.problems(), [])
        self.add(bundle=make_bundle("too long", track="agent", budget=7200))
        self.add(bundle=make_bundle("not an agent run", track="record", budget=3600))
        got = "\n".join(self.problems())
        self.assertIn("at most 3600 seconds per run", got)
        self.assertIn("lcbench start --track agent", got)

    def test_human_help_is_open_track_only(self):
        self.entry(METADATA.replace("track: open", "track: agent-120").replace("human_assisted: false",
                                                                              "human_assisted: true"))
        self.add(bundle=make_bundle("x", track="agent", budget=7200))
        self.assertTrue(any("human_assisted must be false" in p for p in self.problems()))

    def test_metadata_yaml_alone_is_refused(self):
        self.entry(METADATA)
        self.assertIn("the branch adds no bundle beside its metadata.yaml", self.problems())

    def test_the_readme_and_template_name_exactly_the_validators_fields(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import submission_meta
        readme = (ROOT / "README.md").read_text()
        table = re.search(r"<!-- begin metadata-fields -->(.*?)<!-- end metadata-fields -->", readme, re.S).group(1)
        self.assertEqual(re.findall(r"^\| `(\w+)`", table, re.M),
                         list(submission_meta.REQUIRED + submission_meta.OPTIONAL))
        meta, problems = submission_meta.load(ROOT / "templates/metadata.yaml")
        self.assertEqual(problems, [])
        self.assertEqual(set(meta), set(submission_meta.REQUIRED + submission_meta.OPTIONAL))

    def test_empty_branch_is_refused(self):
        self.assertEqual(check_submission.check(self.repo, "main"), ["the branch adds no files compared with main"])


if __name__ == "__main__":
    unittest.main()
