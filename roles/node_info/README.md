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
| ni_collect_bmc            | `false`                             | No       | Enable out-of-band BMC firmware collection via the Redfish API
| ni_bmc_address            | `{}`                                | No*      | Map of node name → BMC hostname/IP. Required when `ni_collect_bmc=true` and `ni_bmc_from_bmh=false` (not needed when BareMetalHost discovery supplies addresses)
| ni_bmc_username           | `""`                                | No*      | Username for Redfish API authentication
| ni_bmc_password           | `""`                                | No*      | Password for Redfish API authentication. Use Ansible Vault to protect this value
| ni_bmc_from_bmh           | `false`                             | No       | Discover BMC address and credentials from `BareMetalHost` resources (follows `spec.bmc.credentialsName`). Merged on top of manually provided values
| ni_hub_kubeconfig         | `""`                                | No       | Kubeconfig to read `BareMetalHost`/`Secret` from. Empty uses the current cluster; set to the ACM hub kubeconfig when BMHs live on the hub
| ni_hub_kubeconfig_namespace | `""`                              | No       | Namespace to scope `BareMetalHost` discovery. When using an ACM hub with multiple managed clusters, set this to the namespace of the target managed cluster to avoid mixing BareMetalHosts across clusters. Empty = all namespaces
| ni_bmc_validate_certs     | `true`                              | No       | Set to `false` to skip TLS certificate validation for BMC Redfish requests. Use only for BMCs with self-signed certificates in lab environments

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
- **BMC firmware collection**: Queries each node's BMC out-of-band via Redfish and merges vendor and firmware version into `hardware.<node>.json` under `hardware.data.bmc` (keys: `vendor`, `version`)
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

### BMC firmware collection via Redfish

```yaml
- name: Gather node information with BMC firmware data
  ansible.builtin.include_role:
    name: redhatci.ocp.node_info
  vars:
    ni_oc_tool_path: "/usr/bin/oc"
    ni_job_logs_path: "/var/log/cluster-diagnostics"
    ni_collect_bmc: true
    ni_bmc_address:
      worker-0: "192.0.2.10"
      worker-1: "192.0.2.11"
    ni_bmc_username: "admin"
    ni_bmc_password: "{{ vault_bmc_password }}"
```

The `hardware.<node>.json` output will include a `bmc` key under `hardware.data`:

```json
{
  "hardware": {
    "node": "worker-0",
    "data": {
      "bmc": {
        "vendor": "Contoso",
        "version": "1.45.455b66-rev4"
      }
    }
  }
}
```

### BMC firmware collection with BareMetalHost discovery

Instead of listing addresses and credentials, the role can discover them from
`BareMetalHost` resources. For each host it uses `spec.bmc.address` and follows
`spec.bmc.credentialsName` to its `Secret`, so the Secret naming convention does
not matter. This works for IPI/ABI (BMHs on the cluster itself) and for ACM/ZTP
managed spokes (BMHs on the hub, reached via `ni_hub_kubeconfig`).

```yaml
- name: Gather node information with BMC data discovered from BareMetalHosts
  ansible.builtin.include_role:
    name: redhatci.ocp.node_info
  vars:
    ni_oc_tool_path: "/usr/bin/oc"
    ni_job_logs_path: "/var/log/cluster-diagnostics"
    ni_collect_bmc: true
    ni_bmc_from_bmh: true
    # Only needed when the BareMetalHosts live on an ACM hub:
    ni_hub_kubeconfig: "/path/to/hub/kubeconfig"
```

The node name is taken from the `bmac.agent-install.openshift.io/hostname`
annotation when present, otherwise from the BareMetalHost's discovered hostname
or its name. Only nodes whose name matches a ready node are queried.

## Notes

- The role uses `ignore_errors: true` at the block level, so failures won't stop playbook execution
- In connected environments, the role uses `registry.access.redhat.com/ubi10/ubi-minimal:latest` and installs `lshw` on-the-fly
- In disconnected environments, you must provide a local registry to build and push the lshw container image
- Hardware information collection may take several minutes depending on the number of nodes
- BMC credentials are passed with `no_log: true`; Redfish calls use `failed_when: false` so a missing or unreachable BMC does not abort the play
