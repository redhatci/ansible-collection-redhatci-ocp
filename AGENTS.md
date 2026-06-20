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

## ansible-test and Podman

`ansible-test --docker` requires a real Docker daemon. When `docker` is
a symlink to Podman, the JSON output format differs and ansible-test
fails with "Unable to get container host server information." Use
`--local` instead on Podman-only systems.
