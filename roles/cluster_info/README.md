# cluster_info role

Gathers cluster configuration facts from an OpenShift cluster. This role collects key cluster properties such as OCP version, platform type, topology, region, IP stack, network type, and default storage classes, making them available as Ansible facts for downstream tasks.

## Requirements

- `kubernetes.core` Ansible collection
- `jmespath` Python package on the Ansible controller (`dnf install python3-jmespath`)
- Access to the OpenShift cluster API with permissions to read:
  - `config.openshift.io/v1/ClusterVersion`
  - `config.openshift.io/v1/Infrastructure`
  - `config.openshift.io/v1/Network`
  - `storage.k8s.io/v1/StorageClass`
  - `v1/Node` (optional — required only for the region fallback on non-AWS/GCP platforms such as Azure)

## Output Facts

| Fact                       | Type   | Description
| -------------------------- | ------ | -----------
| cluster_info_ocp_version   | string | Desired OCP version from ClusterVersion status (e.g. `4.16.12`). `unknown` if unavailable.
| cluster_info_platform      | string | Platform type from Infrastructure spec (e.g. `AWS`, `BareMetal`, `None`). `unknown` if unavailable.
| cluster_info_topology      | string | Infrastructure topology from Infrastructure status (e.g. `HighlyAvailable`, `SingleReplica`). `unknown` if unavailable.
| cluster_info_region        | string | Cloud region from Infrastructure status (AWS/GCP/Azure). `unknown` for bare-metal or if unavailable.
| cluster_info_ip_stack      | string | IP stack derived from cluster network CIDRs: `ipv4`, `ipv6`, or `dual`. `unknown` if unavailable.
| cluster_info_network_type  | string | CNI network type from Network spec (e.g. `OVNKubernetes`, `OpenShiftSDN`). `unknown` if unavailable.
| cluster_info_default_storage       | list   | Names of StorageClasses annotated as default. Empty list `[]` if none found or unavailable.
| cluster_info_node_count            | int    | Total number of cluster nodes (each node counted once). `0` if unavailable.
| cluster_info_node_count_by_role    | dict   | Node count per `node-role.kubernetes.io/<role>` label (e.g. `{"master": 3, "control-plane": 3, "worker": 3}`). Empty dict `{}` if unavailable.

All facts are pre-initialized to `unknown` (or `[]`/`{}`/`0`) before any API queries, so they are always defined even when the cluster is unreachable.

## Features

- **Best-effort execution**: Uses `ignore_errors: true` so failures do not stop playbook execution
- **Always-defined facts**: All 7 facts are pre-initialized before the API queries block
- **IP stack detection**: Automatically detects single-stack IPv4/IPv6 or dual-stack from cluster network CIDRs
- **Default storage classes**: Identifies storage classes annotated as the cluster default
- **No-log on API calls**: All `kubernetes.core.k8s_info` tasks use `no_log: true` to avoid leaking sensitive data

## Usage Examples

### Basic usage

```yaml
- name: Gather cluster information
  ansible.builtin.include_role:
    name: redhatci.ocp.cluster_info

- name: Display OCP version
  ansible.builtin.debug:
    msg: "Running OCP {{ cluster_info_ocp_version }} on {{ cluster_info_platform }} ({{ cluster_info_topology }})"
```

## Notes

- The `cluster_info_region` fact reflects AWS, GCP, or Azure region; for other platforms (e.g. `BareMetal`) it will be `unknown`
- The `cluster_info_default_storage` fact returns only StorageClasses annotated with `storageclass.kubernetes.io/is-default-class: "true"`
- The `cluster_info_topology` fact is sourced from `Infrastructure.status.infrastructureTopology` (typically `HighlyAvailable` or `SingleReplica`)
- `cluster_info_node_count` always counts each node once. `cluster_info_node_count_by_role` counts a node once per `node-role.kubernetes.io/<role>` label it carries, so the per-role sum can exceed `cluster_info_node_count`: OCP control-plane nodes carry both `master` and `control-plane`, and compact/SNO nodes carry both `master` and `worker`.
