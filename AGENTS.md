# AI Agent Instructions — redhatci.ocp

## FQCN validation

`ansible-lint` only checks that module references use fully qualified
format — it does **not** verify the module actually exists in the named
collection. A wrong FQCN like `ansible.builtin.sefcontext` will pass
all lint and CI checks but fail at runtime.

When adding or changing FQCN references, verify each module exists:

```bash
ansible-doc <fqcn>            # single module check
./hack/check_fqcn_modules.sh  # scan all roles for unresolvable FQCNs
```

Common misattributions to watch for:
- `sefcontext` → `community.general.sefcontext` (NOT ansible.builtin)
- `archive` → `community.general.archive` (NOT ansible.builtin)
- `openssh_keypair` → `community.crypto.openssh_keypair` (NOT ansible.builtin)
- `firewalld` → `ansible.posix.firewalld` (NOT ansible.builtin)
- `mount` → `ansible.posix.mount` (NOT ansible.builtin)
- `sysctl` → `ansible.posix.sysctl` (NOT ansible.builtin)
- `nmcli` → `community.general.nmcli` (NOT ansible.builtin)
- `dci_*` → bare `dci_job` etc. (`ansible.legacy.dci_*` triggers fqcn[canonical])

## Running tests locally (without docker)

**Reproducing a CI failure? Do not run `./hack/run_ansible_test.sh` locally.**
That script *is* the CI harness: it uses `ansible-test --docker`, runs the
full sanity/units/integration matrix across every Python version, twice
(branch vs. `main`), and takes 10+ minutes — and it hard-requires a real
Docker daemon (a Podman symlink makes it fail). You do **not** need to
replicate that matrix to reproduce one failing check. Map the failing CI
test to the single `--local` command below and iterate in seconds. Reserve
`run_ansible_test.sh` for CI, or for when you specifically want the
branch-vs-`main` regression diff *and* Docker is available.

`./hack/run_ansible_test.sh` runs the full sanity/units/integration matrix
in containers with `ansible-test --docker`. That is what CI does on Ubuntu
and is the authoritative check, but it needs a working Docker daemon and
runs every test twice (branch vs. `main`) — slow for iteration.

For fast local feedback, or when Docker is unavailable, run individual
`ansible-test` commands with `--local` instead of the script. `--local`
uses the current Python interpreter and its installed dependencies, so no
container is launched:

```bash
# sanity for a single module/plugin (fastest feedback)
ansible-test sanity --local --requirements plugins/modules/<name>.py

# whole suites
ansible-test units --local --requirements
ansible-test integration --local --requirements <target>
```

Notes:
- `--local` runs against the current interpreter/venv. Drop `--python X.Y`
  (used by the docker path to pick a version) — with `--local` it must
  match the interpreter running ansible-test.
- `--requirements` installs the command's test dependencies into the
  current environment on first run.
- `--docker` requires a real Docker daemon. When `docker` is a symlink to
  Podman, the JSON output format differs and ansible-test fails with
  "Unable to get container host server information." Use `--local` there.
- Docker via `run_ansible_test.sh` remains the way to reproduce CI results
  and catch regressions against `main`; prefer it before opening a PR.
