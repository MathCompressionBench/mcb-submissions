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

**Open for submissions now: the seven lcbench-v1 tasks, the 175 oai-v1 tasks and `toyarith-warm`.** Each lcbench-v1
task (ramsey96, slt26, slt49, permanent2, compactness5, mathlib197 and mathlib372) is open with its `warm` and its
`no_hint` package; each oai-v1 task (made from OpenAI's published math challenges, https://github.com/openai/math)
is open with its `warm` package; all are listed in the table below. The toy task belongs to no task set, so it is
checked and commented on but not ranked.

An untouched no_hint package reports INVALID: its target proofs are replaced by `sorry`, and `./check` names every
target whose proof is, or uses, a replaced one (for example 175 of the 197 targets of mathlib197). The baseline in
its `TASK.md` is the node count of the original proofs; your proofs are scored against it once no target uses
`sorry`.

## What you need

- **The benchmark code:** the repository https://github.com/MathCompressionBench/mcb, branch **`main`**. The newest task packages below are made for `main`.

  ```sh
  git clone -b main https://github.com/MathCompressionBench/mcb.git
  ```

  Run the commands below from that checkout as `bin/mcb ...`. They need `python3` 3.10 or later and `git`.
- **Lean `leanprover/lean4:v4.32.0`** for the toy task and the lcbench-v1 tasks, **`leanprover/lean4:v4.34.1`** for
  the oai-v1 tasks (each package's `TASK.json` names its toolchain), installed with elan unless it is already there
  (`elan toolchain install` fails on an installed toolchain). For 4.32.0:

  ```sh
  elan toolchain list | grep -q 'leanprover/lean4:v4.32.0' || elan toolchain install leanprover/lean4:v4.32.0
  export PATH="$HOME/.elan/toolchains/leanprover--lean4---v4.32.0/bin:$PATH"
  lean --version        # must say 4.32.0
  ```

  For an oai-v1 task, the same with `v4.34.1` in place of `v4.32.0`.

- **The task package.** For the toy task `toyarith-warm`, download it from the release `toyarith-rc.11`:

  ```sh
  curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/toyarith-rc.11/toyarith-warm.tar.gz
  curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/toyarith-rc.11/toyarith-warm.tar.gz.sha256
  # or, logged in to GitHub: gh release download toyarith-rc.11 --repo MathCompressionBench/mcb
  ```

  For an lcbench-v1 task, download its package and its `.sha256` file from the release `lcbench-v1-rc.11`, for
  example the warm package of ramsey96:

  ```sh
  curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.11/ramsey96-warm.tar.gz
  curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.11/ramsey96-warm.tar.gz.sha256
  ```

  The lcbench-v1 tasks import Mathlib; the MathCompressionBench README (section "The lcbench-v1 tasks: dependencies")
  says how to provide the pinned Lake packages.

  For an oai-v1 task, download its package and its `.sha256` file from the release `oai-v1-rc.11`, for example
  oai-matrix-fields:

  ```sh
  curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-matrix-fields-warm.tar.gz
  curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-matrix-fields-warm.tar.gz.sha256
  ```

  The oai-v1 tasks build on the Lake packages of github.com/openai/math at the commit their `TASK.json` pins; the
  MathCompressionBench README (section "The oai-v1 tasks: dependencies") says how to prepare them once and pass them
  to `start` with `--deps`.

  For the toy task you can also build the package yourself in the MathCompressionBench checkout and compare its sha256
  with the table below:

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
| `compactness5-no_hint` | `3bb0c3a52c0b34ffaa3dde6fe4c02d1aa3a9d2e0d007aba36993f8a3c2a1a029` | `5f905d0d02904ac50d0e938139fd08d3118877c0376017cb5dce5dbcc9cd7a8e` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.11/compactness5-no_hint.tar.gz` |
| `compactness5-no_hint` | `d089a0414f93339f8ba431169eec36b7fa5bf30ec4ae55a180ebdc45c18fad9a` | `3aa5fdbb6282db578436c02583a2f6eb55aa4423a33143441104739379e844a9` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.3/compactness5-no_hint.tar.gz` |
| `compactness5-no_hint` | `6a86f27a5a737415b4bb8f695dcb47de40d53ce82105fd8aaf48275d2f66fc3a` | `f8ce12207cf01afeb2009b0e41525889625597ca9ec8aabe8d890ee8b9ab6f54` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.2/compactness5-no_hint.tar.gz` |
| `compactness5-warm` | `77c706dc12f2068abe74c68a3cc0b6f747298393f370a5023abd97cf7aff6402` | `15727b9810472513163c4f3f8a7e41cf2a47a70ec7547c597c06ef1efa932fef` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.11/compactness5-warm.tar.gz` |
| `compactness5-warm` | `0e6b3aee5f7fd2c69098a12635e4f5dd29dd3c290b04f1b25f21ce08361f768f` | `17554e6ca46f7b653c08cebb57bc3cf9e56be409884c2a80c48f0fa924fbec96` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.3/compactness5-warm.tar.gz` |
| `compactness5-warm` | `b2086e6b13963b9fa35ee7b576d51842e63aae7c11a593452404d38addd46a57` | `6ed3a88f04c6772684bfa61727207ed78de68d6937d0be5531e1e2e9775c2ef8` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.2/compactness5-warm.tar.gz` |
| `mathlib197-no_hint` | `24c66bb849c62688c31095e448c279fcb821ea05a6b2af5102c8c8d364f0c505` | `cafddb418e040b61e0361a754a612e1feaffd3b93a855c8eb4025031cddc6a0c` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.11/mathlib197-no_hint.tar.gz` |
| `mathlib197-no_hint` | `0f6d5f5759ab353703f3dec565f42d4ea338438a571ae900c179faa78a18fdc2` | `86350d3db5d66f05a88778d224d0f253c173194eb97c3825b403ffc9ff5e96ef` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.3/mathlib197-no_hint.tar.gz` |
| `mathlib197-no_hint` | `ee9cfc7bf5235c80fb851317a93fd12b792f90e431fdbf4e14cffc834e792009` | `6d7ba37f4088f58b7126c393a058dcbbefc7930b39809789436e2b65a6aca3ac` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.2/mathlib197-no_hint.tar.gz` |
| `mathlib197-warm` | `b9ca260045732698b31db2c8ecbad3b54a5b4621f6e909c672c666725d7bc8be` | `569593620d63899798b87fbf055330912d08c0dfa92df7779dff4eb67be66e87` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.11/mathlib197-warm.tar.gz` |
| `mathlib197-warm` | `17a83ae30558f690b1403d906dca89537d03b34e102e4d2d2f833fd7fa34b07b` | `ff10aca12e6e33c4e246cf5b5ca89e65440023c4a223bbcf34b5d098a92970bd` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.3/mathlib197-warm.tar.gz` |
| `mathlib197-warm` | `13b92df3ee48cb9e15378567050916bd3f43f0b7d9044176978c90f2f426ef2c` | `e7dec6c30a07fc4761b74d8e58b6d27f0d168fbed1728110b9fcbdea78fc38b4` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.2/mathlib197-warm.tar.gz` |
| `mathlib372-no_hint` | `2ad9fc502d860ebe20794d65b18c4f1cd6d41ec6e48567af57ff2aa2240d8971` | `483a715c030f86ef301e34441d923e6c2150210fba8025562883ce1ddda6a5b9` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.11/mathlib372-no_hint.tar.gz` |
| `mathlib372-no_hint` | `bcc706541abaec1c06056a5a62c75213b110875e7f76009e88aafde2d93b70ef` | `7042b3a2d1c490b2db81d5f4b2e92174972b9f9f23692c8a81f6809bf82d1aee` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.3/mathlib372-no_hint.tar.gz` |
| `mathlib372-no_hint` | `c59f59f46746ccbc72017323e85ac346c5377e1fc1e12d3fe6abef0139e2ccf2` | `11a550a6e9a5bd2161a1287e7ab257ac42ef9aa387a0252afceb63980c3f4d7a` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.2/mathlib372-no_hint.tar.gz` |
| `mathlib372-warm` | `fcd17b464e09eb5c824107dcb09030dc82c1304b660bf730eb127872e5c155e7` | `3b9b662616c6b5ae8d0d97bb003b6da4ef62dcb7c9314dd07179e6fa96e6ad6e` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.11/mathlib372-warm.tar.gz` |
| `mathlib372-warm` | `a3ca91a9b709c46dc48c35df2ab8235a281d19d246ed1baa34ffc997cc3921dc` | `55dc96e940ab0c38f6b0069da854e68c8024afe9e7d3d712ab0d57f3333ce0bc` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.3/mathlib372-warm.tar.gz` |
| `mathlib372-warm` | `750d328d04c52eedda84d8e9d59d18ef84b91fc75b9a559a13c0257a6297b3a0` | `cab594d34900413b4543e10fb16a24d80aed4dbbd5bde8c35928e07d5c22d783` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.2/mathlib372-warm.tar.gz` |
| `oai-abhyankar-sathaye-warm` | `db13deaee81f7db9b4d8208ef63a7e2c95d9f78c6d739af7b2b595478ffd6367` | `c6dcd12e5869cc43bfc5657ad5e690f944f99115205b8d096832e4d35ed0c1f8` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-abhyankar-sathaye-warm.tar.gz` |
| `oai-amplitude-damping-warm` | `091accc7eec21c6a140996a53f9f0ac224d164fc6789e77f4f5320b66e59c5b2` | `520ba6a9b829afb235648e6259f6f45b74424efc046c585bd49c9ed03b8694bf` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-amplitude-damping-warm.tar.gz` |
| `oai-arnold-counterexample-warm` | `cf421ff79cd3ad2821792ba60bb919d11a1637b792806fcb7f5dd76245b1f2c1` | `211fa1acd877ae0b107de43ef51f6e553bc178d57aead27c8a0d9f0bd8959274` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-arnold-counterexample-warm.tar.gz` |
| `oai-artin-cat0-warm` | `0cb12e31dc25e27a5adedad0a64786df7c9a406c499470365e07f1652c8d3a46` | `135e6824da95a0adea59f7468de20ee0d4c3d54786c4e8ad2a378fa2e627ce28` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-artin-cat0-warm.tar.gz` |
| `oai-asymptotically-minimal-littlewood-warm` | `19fa9fd7925fb780613fe1abadab8aee2203f457fca87679dfcfe97492420ccb` | `0b3465bd0f5324a119c0789e27afdd4c60ff0259ff255c7faaa6c248735e1849` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-asymptotically-minimal-littlewood-warm.tar.gz` |
| `oai-auslander-reiten-warm` | `31ef979170472999211280ec2267b95472a0981d50020ec5368623d7b34e6dad` | `a59744bb1fd24fe9092e561f947a8bf5fb52d4c7d4c43bd531af801ebf45b2df` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-auslander-reiten-warm.tar.gz` |
| `oai-backward-intertwiners-warm` | `5ab48192c2d84918a3f222cdf0e34dfdcac28557600cae9b9eb5398fac72e185` | `98846cec5c4a00173f631cdc9dd88d73afd7cccd892f7d56d530b90ab4c90730` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-backward-intertwiners-warm.tar.gz` |
| `oai-bass-trace-warm` | `b2422e14121a44f20760aa3fafcb66a5f4df45c48f0b37618f2c0ed76e194a80` | `ec6aa3e4152bdcf8b7bd37a0a5aed6e1c2469cc9797e62fb589a3621640ff197` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-bass-trace-warm.tar.gz` |
| `oai-biholder-transport-warm` | `502e684edd5b1e3a49b58ed78c7c90e6997ff3cacb405338454f52c8e5b4904e` | `4531ab85d722b08b1514cfce2a27e85a69b49f363dc41abd108305114bf09376` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-biholder-transport-warm.tar.gz` |
| `oai-bin-packing-gap-warm` | `555e8defc9f7422a7800fe3a69617406cbdce5191ad6f0e92bf9524ff7353556` | `07808ccde23074ec62e72b787039295db6baad112ecd1f047f5b2769ae9aeda3` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-bin-packing-gap-warm.tar.gz` |
| `oai-binary-matching-warm` | `008c4a8a5d8d203b5fe355d4b01394a8dc5cf811ea337fdcbd934f73ef2af402` | `94d586d4aba1cff93070e10bf724606ac26716547cca2e5b361d647a57ef173c` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-binary-matching-warm.tar.gz` |
| `oai-binary-sweep-warm` | `fcbb687e5b2f6d964c7b2590686208804787ff9e6fb054d3422071d04199601d` | `250413b48cd877ddd0095839d214ba4cff10ece2e0d072abdea1692929326691` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-binary-sweep-warm.tar.gz` |
| `oai-bipartite-crossing-warm` | `18179ca79749f904895928e2a0e368828d90181301e11aba09aa1b7be121637b` | `a8b19edf249adc2f85565a0b7b9f362ab566ef189b91be1452572d4376854e4a` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-bipartite-crossing-warm.tar.gz` |
| `oai-borsuk-nine-warm` | `7b5c4e5817205cfcda03d1af4b888b89a74501f8e1d4eea8b3efbc248c1a9b09` | `319d8b0450ee50c591becb2663d8e026879429d7d02458d666062d2f49693620` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-borsuk-nine-warm.tar.gz` |
| `oai-bounded-recovery-warm` | `ec776031504c2c0b7833b07fa919fd822c4753e949a92e0b30ccad9bf4bb681f` | `d67a34191b54682b3bdacf87dda2be1c22e288f5449ac2e8986057802a316965` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-bounded-recovery-warm.tar.gz` |
| `oai-bounded-tree-potentials-warm` | `7cde3dd30fca6b733bc5b9710f8d4ee39893da346adbd17ebc28286fdd2cfc20` | `98c2e13e318cdcbc95cdab66a15c74c9551e3a3dafd4953af160d102e3439b5d` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-bounded-tree-potentials-warm.tar.gz` |
| `oai-bounded-treewidth-l1-warm` | `b59b46b23800b5fc1eb5a1c19450dcf369ba9ad42f2d61aad6192818b13b684f` | `e779baa6daa25aeaa68725fc64f3d33d4e2f8084cec90aed483d7d6ab8f86d13` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-bounded-treewidth-l1-warm.tar.gz` |
| `oai-brennan-sharp-warm` | `b9e0452df7ed8100c2a9e6433b63ba4d9fdf8d9f599abc5d3946dc98debab4ac` | `08916d114430d0e768c455250f0549f523ee52e312f0e9af13163e974edd3478` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-brennan-sharp-warm.tar.gz` |
| `oai-brennan-warm` | `0e4f7da72b9676bfa8615a7aa35e328e2f83c48844fb17616cbc20689edcf504` | `e34924191785ee56a24269a680c6a1bf758829da18c4fec2d486d46866c167b3` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-brennan-warm.tar.gz` |
| `oai-c0-absorption-warm` | `3b09690fbedc1ef9d3eb26ab727f732ad35ba50ae179b7b1d0b7ebf2beb64d68` | `1c473b81003ad203b9f0568644b69f58e169df2b163baf1a57ffcacd03a6aff5` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-c0-absorption-warm.tar.gz` |
| `oai-ch-obstruction-warm` | `f1f3eb9f34338431c2fc094e5615c0fe0ea41ecd78386a5d6dbd1aca54c99e16` | `3958e89b6c246a3324c20e2b2c97d9c1c77f74cb8e805db1efa32d76e11b8a83` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-ch-obstruction-warm.tar.gz` |
| `oai-character-criterion-warm` | `1a4a3c3fccdf3ed4222121ef73e24e06b62f1472af9f8e10a49452ba779a6049` | `13ecbfbfdaa0ddbee19fe58bed3cc4dfc153bd98195e4b37e24382d98dc4e9f4` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-character-criterion-warm.tar.gz` |
| `oai-choiceless-polynomial-time-warm` | `45de78adac8b69edf30e7a53abf33e2f231405f62f51d0566bea49bedea7cfa0` | `eb28d43c057149a3e9258c9b57bddc1629ffa160549323700eb66c5f85ae9d3a` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-choiceless-polynomial-time-warm.tar.gz` |
| `oai-circulant-hadamard-warm` | `0ffb8ed4a83ec18a7631c6ce39942b0ca9ae10890640bc9c27b1180a6ef4773b` | `263cc3652c31f503740b3a26edc8a2aa1fc22b5de6b33a35f4e2ec547d8764d3` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-circulant-hadamard-warm.tar.gz` |
| `oai-classical-on-warm` | `08de313bc6f676f951d07c3be4e7f45f04a55c22ade4fba2f30b79d3fa7f69ab` | `aac4e3dbfb64944cdcd97817cc39b9f7cfcd998f6656919b7ae73efb2eff2ecf` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-classical-on-warm.tar.gz` |
| `oai-clique-free-log-warm` | `a563c5cde41d813ae01f1fff7049d3c0ce27602c9dfd7da4d67a1ae98410ffa9` | `a4779762f6ffd8458a87f34eb37a4b17ed1532658e1ba90ffb0c1608a86f64f0` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-clique-free-log-warm.tar.gz` |
| `oai-common-bases-fpras-warm` | `31a9afc7555f52d1e8ac1a97b416a2ac8796cd9e487d4c0d0a219235c2003fc0` | `d08717652cfadb9694fd941c7ccabf61f37245e41d2b089cedb98e0f3deb28cd` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-common-bases-fpras-warm.tar.gz` |
| `oai-commuting-derivations-warm` | `e52acd3fc63710d6e3797fcf41cf28cf43c89498b0b08a31a49f5733cfdc0045` | `89980d6bb26f06a9d6e5fbcb22fb44f767d10dcb3535da39f34b453e25634eba` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-commuting-derivations-warm.tar.gz` |
| `oai-compact-banach-warm` | `3a5612737ed55487740505d1a4b26b10e715336a2a565a6d6b8bbc17b9650fa3` | `cdd33387f949b2f9c16f620b0afb1fbe749072fc7415af3fb0c488acc5676340` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-compact-banach-warm.tar.gz` |
| `oai-complete-crouzeix-warm` | `176da90d340464d5e227609af307900cce34d81eb9e83508f023d04f218fec83` | `3843948f48726efbce083cee58b5d4f8bae1250c4cb982ed7efd85ad41684fe8` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-complete-crouzeix-warm.tar.gz` |
| `oai-complex-cancellation-warm` | `a89603c307b9eb6170fedb62c2dcabcb26fa2863591fe84cadc88e068b8996ca` | `be8aa0df1505c333a587196e4b944542281fb14542905ea55e31445153c68536` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-complex-cancellation-warm.tar.gz` |
| `oai-conductivity-warm` | `e54c5fe92bf616b0a77affff0ae8cd78e6aa15b4b91c0dc195899a4b42a43185` | `f238595c997e9e4fe9de57cafd37b2faf7c15ad5107604df3b1fabc1063eb170` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-conductivity-warm.tar.gz` |
| `oai-conjugate-points-warm` | `93f76221c0ce4bc3df1d0a98c50b24edf023b529b41f8f4112b212fed67210b2` | `866b15e461f62755cc3f133f6056d992daa6ba393f418bbdefe404693df51241` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-conjugate-points-warm.tar.gz` |
| `oai-continuum-transition-warm` | `524aa2b280bcd531f843b3cb640648c303f657507f5c4f82bd4dd39f98533d35` | `d064aa0d83365e605175d081549190f11ecff3e79f97519d4e6017ea127b9b3c` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-continuum-transition-warm.tar.gz` |
| `oai-coordinate-sweeps-warm` | `f9de7d83ecd99c67d4cc9cce11a2e6b04790033c5e604b7e2fc7a20d1615aabc` | `e300db8fc0328fa92ca1e1e50bf1703043768b058f864474a9984c3a0dec55b1` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-coordinate-sweeps-warm.tar.gz` |
| `oai-cotype-warm` | `c948749240563590cac7f671365453dc6351841968ec90819d938729cac1743b` | `cc8b27768350631ec02e06a44beb5c23e317e661194c38768885443fc270f9d8` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-cotype-warm.tar.gz` |
| `oai-coulomb-ionization-warm` | `19b0c906ed468c8ffe2c5c24275d2c4e7bac1c3796f5a76ec5b1d56d02dfe522` | `0056b8b7ef982ddabda3fd5b4d090976ea668b5a176b9b738fe3ec0840f83c51` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-coulomb-ionization-warm.tar.gz` |
| `oai-courtade-kumar-warm` | `64d29b41245b78c5a90390d7e8f8af1f3b5bcaead8925bfb3750faa17059c714` | `ee90eda7c6dc649f4e6b3bdd065c6e1b414876d8247f537650a8d8224c855e77` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-courtade-kumar-warm.tar.gz` |
| `oai-critical-sk-mixing-warm` | `0c0b98e877f7ecefb510fc68fd12a42f5998985c496bd3657b3cbffdacde1edb` | `38ec633d2377cd8fb424d4b35c76c47217d9be9c81a31a8a1cc7a2449120de45` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-critical-sk-mixing-warm.tar.gz` |
| `oai-critical-sk-warm` | `1509ab61ccb1b563b8f6cb3a3699f5751d47b469ed5e77f63cc08b163fc42b9f` | `eb339d2db7152d5850552453cdcb6ece276ce45ee6412e9a6ce56615b5bb19c7` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-critical-sk-warm.tar.gz` |
| `oai-critical-z3-warm` | `c6323d7831eaeaf050420013092158e5f16d27f949df42380555e30aad059ff7` | `6a8d1ab620f108a0617e177e2f798d676a01355a8fdd5508c85abc507c4dbf90` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-critical-z3-warm.tar.gz` |
| `oai-cycle-decomposition-warm` | `9493cf023aff4b7db6b9c8ad2907e18369fe174a62aff8da4cc4ea16c8555593` | `01f917730ee1086f521cddb34434e82cf82f29af4e5375b507271569939db8e8` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-cycle-decomposition-warm.tar.gz` |
| `oai-daugavet-moduli-warm` | `e75c0cb03b036920e1e7013b4b6841c8b1054f028995f77375120745930c12c7` | `c0e2e1a832cdc27f36be67a5112e55019beb2664ea29b2edc0f7bde8b7177c28` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-daugavet-moduli-warm.tar.gz` |
| `oai-degree-rigidity-warm` | `62a29a4a93ae1db60d8c3e236481ea0d3f4336278d0285550c1288e65f1a70d8` | `4106235b794d8f26fe4aebd5fc0d2e53efaa4d6308dce54b78fc5728b9c5c353` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-degree-rigidity-warm.tar.gz` |
| `oai-deligne-drinfeld-warm` | `731d024ba35c1609e505b1771cae89d53355e97e8962c8efef1181bac621efde` | `fd28b373c5128432b6a43d87230d536bb8e9b168fc399dc54067ca2e19b65aff` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-deligne-drinfeld-warm.tar.gz` |
| `oai-depth-three-warm` | `cb5f30d778e0b4c4632f9a5b38b6f0c097c970325b62c902f8ff1c7ac209081e` | `254a16a305592a06f87a51f690d2978bda16dfae76b044dc15b48ef8316017d6` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-depth-three-warm.tar.gz` |
| `oai-diamond-distortion-warm` | `5fe6549c6ef37391617c93f648d056525f3635e8f136ed6e4d208ed2d4ac4263` | `7e3dc6c60ab4caee467ab323d8befa0d6379d8cd26f22277592ed2d855f0a660` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-diamond-distortion-warm.tar.gz` |
| `oai-direct-crouzeix-warm` | `2981af18d7fd46d3825062554ee54c144b03482a285aa638436e6d821b5b6c7e` | `1cf47fc3dfefc3fe124b72c24b968db41482c5c5437150236bf7e9647bb9d086` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-direct-crouzeix-warm.tar.gz` |
| `oai-directional-ballisticity-warm` | `c6065261ff283a7ff36728f513ee30496c4dff399f6e4420f84d54d9db9361b8` | `548cb08a63e95d485921f62318ca8a011fca7bb63805dd09fbefe25494d00f36` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-directional-ballisticity-warm.tar.gz` |
| `oai-dirichlet-seven-eighths-warm` | `91cdbea82be97c99633ac891c79361498d6805def0e19226dfba8f9c553f2d6f` | `59c89cc9304110454a0bcb3f06a73bc28c78e04435eee53f897554e6b917e8d2` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-dirichlet-seven-eighths-warm.tar.gz` |
| `oai-dixmier-all-discrete-warm` | `9dd26d1e46cd06c7d53c8ea7236746c0fdd4a6fd3605179900ce82db72bf2cb8` | `b386323c77710e752fc27d01444836977fd88b8544f7f1694069a4c8890ec2f2` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-dixmier-all-discrete-warm.tar.gz` |
| `oai-doubling-hilbert-warm` | `5769186ee7a770295565570415724a1b9a5bba27f40e21295f5429625b4a6906` | `847feec2b30869e6ffbfcdbfdd40b7781cf01289435a1ed4efc8a22c979f5d2e` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-doubling-hilbert-warm.tar.gz` |
| `oai-egyptian-fractions-warm` | `d8cf8f34ab87116b49b4f7533de9b2f30d87d1a33f183f83027fad8eba9ae8a2` | `7e8d10a900f3a3fcf8ce2ba331bb541fb9d575b8fc2b518653cd3db764884258` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-egyptian-fractions-warm.tar.gz` |
| `oai-entangled-games-warm` | `6d1ffae81b188d7a7894e203507fd191e8f3e42452cfe4a37c0529b7dc04bc94` | `7ed0e13016c19b8bcb098fcdd59a6979260f7c56ab8b2c149a353305290ef43e` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-entangled-games-warm.tar.gz` |
| `oai-euclidean-ramsey-warm` | `b0db9ada93cfa0d814f2378b95d163ba6ac580d690517b7df3f0cb615b8f417e` | `9303bf0f3155683e41471e0d07758c7132ca46bace9ae9730b5064095a24acae` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-euclidean-ramsey-warm.tar.gz` |
| `oai-exact-fourier-warm` | `9c9decbeb5cb92b13c72e6ff5469c6071704fc32671e18d0ce96508a210e4c23` | `e8ca0acf87679340b326e12fdeab7aba80906483821bbafa8c823fbc26c6edda` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-exact-fourier-warm.tar.gz` |
| `oai-factor-generation-warm` | `ce53c14c506f46517a838754a074d904ee912fd3d6601685cbc18bd76505dcb0` | `da399b4cc6ab58a169dbbba7a38d7ced958ba138597dfcdc8f7b55629134671b` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-factor-generation-warm.tar.gz` |
| `oai-finitistic-asymmetry-warm` | `e7e2ca27f932b1b3329979595a52c6dc2295bef52c9ccca715c2ba372ed9a22f` | `c086e6acc8c91d27e2eb7c99215d00d5a47b0d17fcf63dbe9a5426a01da9f19d` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-finitistic-asymmetry-warm.tar.gz` |
| `oai-forest-space-warm` | `c7f3b623b1613a5170dacc74dcc07d913c14ba330c2531d382829ec58c34c225` | `cd37963bc26e42bae354eb64160e16a9b03fdcc558db028ec7fd55e86f11eb10` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-forest-space-warm.tar.gz` |
| `oai-foulkes-howe-warm` | `106414bf5c188ad11402ad45d9c5c83c1071f12a26ffc6ffb6ef4c526eee0bef` | `4f7b40948ddc7a71569ae171ec9b70b054ace132b11c36478662a20a83137627` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-foulkes-howe-warm.tar.gz` |
| `oai-free-ising-warm` | `27be7b73375c7bdaa99b220f3aa515d3afe784b0a12037ced0e1fe19787c1353` | `c2f10a063c14d69e5f1979dd54e51c9881da8561d8fc91ba1fa43a354248ab88` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-free-ising-warm.tar.gz` |
| `oai-gaussian-moat-warm` | `c218fd769b66f67f458e58a51ecee82a0d7662353a04d7387af93efa46788463` | `c116779955441da39cbc1a9815c590d5801d8cf34f0786350258f705101a194d` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-gaussian-moat-warm.tar.gz` |
| `oai-gaussian-propeller-warm` | `79fd91582483c391fcdfc975f2d0c6b4dd6d354bcbe0e4d3895787094fa809c0` | `10ec5729377b79c08055942996a9916d52cf1fb82625fceff74293ea8db881d0` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-gaussian-propeller-warm.tar.gz` |
| `oai-gaussian-replacement-warm` | `3d6e9066316bf85d86cdba28c66fbe1edc501e01ede193b3cea84a8969766da3` | `5cebaf78cd8d52203798cad5f73a62052e6b599f87b17c4a008bcd6f886ecc2d` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-gaussian-replacement-warm.tar.gz` |
| `oai-gotsman-linial-warm` | `bb1d601f031cb50319bc8b6467f0b3e4576d18e68aa59ad2d26ad5cccc8681ba` | `dba2698c5bc03c97acbf24f958c0c23f90eca9f4660ec3bf868fd3061f669f09` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-gotsman-linial-warm.tar.gz` |
| `oai-graham-spherical-warm` | `b40ddc27e0badd850c64b1db7d56b7d713977297e2135a1f183e9fe7975b8dc1` | `74ee69689106784d4957372045a583e08a2f7a813cea8bd3c7320ca0dbb33668` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-graham-spherical-warm.tar.gz` |
| `oai-grothendieck-elementary-expansion-warm` | `08d658331e75020bad8fb1d785eb04739e88095abd53850bceb8eb1b973a7070` | `fc4563f9300335e80738ea3fe427d83278fc60d81021402b5b5d26e11193bb55` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-grothendieck-elementary-expansion-warm.tar.gz` |
| `oai-group-ring-determinant-warm` | `c30862ced9480c04a3d165b3cb9a2b8a9bd1595a74c4d0ecb6af21bd413ed7ac` | `ad0cbe309a9361a2e662f1c913450f537b197ffb57b62aac5f2e974a25b41844` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-group-ring-determinant-warm.tar.gz` |
| `oai-harmonic-artin-warm` | `b87ccb234ba03d0f7ff058ff45a6868e776bc358e4d1012d9c75ecda16f3a6a0` | `4a3d796af447f6f146a22353fa85ed7be7bd84d60112d5ae96b1f24581871e33` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-harmonic-artin-warm.tar.gz` |
| `oai-harmonic-growth-warm` | `bce79343ee2074464eab40d7374ef6e97464c3a1366a0d5fbc055c501896aa2a` | `0ada80b48932e1d4957af543abbe4cf625a7850307e3310c97b5036ddae0f274` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-harmonic-growth-warm.tar.gz` |
| `oai-hecke-seven-eighths-warm` | `20668aa1ecde45bd8e2d70570d82ed85ad7f1b827bbf0a5825bc56d49cceb937` | `83913336f30f725723b700fd19403deeaf3c831584c3dad6db898f2f7c07ef8d` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-hecke-seven-eighths-warm.tar.gz` |
| `oai-henon-emden-warm` | `49ac321ac4e1ce7c4ce1b1461998adfaf6570003c0a70edd7e6ae09af2e4c2df` | `5a21e86a51013cfe62bde0ec871b71401ad0abdf0783955149147fd6bca0629e` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-henon-emden-warm.tar.gz` |
| `oai-hyperbolic-cones-warm` | `0f91e10ba2e6acfc23bbd3e681b71ef9168888262fcf1337673d913440e76dbf` | `1d800083625e6ebcfc674900bd7cbb9d9f62edba9281b42480eef035429d60ba` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-hyperbolic-cones-warm.tar.gz` |
| `oai-hyperbolic-obstruction-warm` | `70283b34a42b90cccf014789d45d20713410c92505b302c788f2cbb30074dd92` | `1bb39fd2bf539e2706d560e933912b83e9671c70112606bc126369f0420a17d1` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-hyperbolic-obstruction-warm.tar.gz` |
| `oai-independent-products-warm` | `0f59efd194731f0508039ac59c6b3431400fd1770bd5e75e8f43520aab3299c9` | `b0133f8fe80db5a140a15c2372127a0ed9bc6870cd80c2faac6475e047257f9c` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-independent-products-warm.tar.gz` |
| `oai-independent-sets-warm` | `fdfe8be55a0ca796e608546e21f816ad6d0afb0b7936d4a5fcd98d7a81566418` | `4fda3b615212acd017c7b13a1ee20cd5fa2fdab8704472742ee05feb1d5ce754` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-independent-sets-warm.tar.gz` |
| `oai-infinite-matroid-warm` | `f854980d4e5ec48b39c23f78f64da2ecce251ed925b9ed9f6cad62a8b1808516` | `45b632b85e58843ee30787774d8e4af7ce0d5cae030042a27e6978820e0d78ce` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-infinite-matroid-warm.tar.gz` |
| `oai-isometric-immersion-warm` | `a88918eabd7321728a7d74e05923ac9e91f2f2a915c9a5ddf66c3caeaf66c2ad` | `b755c1f881758c1a63865ecac5c62348df52aa9029fc94694fbc9ad47a42b765` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-isometric-immersion-warm.tar.gz` |
| `oai-jacobsthal-warm` | `aea19beccbb9c69a577b237cc797ba9d37d5110b53191cfde7c166ee980f4203` | `5dfd7bc4e8e85f79c0f0e1aca058e89160ef24e063a6d8b3ae0d883fd3b2448f` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-jacobsthal-warm.tar.gz` |
| `oai-k-median-recovery-warm` | `7806876ffad44f58b4d77f19dd316f5293a4e64745e89e4509f9aa7486180b18` | `9a05c150327103082954ef524a2aa6c346b36c792ca7625342d02272347970c9` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-k-median-recovery-warm.tar.gz` |
| `oai-kahler-splitting-warm` | `1e2cf6c9ef1a87df1b87fd38dfb5f5747a59d4b5eda4c784ed5562895608c3b2` | `ac80ceed1c540ef9451a82d5e747db9c255eed6d068ef42939085b11bc622306` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-kahler-splitting-warm.tar.gz` |
| `oai-kaplansky-finitely-presented-warm` | `e04518b4723695d74b90589e8481485be2ef7082c200f7cff8f45f851b47a9bc` | `15439f2921591740009d7ce05385a7c90899169987c0133f8cabd07a3734254b` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-kaplansky-finitely-presented-warm.tar.gz` |
| `oai-kaplansky-quasitrace-warm` | `6d90bc36e13a87dc8519be590e8c550671d220df25628259979c6e831e873a54` | `2b02570d909b3e1ce917d42bb30229aefe9cd1670b5e88ba0e7a04c96769fdbe` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-kaplansky-quasitrace-warm.tar.gz` |
| `oai-laughlin-warm` | `d5343dfe877b6192adbe71adbad622d53b12afa32be41e1f465a1d6902c6bf4c` | `631adc33e03c671074f92a4f53eecebce25793fe7c5c74f982c8e6ef5c991a1b` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-laughlin-warm.tar.gz` |
| `oai-lieb-thirring-warm` | `da186eb66caa9be117c9a999e29cca8e0d1f9a8e1206affb8a15661c4c9fa49d` | `05daa12a89685756cf59baec7cf2ad5c8b5d5bd4c97810b3219e3a7b3ef6b6bb` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-lieb-thirring-warm.tar.gz` |
| `oai-lipschitz-equivalence-warm` | `eb112ae9d1d8351d8adda3e95ae8bc49dabc838dabd6a9db05f9986f9386ae48` | `bb73483810f8095289ce263b6cddc230916c8cce227d9ade38985020c8b773ae` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-lipschitz-equivalence-warm.tar.gz` |
| `oai-little-finitistic-warm` | `ce76d2214bd1deb068e9903b4b73024fbead021c1ef3180a4fbb99a54beb1255` | `ea0aff361086d3e413ba38590e2394dc253095eb008335f77ba475377963da86` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-little-finitistic-warm.tar.gz` |
| `oai-log-brunn-minkowski-warm` | `eb79ec83a4e5c83c53e8a7ab8a13ada26749625607c55cf9609c5debe50ef7dc` | `76456280f242f1cefd438d81decfd1a75349f5a37a733b60f0b04f8407fa39e9` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-log-brunn-minkowski-warm.tar.gz` |
| `oai-log-concave-query-warm` | `be4f269b9e91e32f55e0fd32b886f6cbfb49630cfda7e571afeae8f0dc107256` | `4a619e2fe5f935626a11b8b8ed6a62040da6a428e424d51f13cf33db60d597f8` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-log-concave-query-warm.tar.gz` |
| `oai-mahler-conjecture-warm` | `562ee69431dce3edb0d242ef2562fed33ac0260e4f0ce2eb7b37ff6631a3c1c9` | `c5a7af6cb1d5c0070ad82972b5121faf8e82917f47f9168e6f81745ba4956e09` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-mahler-conjecture-warm.tar.gz` |
| `oai-markov-type-warm` | `bc61eebbfcdb62625da4ed155f491e78063e3b08311c0fa1178f07edfbd583ef` | `220b3fda91b5ac4b4911acbe91a953dd868b31279618467b17560b3d5ff39686` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-markov-type-warm.tar.gz` |
| `oai-matching-entropy-warm` | `961e6048b74f2c8ce97445442fec2ac9f400b1e25769f1dfae1ddd8fb45db98c` | `149dbe7c3465b6fae3e69f0d02cae4db40db4495de5aa98936eb4dc878fac401` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-matching-entropy-warm.tar.gz` |
| `oai-matrix-fields-warm` | `a46e477f381db0e9e45e0a683b700a357e17552289661cda8387a201ba16e251` | `ad2baad4d5dab54ed055f85138f6093499765a44ba1fbe64971475b989bb7f59` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-matrix-fields-warm.tar.gz` |
| `oai-matrix-multiplication-warm` | `f4fedc15bc35d66471bde119fa29c989e83901c96de0ed569510716e8f4fb316` | `990b751c69710bba39f97781fa0ed80a41356059850ab29be6b5188d1ab1fec3` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-matrix-multiplication-warm.tar.gz` |
| `oai-matrix-removal-warm` | `57d356ab1e077d957b3ac390103c38d420e6f433a20dd6f0f7f8a34927723b69` | `316f86cbbdd0d7895fde92f8f42db85072a23d52396f7aaa3ab784de28df9233` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-matrix-removal-warm.tar.gz` |
| `oai-maximal-seshadri-constants-warm` | `03c42e4e63e342ef4f4122baff76f50e5cf61e406b6848f6416df24c1f4ea4f4` | `d352a5d3b62b0e308a890adc673442843f0e0973617359911b48fee122ab6737` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-maximal-seshadri-constants-warm.tar.gz` |
| `oai-memory-precision-warm` | `97c58d1564aaf2b431d94d9a453c7280e4b98d9a66050e76a7cb4dd5162e8aa0` | `e14f851c5f0ae2d3b9a66569d9084d4d91b1eb93147c70300dcb651b0e2e4783` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-memory-precision-warm.tar.gz` |
| `oai-metric-entropy-duality-warm` | `1ed0874d2c7ee6077dff2b3588fd031e972c53ecb711672002a17a3f770607f2` | `7ff75632052eb575710458594baa7bd7fa30188b6b981b06d72f98463600f4d6` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-metric-entropy-duality-warm.tar.gz` |
| `oai-midpoint-lenses-warm` | `08ce7051d9cdd31e4238601103113a240392269035f3393cf14b7dd7db13d0f2` | `20516225c727fb8803690fac9dd272d32fc92da997e4171c037dc1b3215993a9` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-midpoint-lenses-warm.tar.gz` |
| `oai-odd-kaplansky-warm` | `7e2c585cd247918121b1b2315e46ee7eb8506540d5a56ae191b6d98b4ef406de` | `81d3e15871bbb620478489723c7811de85268bebdfa76026461210aa7e584e17` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-odd-kaplansky-warm.tar.gz` |
| `oai-one-way-liveness-warm` | `bf82092c5ff3d4426d81ddee815d8ea347fc85ce89b0a152be676b38a95e6d4f` | `47a3bd4958cdb595457169d843674fca7498a252e853ad631f98230d266bb14a` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-one-way-liveness-warm.tar.gz` |
| `oai-optimal-max-cut-warm` | `24468253cfa5bddc250f99ff1881d77041960410f7a5f4c7a8e6a07e01cee208` | `d9c0cfc17c8ad7c14338f066a575d1c7a57c7aa07c859080168b0667a180cdcf` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-optimal-max-cut-warm.tar.gz` |
| `oai-partition-principle-warm` | `eb5db04f85a69deaac48cabc13e9baf8ba359672d8bc8e11189170372a847fbf` | `90f69465ad2c6b5a696bd077a046a1933d9854a42890e1386ae3ef74dcdef0c6` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-partition-principle-warm.tar.gz` |
| `oai-perfect-completeness-warm` | `b688c63adfcc42d64c01864f396116379f291bca289f2ca183335988fe991869` | `24aca7508cf9bac7bc9870d11ef92265cd55a4ba7e4cb473a9d55caedce9298a` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-perfect-completeness-warm.tar.gz` |
| `oai-periodic-tiling-three-warm` | `7d2644f24bb6afbe01b6218e15c83dd8c8ea98433009eea1a9f0d5a8de113888` | `d78be7636a141f2a26ab894c3055fad54699220b5955000d046b391a17440bcf` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-periodic-tiling-three-warm.tar.gz` |
| `oai-petty-projection-volume-warm` | `1c56ffd82200288ac2bef78e3d1113c80cae15c864f049f5fcd85b89317957a2` | `764bfe24c26074db621966baaf0113613afa45a9b548d2e1a00d7eaddfb28fe6` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-petty-projection-volume-warm.tar.gz` |
| `oai-pinched-kahler-warm` | `edea9133c497909ef61fa32c2a9d4abe8c0c5ad03bacc76ae2e18043de592f95` | `c31ab18860dd436e08c66517bf3fecfb18791abd9f29473ac7fa5d897545a4ea` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-pinched-kahler-warm.tar.gz` |
| `oai-pinned-distances-warm` | `9f6f32f79ac1bc07048a63f9d79afc1a47244ebf040a571b87e10606b7a1e617` | `d7c248e6fb44c7bec9ab36b5b477a219c9262029da808919534e5a244d17bc17` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-pinned-distances-warm.tar.gz` |
| `oai-planar-falconer-warm` | `71cc278b6ccec3f58c5fe400194480f9fed13853fd6fd6188b07f2d8d52f4fee` | `a4dd2415f0c4a2b20077b34171b10ef23085f9c53e237e237f994e40a43bb8d6` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-planar-falconer-warm.tar.gz` |
| `oai-planar-first-passage-warm` | `ea5552c32f11970c6cb76888823277ab563c1d4ef95af58c16d0898d2f162c67` | `1a2ebea693f9c11fdd71439a8694227d0bd416d1e1561de055dc9166d9366a10` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-planar-first-passage-warm.tar.gz` |
| `oai-planar-l1-warm` | `fb24e57aab17e1f20919d98cd4fbf9e8243642457e4df8a8cb5a5b314fb98563` | `aa5411db7c17a5a82acf7512899efae273668154bbaba33ded3f6ee4aca51473` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-planar-l1-warm.tar.gz` |
| `oai-plane-coloring-warm` | `c2e1bd675f6c943d5280d70110984979d71a217e82fff380472273e87e6f2d5b` | `1f1471d04bdeb2906cf86f374207f2a28dfed4802519ce6214c6bf19666d7d38` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-plane-coloring-warm.tar.gz` |
| `oai-posterior-replicas-warm` | `efe869590e72f0b18e62014967d111d04e65b9542404615738e8f8191f553ca3` | `4a61399c7a86bf7103f4014126b96680bb2b01bc2de6c37d17f659d949e2f5dc` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-posterior-replicas-warm.tar.gz` |
| `oai-power-free-values-warm` | `8d897396751d06fb7699b9d828a7f01dc4356b599434ceb0c46c02b98084720c` | `c5c1dc5cdbdc8ff4b2d71510cccff4f126911e08bde16583e9e38360ef8a33b7` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-power-free-values-warm.tar.gz` |
| `oai-projection-counterexample-warm` | `184bedb56844c8694487c7b90601cc01a3f643ced672e9e5e589d516a0a8b314` | `df128fbadc7752e76120c88b7c6e49da0b5544feaa5244b6d4ed53921ac26757` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-projection-counterexample-warm.tar.gz` |
| `oai-projection-moments-warm` | `b442d923386253c0de9872c13c7a12925b58e55636a702472632181fdc920def` | `7fc292a58dfc03c0f151d1ab2184df385c2c50d7a513489d75e01c5d83a3f7d7` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-projection-moments-warm.tar.gz` |
| `oai-projection-volume-warm` | `29320ad87ff2fe3cdf1cff9968b53cb9b7cceb776491fad8df0b10f6c9ac9bc7` | `0c6639b4f365e19a8a1ac7e01d8f742160ccb21e0a1b825582a38bc20b8f4805` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-projection-volume-warm.tar.gz` |
| `oai-qac-parity-warm` | `e8b2e9dfdce2a521d8dc06134707233cf6160cb25203e6b2d41fea85e7969c8b` | `cbb13c8547f44ee530bf3ae7bdd8ca9137fd30b82474c58266e5e4257cf30ccf` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-qac-parity-warm.tar.gz` |
| `oai-quadric-bundles-warm` | `e49cf7d66a8ce36fa58745397fd0dded0a401d6dbb696ee03aa53702e215d1bd` | `9fbb808062ddd7ba6db41c9c427f5757cd401fa0efcc0723155b193bf342c2ec` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-quadric-bundles-warm.tar.gz` |
| `oai-quantitative-van-der-waerden-warm` | `98d5dac8db5a74927a8e56521be72ad16cb2f367c18f8e458a89c1ec39d26509` | `6cd9167537b481f46de05ab6548b870cd4c26be064e8be4e0d8d5bac1a016332` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-quantitative-van-der-waerden-warm.tar.gz` |
| `oai-quasi-riemann-hypothesis-warm` | `25b108e727570590450388296af3ad8608b5835d1d5b766bf5a53e61c3f5a4c2` | `97e956f4157ec73b3e1764d1243976c1652b38b13a0acd37d541249ffdad9b80` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-quasi-riemann-hypothesis-warm.tar.gz` |
| `oai-quintic-lienard-warm` | `31b5a68239afa11efe6b9007978e5ec2a98b218d93a1f1ff105fcde5ce9e1e3d` | `f9e5c99ee542d7e7c7da060611fcefcd16ebc19c115d6e864856bc4715a0cedd` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-quintic-lienard-warm.tar.gz` |
| `oai-radial-transition-warm` | `60f18bd95b75efa78c29eee4fec75638c726922ab0702951c97bcb8d22f3c6c5` | `607eb0ed413902d0c0aab6024f1c93bf61d55cc4076a360f091a27fe215c07db` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-radial-transition-warm.tar.gz` |
| `oai-randomized-mean-payoff-warm` | `4aa14810edde314c493481fac2f64a64aa80e31afbb4ae8ac6990db7bd765fa2` | `c488c31169a4082a3db261a7cad2b3bc63afa1445c13e27776e207131b0b1043` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-randomized-mean-payoff-warm.tar.gz` |
| `oai-rational-hitting-warm` | `f31ccb3c18b2f3141ca2777069b66779ba6e2d077b720ef4ab0978f57e3792f2` | `7acb648d795e1e546257da05a26f79e20c471e402255a6f935b35745fdf1e6ef` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-rational-hitting-warm.tar.gz` |
| `oai-recursive-potentials-warm` | `c07ab468dd42b55d2f89d4424c7e0d6a1510ea00813c9b84ab5487fe1817ffe8` | `60b752402c6acfa2e2f02e90a7c278b2e9ef344c3331609df75fa2a39b77c62d` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-recursive-potentials-warm.tar.gz` |
| `oai-reflexive-fixed-points-warm` | `1328de60731c48bb12dc0c6311645d3f5d24145132d8717755b28eca4d412136` | `b2482d39515e6355a1bbd146d790a8caa133f36cb73d8e8cbb72d42084addc60` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-reflexive-fixed-points-warm.tar.gz` |
| `oai-regular-parity-warm` | `34cf63807c3560539bbc6b2998aa44364b2e1148095cf1920c09cb133f0834b0` | `1dd43dc5b2ea1bf87ee28b5ff9b0514ec34d03afc120833851988380554c6bf8` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-regular-parity-warm.tar.gz` |
| `oai-riesz-quantitative-warm` | `daf3c74e7cb747735c3e1c9328689a847ecd0d89d2279e11e4c19781abbe91d6` | `775a82c33e5f29916466b60db29214a497ccf1b5df7af16aeeae5ba931b77a5d` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-riesz-quantitative-warm.tar.gz` |
| `oai-ryser-covering-warm` | `90c836fc7106586ecce362015390264dc564990e0c4d3d62a125852c585cc7b6` | `c514e2531befb4da24f348e0d241528086072a7d3a53e676c79ad5db6974cdce` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-ryser-covering-warm.tar.gz` |
| `oai-ryser-odd-extensions-warm` | `85fbba165a43c8e33a520c3fe423b595c64f7dee1f0abf4e6d93de9162f02b81` | `af845b3212494d71c627ac2266332bdc8a1dbe2d28300e769c30e070ccf1f05c` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-ryser-odd-extensions-warm.tar.gz` |
| `oai-saxl-warm` | `54b4444b6322a4a4e3146f092c6143e755e753b7e83f0a22ec08c2fec2a5963c` | `c19ed1af4fdd951b1f7f24ff62dfcfa304a96ed5259c46cba49db3f1ca716ef5` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-saxl-warm.tar.gz` |
| `oai-second-kahn-kalai-warm` | `6d6d2dd9ded2a42e8bf39f36de6ddf1f1cad492f87fecd89a50e2d678b6bff1b` | `618f0c3d98c49e2334d5877b69d9ca6d381d0cc910a4c1e4ec6cc6d604a9b8ba` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-second-kahn-kalai-warm.tar.gz` |
| `oai-self-similar-warm` | `f471eff59d436fc60d38f21497a0dafdf7a65e293f808cb1d6b35463f09ca209` | `6ca42ad06bc82db5cd7b8ef4cd22b513e1c51bd4044fbcf2a8264a5de88dee63` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-self-similar-warm.tar.gz` |
| `oai-sensitivity-separation-warm` | `7c515e922d196b0b3c285d81f3460646dc75e8100aa6e69cceec70266d94ec00` | `25d854c8f66020fea131d2c13ce6d1d24ea24b253f9db5124b6b24f681bea114` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-sensitivity-separation-warm.tar.gz` |
| `oai-seymour-second-neighborhood-warm` | `7964481956cf0b700aa417b7ccce3f88ba08a6dba8f988dcb3f9332d103ff705` | `599048f1bf366443b3a5600d59d1998d9ea6a1675e6a9f8f149c7deae206cc9c` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-seymour-second-neighborhood-warm.tar.gz` |
| `oai-siegel-zeros-warm` | `fe6a7d00a78b0271353a90c661f47c54577d40882b5f1f63f8e61fb382342dd7` | `8a99ecc6ec91c19b1d2ac8c8dee6b52097a36da08cd2c574c5c79d6afad182b3` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-siegel-zeros-warm.tar.gz` |
| `oai-signed-finite-band-warm` | `02be0919098973cfee0e9b1370ca1c05eb421801d5fde9ea8d4f6b81fb1b6728` | `05971750c27031cae2803ee66bdb73e6e0ad65dbe2170688b2ecd6c956f3d689` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-signed-finite-band-warm.tar.gz` |
| `oai-simple-amenable-warm` | `c680947f0d9ee31c9c99a353c66f813d84db1e0bec4ef27776914f380763f8a4` | `c26f805f5b3cd0f87084151a35a591981fb214d9c14dfda799aafabc48760b18` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-simple-amenable-warm.tar.gz` |
| `oai-single-fold-warm` | `15d7d0578a6d27b3d45d1a7d0b672c9688412aa78adea95c928bd78eaa9f06af` | `3638f245c1101779f5a3c5a5297ac171a45df6108a5f6f7bb157189d18a04d67` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-single-fold-warm.tar.gz` |
| `oai-single-lattice-covering-warm` | `59f10f7e4a46c7238bf9031d8386f2fd2f28bad52a256f6d8b4adf7b2cd7bd4b` | `7901c27523e7b6174a01d5be5876a1ff1eee488be3082831d6600bffe559935c` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-single-lattice-covering-warm.tar.gz` |
| `oai-singleton-loop-matching-warm` | `c8de4d563594a2ec4166919f1adfbdfca888607c4dc19d9e67ad8811e1394083` | `6e7acf61d6f886eb42fd7fdfb51302b4297717d982e025bee11e46468891995e` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-singleton-loop-matching-warm.tar.gz` |
| `oai-smooth-yau-warm` | `98921ffac0643b027818669a5d79b29907045bcd3f3ea3697cf7a41739a417ed` | `df9c6ab0941df7a26466a3ab65c60b6f87a1377d9e8915fc81fb4c970f47522c` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-smooth-yau-warm.tar.gz` |
| `oai-steinitz-bergstrom-warm` | `688f2d96dbd47983d1ec7e70ca05cff1b50c573325a9a570af20a9aeb2e8e68e` | `b4104918a280bad2e822a5ef432466df19dd04ec277643c3e794c165f431a31b` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-steinitz-bergstrom-warm.tar.gz` |
| `oai-strict-means-warm` | `e57ed151903d4d351b129ce85539554ce0acb0005cda137c8d61e55103db9fbc` | `f1ede6380222959832a82e388c6190af49fb81f2112aa01ddfae4e375c0738ff` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-strict-means-warm.tar.gz` |
| `oai-strong-thin-tree-warm` | `6271b0e6c3f4b026a92f395bf24349f74191cce3f5d75801c185f8456468c44d` | `e374d0b8c038eafa6919055bebc73a292606f72ca03d3151c7bb6c237da3279d` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-strong-thin-tree-warm.tar.gz` |
| `oai-structural-crouzeix-warm` | `7ee5b2b9d5176a61e03b8b80901c618fcf0b898c7d0831cfea5befb2cb6263e0` | `5a20fa51ae19036779da48ba88425dd246fe7afd327ff9cb305a3016999ef0c8` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-structural-crouzeix-warm.tar.gz` |
| `oai-subpolynomial-lp-warm` | `03fc940c9c4014773c77424e83010114e78670f7f509c2a1d9bdf3009caa2673` | `68a6f017ef2fc6a62eead78d4177b23a637c40a05dd946fa4e5fdf60cb84952a` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-subpolynomial-lp-warm.tar.gz` |
| `oai-subsphere-current-warm` | `dd3f868feea90036e8832a2fc262887fbf5ec4a9322823d89c0c47c90489dfaa` | `eb32f0f5b0a1204d2a68fbfb514661e8bc772cb744ff9a070286950e9eb45ada` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-subsphere-current-warm.tar.gz` |
| `oai-superstring-warm` | `6d912313d2e1f7bcb6d801ebb029d43012b20b0d0b20f1fe456788e6dc51b746` | `4808fb69abdb9414e6259159a8397f7ef20dda67217d33c789a45535e2bef318` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-superstring-warm.tar.gz` |
| `oai-symmetric-domains-warm` | `7f49ee521b42da9db6dcc4bbcf9c19fbc3113abf38d6ee7faa6bcff0f0cb85e4` | `ea2cde0d46ae2d3bdfeeff69141b2c8390ba194590d2eb00a6a3224e9e180afa` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-symmetric-domains-warm.tar.gz` |
| `oai-symmetric-mahler-equality-warm` | `81179c6a81852a06ae43031df11ee551b53492f8ff24161d9ce4482f5dc1cb49` | `f4705ba3b77c604db38b5d984d187ee87d0b25e0e444492941a7b9ab5a29a966` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-symmetric-mahler-equality-warm.tar.gz` |
| `oai-symmetric-polar-warm` | `ba07655c69a860e1f4123efc0921a1890b9d309bb35be22dcb67c28d3610da5b` | `65cc0e66cbacc95085ed216c4d511e670a97ddc2b146c118501607409432c37a` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-symmetric-polar-warm.tar.gz` |
| `oai-tachikawa-warm` | `f68eea48a2718cdd52808496119fd552936eada11977f6daf80ca4cf75b4a3ea` | `b047abc4a3f5b7ee529e47f9500f611b7a15ba7cea5cb99acac32b12aa1a84f4` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-tachikawa-warm.tar.gz` |
| `oai-talagrand-discrete-convexity-warm` | `5650daf2157e7ef6675d4a32063c8c8298c0e80359b257e673515ac20c8c78eb` | `3771161e12f0595d65d90983fac9d4a9c7ecda3c8ae1002a309eee2bc3feab0e` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-talagrand-discrete-convexity-warm.tar.gz` |
| `oai-talagrand-expectation-threshold-warm` | `0b32662b64e7a378c04032d0354246e94b49d6bbd9562f270271d567b9ceb8d7` | `f0e8d57dc88a52af2bf29b9e136369e04a87197f0b4febfc0501fcc30b204338` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-talagrand-expectation-threshold-warm.tar.gz` |
| `oai-taming-compatibility-warm` | `0b4b5fcfd811fc2e5adc7d90672ebedaca3121aa6fb640303a9139b320435805` | `4909b9eecd8556c124d6dd3b5275fe13684f30746973c2d1ec078dbf60ae0744` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-taming-compatibility-warm.tar.gz` |
| `oai-thompson-nonamenability-warm` | `f20a3e719044209b21e238bc80082637b99d705996e80940a7198586a3e8a4df` | `f427adee19474c526704d5840d2bcd598b11692c4064ef5ba6259db0bfa0274e` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-thompson-nonamenability-warm.tar.gz` |
| `oai-thorp-routing-warm` | `a97abee9c406fc5a21e0be0bcd586f5528769c0cd2da53cb39cb2a48236098ab` | `f08e44878f1253a2d5ad567b88509c638adb6741bae7371bf7112411ebef1d8b` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-thorp-routing-warm.tar.gz` |
| `oai-thorp-weighted-compatibility-warm` | `4d8ca9a975bf038bfabcaff7ff0fe54e38040bd56d2d58741df0c98a837be3de` | `df7e931c57df19a352fc9dca8db19c0fdda4000302af77cdd586b5b14777f5bb` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-thorp-weighted-compatibility-warm.tar.gz` |
| `oai-tingley-sphere-isometry-warm` | `196987269286ea4ba9ef46b8f5447f471827e74a98095886437d14aeedd8c1f6` | `6f63afb864d79bc962ba48a60f27b740a4f8269c81ed635ad722127d0e926f4e` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-tingley-sphere-isometry-warm.tar.gz` |
| `oai-torsion-free-hyperbolic-warm` | `c1559da0def24d6adfbe98df1802e98bf6944c9da5e6217bcfc264acbcb6a531` | `c867034fc87aca5eac663c4181b68e861ff7b4eba7f296e78ae0e8a6ee40dc34` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-torsion-free-hyperbolic-warm.tar.gz` |
| `oai-torsion-free-zero-divisors-warm` | `2034ce2def9d6c6ee3f211661911d21506cb8c7062c525a36bd0e314f1dcbcba` | `57365d3f05a0e1a155f33435bac4b6f0effc398689371003c84d95803ea7f7b4` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-torsion-free-zero-divisors-warm.tar.gz` |
| `oai-triangular-hilbert-warm` | `2cedc02909839600a6277d1c97c0ed2ce2b14c6586f077040adad9f518aa06dd` | `b2800934dd961cb79b57fe20dbbee330f730cf6a202c1819c39f61b423defbc2` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-triangular-hilbert-warm.tar.gz` |
| `oai-two-way-complementation-warm` | `5aa25df3ea91f0867ca41d9c7ed18dd398b12808b952962f2daff913c19127e2` | `977580fc18cff437b30e8d47c70277f8e5b3a407e757f52ff2bb641c9fe659ef` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-two-way-complementation-warm.tar.gz` |
| `oai-two-way-determinization-warm` | `40ec38d66117363470b96ee2900c16a47f5ac0a4fc181d13d7c4346d3e8667f1` | `c1f0da0413c6df06af6d10ba065b3709ffe6fdee84b5c0476b989ac5c1b93d80` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-two-way-determinization-warm.tar.gz` |
| `oai-uniform-gamma-warm` | `23bbef597fdc6da2a25de2faf3973583a50f2fe93deede63e56c4fb998af2b1d` | `81e37dd2e5db983526818dbb49d03d932b78e97d78da840fe428708ae40c5bd9` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-uniform-gamma-warm.tar.gz` |
| `oai-uniform-sparsest-cut-warm` | `33d3f5601982297982c4c887f252b7d10d9e886bef7a2f4bdeeba99768391db9` | `56fe86d40827d574ef7a1e047f4eb53fdbae4e21cda366051be5b2200de3e989` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-uniform-sparsest-cut-warm.tar.gz` |
| `oai-unique-games-theorem-warm` | `57c5c815658ced1768e8b5897df7b825dc0071514a2c3000817249c9ef9a6671` | `9e2d2a45f025e75a44b16ba35d41684281a163f35f750b2d285beb7cacd50561` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-unique-games-theorem-warm.tar.gz` |
| `oai-universal-f-infinity-warm` | `f1fb1890356aca144afdcad6dc50ded1f67aed6aabe9a291eeeee9b6d783698c` | `5271cdc888843e08b651b17e5c846e8bd0ee63510a164453257a629fa12ab8d4` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-universal-f-infinity-warm.tar.gz` |
| `oai-vertex-cover-warm` | `a10aa6ac1c5293ba2fb229238b31a885635b1896e40a86b4bd548746c9edcd5e` | `296d1323a44bb65b46220502ea8056bf69a24d86ec257e6a6c0d8a72cc762f57` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-vertex-cover-warm.tar.gz` |
| `oai-vlasov-maxwell-warm` | `ffc084ea7c214ea2fe938d9361943b797d3b4c57079a7dac0e08316bbdf610d6` | `0576fed1687ca0e77afcec0c2554b20546d7921b78068da769b758d5be1dfa7a` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-vlasov-maxwell-warm.tar.gz` |
| `oai-weak-hessian-warm` | `2f004b071d81701213285ec5a5a0ce0750f301222aed1b7a7a3956978c956f3e` | `4ad93d365bc69bf8bbef2325608ae59700ebb82286e1f704145b2199f79c878b` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-weak-hessian-warm.tar.gz` |
| `oai-weak-mtw-global-support-warm` | `e55147a32b129092cf9ad1f7f51d225e796a1dac2c6b51489d691802430a034d` | `f45c7b8fc209f58ec6f55e7af0f4c531c44fe2687c670a300e274b0e9a518390` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-weak-mtw-global-support-warm.tar.gz` |
| `oai-yau-counterexample-warm` | `613a87968fcb6e502c1f6596802fa1bac3d48dff8695586c059f172f04ebed71` | `27dc9eb05a75bb4aef9946f8fdaf8a52f0b5f108e7fb710dbf742e61096ea861` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/oai-v1-rc.11/oai-yau-counterexample-warm.tar.gz` |
| `permanent2-no_hint` | `37d5f234b19b0f97d6234882830669c436fad4211c42c75985b23020c82dd807` | `2db75d3caadbe11fb465a43506caf7bf8d0e56154a38f1d9a87f01580560d177` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.11/permanent2-no_hint.tar.gz` |
| `permanent2-no_hint` | `4ea4f40d6d714d030ecf7df328f0053e88008392d74743cb0d35c26ff312a9ac` | `1460cc43fa69c8d4cec492c82d45fbe855f2226780ced98bf731576e51268fbd` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.3/permanent2-no_hint.tar.gz` |
| `permanent2-no_hint` | `8008de7c1a3063a4add315049e4cb37ac3b62f9f357cee844f41ab29ac525018` | `7698dc73104b6aabbf49663f475506c1b0acb3930a0515a11ff50fa8b92b3f0a` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.2/permanent2-no_hint.tar.gz` |
| `permanent2-warm` | `681f3d1ad46decb33b0e2c6086830a05270f2c9cbd86ad2dd678305435e22039` | `516df6032bdaf6fa795156bf402338752d1cd8acb8a562355e63cba34b432c1e` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.11/permanent2-warm.tar.gz` |
| `permanent2-warm` | `cca3a2fb36701d96d2a9552c4de1aa790da6ca96ca6f6633d30e1a9f024d628f` | `47fe5a679fece5797c8a452a236303ef295602d0905a9e3fb01d4a87e77ce388` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.3/permanent2-warm.tar.gz` |
| `permanent2-warm` | `09d53da44052eecd5c50a69e85c2012e6dc555e3e13dc0687b58be452e67715d` | `70c1e585454928fbf18fbb12141c20f16545f090310e05fa268529b051a37eb6` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.2/permanent2-warm.tar.gz` |
| `ramsey96-no_hint` | `35632f292c8ff40f607315806a3747efefdc51929d6b0f8f5a785cf20a52fffc` | `5f310fe55174bdc6f2853f3051e1d546dd78eb9214132eb535ce189e1107a723` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.11/ramsey96-no_hint.tar.gz` |
| `ramsey96-no_hint` | `f03b1753cb68bd8521aba73933a81bfe331fe8a43c0ca8b62b4d249bd0d02475` | `e5b1e07a32dc20c8976a9b5be7588e8fca554025e2da8a429c68a451ee930531` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.3/ramsey96-no_hint.tar.gz` |
| `ramsey96-no_hint` | `30cb460c2be2891c807db6ade184bd5a4b0bc2342ec0ce6077e4d0241329c69b` | `13940c7ac6ae7ac1d5bbef9c7637505c7d500bb3922825828393c4a9c2d62de4` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.2/ramsey96-no_hint.tar.gz` |
| `ramsey96-warm` | `a8471ad1771f9f596015d069fb346f000b86126bd898b7c2457716166500e783` | `f06b9dc95f3bd6861724eafc6f20634c521fb830a3e91a4a3176894be1fe3da0` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.11/ramsey96-warm.tar.gz` |
| `ramsey96-warm` | `f67b590582c780f61713ad5f642e82807e7ab26866d9169fc5b84614c5920460` | `42090b97aa3693171788c8adfb88e07a2bcc7749403034b66813875954b21b75` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.3/ramsey96-warm.tar.gz` |
| `ramsey96-warm` | `2a6154d3c7bb0004432269ce2885d940f35627ca920902a8f568663a13e267c9` | `dc0b3d60898f2a68dccc7cebdf73111bf1e690dbe4103f2614f7ab44add7bdde` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.2/ramsey96-warm.tar.gz` |
| `slt26-no_hint` | `d8e665517bf1811ff9fa376d3d7e35f9b491b6d4ab0da1c406412a0be11fc8cb` | `8400f049033ded41f754fa4da25618868c03c031a358df62b151c3773ca41810` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.11/slt26-no_hint.tar.gz` |
| `slt26-no_hint` | `d87cdd0cd3d56caa995b7f14c7761191c15c0eedc69e6ac31a1b99b512c1cf49` | `ed38dcddef1d640ef17361e9039f3bb5a690b37a2fc6366df3f7b8c03593584f` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.3/slt26-no_hint.tar.gz` |
| `slt26-no_hint` | `727339755f2f4ab900857dc0754f20914b134b67bed0b339e207c445c4b130b8` | `b2dbbef40b1108008f3825a4059d48a0c71fb605f27f3d6605ee24a1b098580d` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.2/slt26-no_hint.tar.gz` |
| `slt26-warm` | `aa845928162840c174ad52a77c157b17c4155465faafe646a78febbcf7e5cd89` | `8138812f40a000aeba3af9b96e00bf2055053d1da1a9026a6e42282852ac13e2` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.11/slt26-warm.tar.gz` |
| `slt26-warm` | `5c7a675fc869f0ba4b89b97fb676ef5fb0ec36818ee63ef3a5269ca2c6b546a3` | `040944247111ec5d607519598bd0016cfa5a715b2dd9888b709f3d05aadefcbf` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.3/slt26-warm.tar.gz` |
| `slt26-warm` | `b0f05a7c85f65a45dfec416f886b2d5459afb0ee6de98ecbd6efc8e4e5f4ae86` | `11bf5bd976d3c7ca0420545b74555da08dd22bba7e2f1816f1c6842662de4937` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.2/slt26-warm.tar.gz` |
| `slt49-no_hint` | `15e654f5e92bcb731d88c538b43985edd6ed253fb2def092feb6087918fed597` | `a70fbe148b9063e36f19f4d9a9d0bfc9d582a1422892d17f707b6e2f9f27c73a` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.11/slt49-no_hint.tar.gz` |
| `slt49-no_hint` | `1ba9063e8f331774a300c2b6ce34c6935a4401fd42d2bf9a411f01509f54a3f1` | `56f46f53bc8cb01c5e8c2e91201e33762411aec6c5fa4ac6c380145ea3d4e53e` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.3/slt49-no_hint.tar.gz` |
| `slt49-no_hint` | `7d64a8f7a11b8374eaaff82570980a44aee3652729a57cb114814ff6b71b0062` | `9988508564088e7108dafa5c468a929bcdfd849981401bfe24f4af16d0660f70` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.2/slt49-no_hint.tar.gz` |
| `slt49-warm` | `a5e5596eb8dccf136caf3ce65aac9509db748771b658951b320c8d1133fc0359` | `80e7a270d2cc0d3ee6ee5a4b463d292dcd63ac89595dca1a74d2c3794a7013f6` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.11/slt49-warm.tar.gz` |
| `slt49-warm` | `4375780ab97b1873a1adb085a6b7f876dab3778131154b94a32886768e26a5be` | `0578472ec60cfaa07bd52d0e92e57b1fb7976fc260b1c3fe1a11a29e03d7e7c5` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.3/slt49-warm.tar.gz` |
| `slt49-warm` | `99d632d51dfd2a55e3af6535e607354733ffd434fdb01f7c98f24960122dd09b` | `adeb810e897574d5e6ceb6c4bfb9db169ab3cb00d01c6a5721a7180a43385f85` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/lcbench-v1-rc.10.2/slt49-warm.tar.gz` |
| `toyarith-warm` | `8e36b9c9d63a9aa649b66406fdb150c8bf484f2b4128463e67f213875606a343` | `6c2561ebc63ad9e5004aaadf6abd1a94fe5b949f230e3687df4897b8a517e55f` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/toyarith-rc.11/toyarith-warm.tar.gz` |
| `toyarith-warm` | `1fb59b63f616c6d1d62f7405ffe9c3986b763353b7b995309f3340eda605282b` | `a31d5e234130f7004defd452dd377ede58342e23dddc7741722afcaac41ba4cb` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/toyarith-rc.10.3/toyarith-warm.tar.gz` |
| `toyarith-warm` | `f381a2302711091efa5c51d55b8bdfb157c2b9ad5e87481989ae76b2d5d583b1` | `a58f2689c2ca3c29c83ec39578b5d29ec39e8e1f02e1ab2bcdcb7ebd8b2c56a1` | `curl -fLO https://github.com/MathCompressionBench/mcb/releases/download/toyarith-rc.10.2/toyarith-warm.tar.gz` |
<!-- end accepted-packages -->

Bundles made from the packages of the earlier releases `toyarith-rc.10.3`, `lcbench-v1-rc.10.3`, `toyarith-rc.10.2`
and `lcbench-v1-rc.10.2` are still accepted (they are in the table above): the organizers check each bundle with the
tools its package was made with. To check one yourself with `mcb verify`, use the tools of that release, for example
`git -C mcb checkout lcbench-v1-rc.10.3` in your checkout.

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
`lcbench-v1` is the study's seven tasks; `oai-v1` is the 175 tasks made from OpenAI's published math challenges.

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

6. **Fork this repository** on GitHub: the "Fork" button on its page, or
   `gh repo fork MathCompressionBench/mcb-submissions --clone=false`. You push to your fork; this repository takes
   only pull requests.

7. **Clone your fork** over https and add this repository as `upstream`:

   ```sh
   git clone https://github.com/<your account>/mcb-submissions.git
   cd mcb-submissions
   git remote add upstream https://github.com/MathCompressionBench/mcb-submissions.git
   ```

8. **Sync your fork with `upstream`, then make a branch**, before every submission. The organizers add newly
   accepted packages to `accepted-packages.json` on `main`. `mcb intake add` (step 9) reads that file in your clone
   and `scripts/check_submission.py` (step 11) reads it on your fork's `main` (`origin/main`), so with a stale fork
   both refuse bundles made from the newly accepted packages.

   ```sh
   git switch main
   git fetch upstream
   git merge --ff-only upstream/main
   git push origin main
   git switch -c my-submission
   ```

   The "Sync fork" button on your fork's GitHub page, or `gh repo sync <your account>/mcb-submissions`, syncs the
   fork on GitHub; then run `git switch main && git pull` in your clone. If you made your branch before syncing,
   run `git merge upstream/main` on it.

9. **Add your bundles.** In the MathCompressionBench checkout, add each bundle under your entry name:

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

10. **Write the metadata.** Copy `templates/metadata.yaml` to `entries/<entry>/metadata.yaml`, fill it in, and check
    it (from the MathCompressionBench checkout, or with plain Python from this checkout):

    ```sh
    bin/mcb submission validate <this repository's checkout>/entries/<entry>
    python3 scripts/submission_meta.py validate entries/<entry>
    ```

11. **Check the pull request before you open it.** Commit the files, then run

    ```sh
    python3 scripts/check_submission.py
    ```

    It applies the same rules the organizers apply (below) to your branch, compared with your fork's `main`
    (`origin/main`, synced in step 8), including the accepted packages and the metadata, and says what to fix. It
    needs only Python 3 and git.

12. **Push and open the pull request.** Push the branch to your fork:

    ```sh
    git push -u origin my-submission
    ```

    Then open the pull request against `main` of MathCompressionBench/mcb-submissions and fill in its template:
    GitHub offers it after the push, or run `gh pr create --repo MathCompressionBench/mcb-submissions --base main`.
    One pull request may add up to five bundles, for one or more tasks. You do not need to do anything else unless
    an organizer asks. The organizers' check posts one comment, **lcbench check status**, and edits that comment in
    place as the status changes (below).

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
