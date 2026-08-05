# monitor_agent_based_installer

Tracks the progress of the agent-based OpenShift installation via `openshift-install agent` commands.

The role:

1. Waits for the cluster API to become available.
2. Waits for bootstrap to complete.
3. Waits for the full installation to complete (with optional retry logic for known
   API-reachability issues).
4. Gathers bootstrap logs on failure and raises a descriptive error.

## Role Variables

| Variable | Type | Default | Description |
|---|---|---|---|
| `mabi_workarounds` | list(str) | `[]` | List of workaround identifiers to enable. Each identifier activates compensating behaviour for a known issue. Pass from the calling agent so that role behaviour is driven by the agent configuration. |
| `mabi_retry_install_complete_check` | bool | `{{ 'retry_install_complete_check' in mabi_workarounds }}` | When `true`, retries the install-complete check up to 10 times (60 s delay) to work around transient API-VIP reachability failures. Automatically enabled when the `retry_install_complete_check` identifier is present in `mabi_workarounds`. |
| `generated_dir` | str | `{{ repo_root_path }}/generated` | Base directory for generated manifests. |
| `manifests_dir` | str | `{{ generated_dir }}/{{ cluster_name }}` | Directory containing the cluster manifests. |
| `agent_based_installer_bootstrap_node` | str | `{{ groups['masters'][0] }}` | Inventory host name of the bootstrap / rendezvous node. |
| `host_ip_keyword` | str | `ansible_host` | Host variable key used to retrieve the bootstrap node IP. |
| `agent_based_installer_path` | str | _(required)_ | Full path to the `openshift-install` binary. |
| `cluster` | str | _(required)_ | Cluster name used to construct the API URL. |
| `base_dns_domain` | str | _(required)_ | Base DNS domain used to construct the API URL. |
| `repo_root_path` | str | _(required)_ | Root path of the repository; used to derive `generated_dir` and to store gathered logs on failure. |
| `cluster_name` | str | _(required)_ | Cluster name used to derive `manifests_dir`. |

## Usage

### Basic usage

```yaml
- name: Monitor agent-based installation
  ansible.builtin.include_role:
    name: redhatci.ocp.monitor_agent_based_installer
  vars:
    cluster: my-cluster
    base_dns_domain: example.com
    repo_root_path: /path/to/repo
    cluster_name: my-cluster
    agent_based_installer_path: /usr/local/bin/openshift-install
```

### Passing workarounds from the calling agent

The recommended pattern is for the calling agent to forward its own workaround list
to the role so that compensating behaviours are activated consistently:

```yaml
- name: Monitor agent-based installation
  ansible.builtin.include_role:
    name: redhatci.ocp.monitor_agent_based_installer
  vars:
    cluster: my-cluster
    base_dns_domain: example.com
    repo_root_path: /path/to/repo
    cluster_name: my-cluster
    agent_based_installer_path: /usr/local/bin/openshift-install
    mabi_workarounds: "{{ dci_workarounds | default([]) }}"
```

With this pattern, adding a workaround identifier to `dci_workarounds` in the agent
configuration is sufficient to enable the corresponding compensating behaviour inside
the role — no role-level variable override is needed.
