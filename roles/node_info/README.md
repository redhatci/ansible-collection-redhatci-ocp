# node_info role

Gathers node hardware and kernel information from an OpenShift cluster. This role collects hardware details using `lshw` and kernel information from all ready nodes in the cluster, saving the data as JSON files for diagnostics and analysis.

## Variables

| Variable                  | Default                             | Required | Description
| ------------------------- | ----------------------------------- | -------- | -----------
| ni_oc_tool_path           | `/usr/local/bin/oc`                 | No       | Path to the oc tool binary
| ni_job_logs_path          | `/tmp/node-info-logs`               | No       | Directory where output JSON files will be saved
| ni_disconnected           | `false`                             | No       | Enable disconnected mode (builds custom lshw container image)
| ni_local_registry         | `""`                                | No*      | Local registry URL for disconnected environments. Required when `ni_disconnected` is `true`
| ni_pullsecret_file        | `""`                                | No*      | Path to pull secret file for registry authentication. Required when `ni_disconnected` is `true`
| ni_tag                    | `latest`                            | No       | Tag used for the lshw container image in disconnected mode
| ni_local_img_path         | `/dci/lshw`                         | No       | Image path in the local registry for the lshw container used in disconnected mode

## Requirements

- OpenShift cluster with `oc` command-line tool available
- `kubernetes.core` Ansible collection
- Access to cluster with permissions to:
  - List nodes (`kubectl get nodes`)
  - Debug nodes (`oc debug node`)
- For disconnected environments:
  - `containers.podman` Ansible collection
  - Podman installed on control node
  - Access to local container registry

## Features

- **Automatic node discovery**: Identifies all ready nodes in the cluster
- **Kernel information**: Captures kernel version and command-line parameters for each node
- **Hardware details**: Uses `lshw` to gather comprehensive hardware information
- **Disconnected support**: Can build and use custom container image in air-gapped environments
- **Best-effort execution**: Uses `ignore_errors: true` to continue on failures

## Output Files

The role creates JSON files in `ni_job_logs_path`:

- `kernel.<node-name>.json` - Kernel information per node
- `hardware.<node-name>.json` - Hardware details per node

## Usage Examples

### Basic usage (connected environment)

```yaml
- name: Gather node information
  ansible.builtin.include_role:
    name: redhatci.ocp.node_info
  vars:
    ni_oc_tool_path: "/usr/bin/oc"
    ni_job_logs_path: "/var/log/cluster-diagnostics"
```

### Disconnected environment

```yaml
- name: Gather node information in disconnected mode
  ansible.builtin.include_role:
    name: redhatci.ocp.node_info
  vars:
    ni_oc_tool_path: "/usr/bin/oc"
    ni_job_logs_path: "/var/log/cluster-diagnostics"
    ni_disconnected: true
    ni_local_registry: "registry.example.com:5000"
    ni_pullsecret_file: "/path/to/pull-secret.json"
    ni_tag: "{{ ansible_date_time.epoch }}"
```

## Notes

- The role uses `ignore_errors: true` at the block level, so failures won't stop playbook execution
- In connected environments, the role uses `registry.access.redhat.com/ubi10/ubi-minimal:latest` and installs `lshw` on-the-fly
- In disconnected environments, you must provide a local registry to build and push the lshw container image
- Hardware information collection may take several minutes depending on the number of nodes
