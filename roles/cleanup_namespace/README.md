# cleanup_namespace

Finds and cleans up Kubernetes resources stuck in termination within a namespace. A resource is considered stuck when it has a `deletionTimestamp` (marked for deletion) but still has finalizers preventing its removal.

This role dynamically discovers all namespaced API resource types and scans for stuck resources, replicating the functionality of the [termin8](https://github.com/mvazquezc/termin8) tool without requiring any Go dependencies.

## Requirements

- A running OpenShift/Kubernetes cluster with proper credentials (via `KUBECONFIG` or `cn_kubeconfig`)
- The `kubernetes` Python library (`pip install kubernetes`)

## Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| cn_namespace | Yes | - | Namespace to scan for stuck resources |
| cn_dry_run | No | `false` | When `true`, only report stuck resources without removing finalizers |
| cn_skip_api_resources | No | `[]` | List of API resources to skip (format: `resource.group`, e.g. `events.events.k8s.io`) |
| cn_kubeconfig | No | `""` | Path to kubeconfig file. Falls back to `KUBECONFIG` env var |

## Output

The role registers `cn_stuck` with the following structure:

| Field | Description |
|-------|-------------|
| `cn_stuck.resources` | List of stuck resources found (name, resource_type, namespace, api_version) |
| `cn_stuck.non_available_api_services` | List of API service discovery warnings |

## Example of usage

```yaml
- name: Clean up stuck resources in a namespace
  ansible.builtin.include_role:
    name: redhatci.ocp.cleanup_namespace
  vars:
    cn_namespace: my-namespace

- name: Dry run - report stuck resources without cleaning
  ansible.builtin.include_role:
    name: redhatci.ocp.cleanup_namespace
  vars:
    cn_namespace: my-namespace
    cn_dry_run: true

- name: Clean up with skipped resources and custom kubeconfig
  ansible.builtin.include_role:
    name: redhatci.ocp.cleanup_namespace
  vars:
    cn_namespace: my-namespace
    cn_kubeconfig: /path/to/kubeconfig
    cn_skip_api_resources:
      - events.events.k8s.io
```
