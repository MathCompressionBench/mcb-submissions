# MathCompressionBench submissions

This repository is where you submit results to **MathCompressionBench**, the benchmark for making Lean proofs smaller. You
submit by opening a pull request.

In short:

1. You open a pull request that adds your bundles (the files `./submit` writes) and one `metadata.yaml` that
   describes your system.
2. The organizers' check rebuilds and re-scores every bundle on their machines and posts the verdict, the node count
   and the organizers' receipt as a comment on your pull request.
3. An organizer reviews your `metadata.yaml` and merges the pull request.
4. On every merge, the leaderboard is regenerated from the receipts of every merged submission, and the site is
   rebuilt.

The full specification is [docs/SUBMITTING.md](https://github.com/MathCompressionBench/mcb/blob/main/docs/SUBMITTING.md) in
the MathCompressionBench repository; this README has what you need to submit.

**Open for submissions now: `toyarith-warm` only.** The lcbench-v1 tasks described in the MathCompressionBench README
work with the tools but are not open yet; a pull request for them is refused, and `mcb intake add` refuses to
add them. The toy task belongs to no task set, so it is checked and commented on but not ranked.

## What you need

- **The benchmark code:** the repository https://github.com/MathCompressionBench/mcb, branch **`main`**. The task package below is made for `main`.

  ```sh
  gh repo clone MathCompressionBench/mcb -- -b main
  # or: git clone -b main git@github.com:MathCompressionBench/mcb.git
  ```

  Run the commands below from that checkout as `bin/mcb ...`. They need `python3` 3.10 or later and `git`.
- **Lean `leanprover/lean4:v4.32.0`**, installed with elan unless it is already there (`elan toolchain install`
  fails on an installed toolchain):

  ```sh
  elan toolchain list | grep -q 'leanprover/lean4:v4.32.0' || elan toolchain install leanprover/lean4:v4.32.0
  export PATH="$HOME/.elan/toolchains/leanprover--lean4---v4.32.0/bin:$PATH"
  lean --version        # must say 4.32.0
  ```

- **The task package.** For the toy task `toyarith-warm`, download it from the release `toyarith-rc.10.2`:

  ```sh
  gh release download toyarith-rc.10.2 --repo MathCompressionBench/mcb    # toyarith-warm.tar.gz and its .sha256
  ```

  or build it yourself in the MathCompressionBench checkout and compare its sha256 with the table below:

  ```sh
  bin/mcb make-task tasks/toyarith/task_source.json --mode warm --out dist --workdir work   # dist/toyarith-warm.tar.gz
  ```

## Accepted task packages

A bundle must be made from one of these packages; any other is refused (the pull request's answer lists them).
`mcb start` prints the package sha256 and the task sha256, and `./check` prints the task sha256. The same list
is in [accepted-packages.json](accepted-packages.json), which `scripts/check_submission.py` reads. The organizers
write both tables and that file from their intake's configuration, so they always agree.

<!-- begin accepted-packages (written by the organizers' intake from its configuration; do not edit) -->
| task | package sha256 | task sha256 | how to get it |
|---|---|---|---|
| `toyarith-warm` | `f381a2302711091efa5c51d55b8bdfb157c2b9ad5e87481989ae76b2d5d583b1` | `a58f2689c2ca3c29c83ec39578b5d29ec39e8e1f02e1ab2bcdcb7ebd8b2c56a1` | `gh release download toyarith-rc.10.2 --repo MathCompressionBench/mcb` |
<!-- end accepted-packages -->

Bundles made from earlier preview packages are refused. If your workspace came from one of them, start a new
workspace from the package above, copy your proof files into it and run `./submit` again.

<!-- begin retired-packages (written by the organizers' intake from its configuration; do not edit) -->

<!-- end retired-packages -->

## Tracks

Every submission names one track. Each track has its own leaderboard table.

| track | who | time limit per run | human help |
|---|---|---|---|
| `open` (the main track) | anyone, by any means | none | allowed, but it must be declared; every entry shows a "human-assisted" flag |
| `agent-60` | an agent alone | 60 minutes of wall-clock time | none |
| `agent-120` | an agent alone | 120 minutes of wall-clock time | none |

An agent-track result also counts on `open`. The study's runs are listed on the agent track of their time limit
(the study: the organizers' runs of six agents on the seven tasks of lcbench-v1 (September 2026)), and all of
them on `open`.

## How entries are ranked

Leaderboards are per task set and per track. A task set is a fixed list of tasks; once frozen it never changes.
`lcbench-v1` is the study's seven tasks.

1. On each task, a system's best verified final is its smallest verified node count.
2. Systems are ranked on each task by that node count, smallest first. Tied systems share the mean of the places they
   span; a system without a verified final on the task ranks last.
3. The overall ranking is the average rank over the task set's tasks. Lower is better.

The leaderboard never states compression factors. A system is the combination of `system`, `model`, `harness`,
`reasoning_effort` and `human_assisted` (compared without regard to case or spacing): all merged submissions that
agree on these are pooled, and only the best final per task counts; each task shows which submission or study run and
which receipt supplied it. A submission that names one of the study's agents as the study records it joins that
agent's row; if the study recorded a version you cannot state, write that it was not recorded (for example
`harness: "<harness name> (version not recorded)"`), and it joins only when every other field matches. You may make any
number of attempts, but `attempts_per_task` must say truthfully how many you made in all so far; the largest number
declared is shown.

## What you submit

One pull request is one submission. It adds:

| file | what it is |
|---|---|
| `entries/<entry>/metadata.yaml` | one per submission: your system, the track and the tasks (below) |
| `submissions/<task>/<id>.tar.gz` | the bundle written by `./submit`. `<id>` is the SHA-256 hash of this file, so do not change the file after `./submit` |
| `submissions/<task>/<id>.json` | a small file with your name, the score you report and the entry it belongs to |
| `submissions/<task>/<id>.receipt.json` | optional: the result of checking your bundle on your own machine with `mcb verify` |

`<task>` is the name of the task package without `.tar.gz`, for example `toyarith-warm`. `<entry>` is a name you
choose for this submission: lowercase letters, digits, `.`, `_` or `-`, at most 64 characters, for example
`acme-prover-2026-10-12`. Every submission takes a new entry name.

### metadata.yaml

Copy [templates/metadata.yaml](templates/metadata.yaml) to `entries/<entry>/metadata.yaml` and fill it in. Every
field is required except `links` and `logs`. **A submission missing a required field is not reviewed:** the
organizers' check refuses the pull request and names the field.

<!-- begin metadata-fields -->
| field | what to write |
|---|---|
| `system` | the name of your system, as the leaderboard shows it |
| `model` | the model and its version (a model id with its date or release); name every model if there are several |
| `harness` | the program that ran the model, with its version |
| `reasoning_effort` | the reasoning effort the model ran with (for example `low`, `medium`, `high`), or `none` |
| `track` | `open`, `agent-60` or `agent-120` |
| `human_assisted` | `true` or `false`; on `agent-60` and `agent-120` it must be `false` |
| `tasks` | the tasks this submission covers, for example `[toyarith-warm]`; every bundle's task must be one of them |
| `attempts_per_task` | how many attempts you made per task in all, counting the ones you do not submit: one whole number, or one number per task |
| `contact` | how the organizers reach you (an email address); it is never published |
| `links` | optional: a list of links (an article, code or a write-up) |
| `logs` | optional: a link to your run logs, or a list of links |
<!-- end metadata-fields -->

For example:

```yaml
system: "Acme Prover"
model: "example-model-2026-09-01"
harness: "example-harness 1.4.2"
reasoning_effort: high
track: agent-60
human_assisted: false
tasks: [toyarith-warm]
attempts_per_task: 3
contact: "you@example.org"
links: ["https://example.org/acme-prover"]
```

Put a value in double quotes when it holds `: ` or `#`, and write `true` or `false`, not `yes` or `no`. The file is
read as a small part of YAML, and anything outside it is refused with its line number.

## Step by step

1. **Start.** Set up a workspace from the task package. The budget is the time you allow yourself, stated up front.
   For `agent-60` and `agent-120`, start every run as an agent run with the track's budget:

   ```sh
   bin/mcb start "file://$PWD/toyarith-warm.tar.gz" --dir <workspace> --track agent --budget-seconds 3600   # agent-60
   bin/mcb start "file://$PWD/toyarith-warm.tar.gz" --dir <workspace> --track agent --budget-seconds 7200   # agent-120
   bin/mcb start "file://$PWD/toyarith-warm.tar.gz" --dir <workspace> --unlimited                           # open
   ```

   The task is then in `<workspace>/toyarith-warm/`. The bundle records the track and the budget; on an agent track,
   a bundle from a workspace started without `--track agent`, or with a larger budget, is refused. Starting again in
   a new workspace does not start a new budget: the time limit is per run, and the time spent in earlier workspaces of
   the same run counts.

2. **Work.** Edit the proofs in the workspace. `TASK.md` in the workspace says what may and may not change.

3. **Check.** Run `./check` in the workspace. It runs the same code as the organizers' check and prints whether
   the submission is valid and its score (the node count; smaller is better).

4. **Submit.** Run `./submit`. It checks again, then writes the bundle
   `submissions/submission-<first 16 hex digits of the id>.tar.gz` and prints the full submission ID `<id>` (the
   bundle's SHA-256 hash). Nothing is sent anywhere.
   If an agent made the run and you ran `./submit` once more on its final files after it stops,
   submit that bundle. The budget covers the agent's work only, not that final `./submit` or `mcb verify`.

5. **Optional: check the bundle yourself.** This makes the same kind of record the organizers will make:

   ```sh
   bin/mcb verify <task package .tar.gz> <bundle> --workdir <empty directory> --out self-receipt.json
   ```

   On a Mac, or on Linux without the sandbox, it says `unverified`. That is expected: only the organizers' run
   can be verified.

6. **Add your files.** Clone this repository (or your fork of it) and make a new branch:

   ```sh
   gh repo clone MathCompressionBench/mcb-submissions      # or: git clone git@github.com:MathCompressionBench/mcb-submissions.git
   git -C lcbench-submissions switch -c my-submission
   ```

   Then, in the MathCompressionBench checkout, add each bundle under your entry name:

   ```sh
   bin/mcb intake add <this repository's checkout> <task> <bundle> --participant "<your name or team>" \
       --entry <entry> [--self-receipt self-receipt.json]
   ```

   `intake add` writes the track that the bundle records (from `mcb start --track`); `--track` is
   optional, and when given it must be the same.

   It first checks that the task is open and that the bundle was made from an accepted package (it reads
   `accepted-packages.json` in your checkout) and refuses otherwise. Then it copies the bundle to
   `submissions/<task>/<id>.tar.gz`, writes `<id>.json`, and copies your self-receipt to `<id>.receipt.json` if you
   gave one. You can also write `<id>.json` by hand:

   ```json
   {
    "schema": "lcbench.intake_submission.v1",
    "task": "toyarith-warm",
    "submission_id": "<id>",
    "participant": "<your name or team>",
    "track": null,
    "claimed": {"expr_nodes_with_levels_v1": 8331},
    "entry": "<entry>"
   }
   ```

   `claimed` holds the score you report, as printed by `./check` (an integer), and `track` the track the bundle
   records (`null` for a workspace started without `--track`).

7. **Write the metadata.** Copy `templates/metadata.yaml` to `entries/<entry>/metadata.yaml`, fill it in, and check
   it (from the MathCompressionBench checkout, or with plain Python from this checkout):

   ```sh
   bin/mcb submission validate <this repository's checkout>/entries/<entry>
   python3 scripts/submission_meta.py validate entries/<entry>
   ```

8. **Check the pull request before you open it.** Commit the files, then run

   ```sh
   python3 scripts/check_submission.py
   ```

   It applies the same rules the organizers apply (below) to your branch, compared with `main`, including the
   accepted packages and the metadata, and says what to fix. It needs only Python 3 and git.

9. **Open a pull request** to `main` of this repository and fill in its template. You do not need to do anything
   else unless an organizer asks.

## Rules for the pull request

The pull request may only **add** `entries/<entry>/metadata.yaml` and files named `submissions/<task>/<id>.tar.gz`,
`<id>.json` and `<id>.receipt.json`. If anything else is in it, the whole pull request is refused and nothing in it is
checked:

- any other path, or a changed or deleted file (an existing entry is never changed: a new submission takes a new
  entry name);
- no `metadata.yaml`, more than one, a missing required field, or a field the template does not have;
- a bundle whose `<id>.json` does not name the entry, or whose task is not in `tasks`;
- on `agent-60` or `agent-120`: `human_assisted: true`, or a bundle from a workspace not started with
  `--track agent` and a budget of at most 3600 (or 7200) seconds;
- a symbolic link or an executable file;
- a bundle whose SHA-256 hash is not its `<id>` (the file was changed after `./submit`);
- a missing `<id>.json`, or one whose fields do not match the file name and task;
- more than five bundles in one pull request, a bundle over 256 MB, a `.json` file over 1 MB, or a `metadata.yaml`
  over 64 KB;
- a task the organizers do not accept yet, or a bundle made from a task package that is not in the list above.

If you push more commits to the pull request, its newest commit is looked at again.

## What happens after you open the pull request

| listing | meaning |
|---|---|
| **self-reported** | The pull request had the right shape and the bundle matches its ID. The score shown is the one you reported. The organizers' check has not finished yet |
| **verified** | The organizers rebuilt and re-scored your bundle on their machines, in the official sandbox, and got exactly what you reported: the same verdict and the same scores |
| **mismatch** | The organizers' check accepted the bundle but got a different result from what you reported. The entry shows the verified score and what differed |
| **rejected** | The organizers' check rejected the bundle, for example because a proof does not compile or a statement changed. The problems are listed |
| **infra-failed** | A machine failure: the organizers' machines failed three times for reasons that have nothing to do with your submission. A person looks at it; it is not a verdict on your work |

Checks run every so often, not the moment you open the pull request, so expect your entry to stay
self-reported for a while.

Machine trouble never counts against you: a check that fails or runs out of time because of the machine is
retried on another machine.

## How you see the result

The organizers' intake keeps one comment on your pull request, **lcbench check status**, and edits it whenever the
status changes (it does not add new comments). It shows:

- your `metadata.yaml` as the reviewer sees it (never the contact), and any listed task without a bundle;
- for each bundle: received, waiting with your place in the queue and an estimated wait ("no estimate while checks
  cannot start" while the organizers' machines cannot start checks), being checked, and then verified with the node
  count, or mismatch, rejected or infra-failed;
- for each finished check, the organizers' **receipt**: a table row with the result, the node count, the receipt root
  and its entry in the organizers' append-only receipt log, and a folded block with the receipt's main fields
  (verdict, scores, problems, the run's track and budget, the verifier version and the receipt's SHA-256);
- on an agent track, whether each verified receipt qualifies for it;
- a line for the reviewer saying whether the submission is ready for review.

Its bold first line follows the status, for example "checked: verified" once the check is done. The organizers'
GitHub account posts and edits it; a comment by anyone else is not the status, even if it looks like one. The
bundles' status (without the metadata and receipt sections) is also attached to the newest commit of your pull
request as a git note:

```sh
git fetch https://github.com/MathCompressionBench/mcb-submissions.git refs/notes/intake:refs/notes/intake
git log --notes=intake -1 <your commit>
```

- **Who you are** is the GitHub account that opened the pull request; the name in your `.json` file is only how your
  bundle is listed, and `system` is how the leaderboard shows your entry.
- **The same bundle twice:** byte-identical bundles count once. The pull request opened first gets the credit; a
  later one is listed as "duplicate of #N" and is not ranked.
- **New commits:** if you push a new commit to your pull request (also a force-push), the newest commit counts; a
  bundle that only an earlier commit had is listed as "replaced".

## Review, merge and the leaderboard

An organizer reads your `metadata.yaml` and the comment, and merges when the metadata is complete and plausible and
the bundles are verified (they may ask you to drop or fix a bundle first). A pull request closed without merging adds
nothing to the leaderboard.

After every merge, the organizers regenerate the leaderboard from every merged `metadata.yaml` and the organizers'
receipts of the merged bundles, and rebuild the site. Only verified bundles made from a task set's packages count,
and on an agent track only those whose receipt records an agent run within the time limit (they still count on
`open`). Anything not counted is listed in the leaderboard data with the reason.

## Questions

Open an issue in this repository, MathCompressionBench/mcb-submissions:
https://github.com/MathCompressionBench/mcb-submissions/issues.
