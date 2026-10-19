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

## Variable naming in roles (redhat-ci[no-role-prefix])

The custom `redhat-ci[no-role-prefix]` rule (`hack/rules/redhat_ci.py`)
enforces role-prefixed variable names for `set_fact` and `register`, and it
treats the two **differently**. The default local `ansible-lint` profile does
**not** load this rule, so violations pass locally but fail the CI
"Ansible-lint Check". The prefix is derived from the role name — for
`roles/<role>` it is the full name or the initials of the `_`-split parts
(e.g. `node_info` → `node_info` or `ni`); `global` is also always allowed.

- **`set_fact` → NO leading underscore.** Must start with `<prefix>_`
  (e.g. `ni_bmc_targets`, `node_info_x`, `global_x`). `_ni_foo` is rejected.
- **`register` → leading underscore REQUIRED.** Must start with `_<prefix>`
  (e.g. `_ni_bmc_managers`, `_node_info_x`). `ni_foo` (no underscore) is rejected.

So for the `node_info` role: name `set_fact` vars `ni_*` and `register` vars
`_ni_*`. Task-level `vars:` are not checked. Example of the mistake that keeps
recurring: a `set_fact: _ni_crd_bmc_version` must be `ni_crd_bmc_version`.
