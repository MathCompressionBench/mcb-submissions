<!-- One pull request is one submission: one entries/<entry>/metadata.yaml and up to five bundles. Please fill in the
lines below; the metadata.yaml itself is what the organizers review. -->

**Entry:** <!-- entries/<entry>/metadata.yaml -->

**System, track and tasks:** <!-- e.g. Acme Prover, agent-60, toyarith-warm -->

**Submission ID(s) and self-reported score(s):** <!-- the <id> printed by ./submit and the node count printed by ./check -->

**Human-assisted?** <!-- no / yes: how a person helped (open track only) -->

**Method (optional):** <!-- a sentence or a link -->

Before opening:

- [ ] This pull request only adds `entries/<entry>/metadata.yaml`, `submissions/<task>/<id>.tar.gz`, `<id>.json` and optionally `<id>.receipt.json`.
- [ ] `metadata.yaml` has every required field (system, model with version, harness with version, reasoning_effort, track, human_assisted, tasks, attempts_per_task, contact), and `attempts_per_task` counts every attempt, not only the submitted ones.
- [ ] On `agent-60` / `agent-120`: an agent alone, every run started with `--track agent --budget-seconds 3600` / `7200`.
- [ ] The bundles are exactly the files written by `./submit` (not changed afterwards).
- [ ] `python3 scripts/check_submission.py` prints `OK`.

The organizers' check posts its result on this pull request: the verdict, the node count and the organizers' receipt
of each bundle. An organizer then reviews the metadata and merges; the leaderboard is regenerated after every merge.
See the README for how to read the answer.
