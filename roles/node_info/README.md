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
| ni_collect_bios_settings  | `false`                             | No       | Enable live BIOS settings collection via Redfish (best-effort); reuses BMC addresses and credentials
| ni_bmc_address            | `{}`                                | No*      | Map of node name → BMC hostname/IP. Required when `ni_collect_bmc=true` and `ni_bmc_from_bmh=false` (not needed when BareMetalHost discovery supplies addresses)
| ni_bmc_username           | `""`                                | No*      | Username for Redfish API authentication
| ni_bmc_password           | `""`                                | No*      | Password for Redfish API authentication. Use Ansible Vault to protect this value
| ni_bmc_from_bmh           | `false`                             | No       | Discover BMC address and credentials from `BareMetalHost` resources (follows `spec.bmc.credentialsName`). Merged on top of manually provided values
| ni_hub_kubeconfig_namespace | `openshift-machine-api`           | No       | Namespace to scope `BareMetalHost` discovery. Defaults to `openshift-machine-api` (the Metal3 namespace). When using an ACM hub with multiple managed clusters, set this to the namespace of the target managed cluster to avoid mixing BareMetalHosts across clusters
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

- When `ni_bmc_from_bmh: true`, the kubeconfig user (or service account) must have:
  - `get`/`list` on `BareMetalHost` resources (`metal3.io/v1alpha1`)
  - `get`/`list` on `HostFirmwareComponents` resources (`metal3.io/v1alpha1`) in the target namespace (used by the CRD-first firmware lookup)
  - `get` on `Secret` resources in the namespaces containing BMC credential secrets

## Features

- **Automatic node discovery**: Identifies all ready nodes in the cluster
- **Kernel information**: Captures kernel version and command-line parameters for each node
- **Hardware details**: Uses `lshw` to gather comprehensive hardware information
- **BMC firmware collection**: Merges vendor and firmware version into `hardware.<node>.json` under `hardware.data.bmc` (keys: `vendor`, `version`) using a two-tier strategy:
  - **Tier 1 — `hostfirmwarecomponents.metal3.io` CRD** (preferred when `ni_bmc_from_bmh: true`): reads `currentVersion` from the CRD. No out-of-band access or credentials required; kubeconfig access is sufficient. `currentVersion` reflects the firmware currently running on the BMC; `previousVersion` holds the prior version.
  - **Tier 2 — Redfish fallback**: used when the CRD is unavailable or carries no `currentVersion` for the `bmc` component, or when `ni_bmc_from_bmh: false` (manual address mode). Queries `/redfish/v1/Managers` out-of-band.
- **BIOS settings collection**: Queries the live Redfish `Bios` resource (not the BareMetalHost `HostFirmwareSettings`) and merges it into `hardware.<node>.json` under `hardware.data.bios_settings` (keys: `registry`, `attributes`). Attributes are a `name`/`value` list (values stringified) to keep the Elasticsearch mapping stable (`nodes.hardware.data.bios_settings.*`). Collection is best-effort: nodes that fail are simply omitted.
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
managed spokes (BMHs on the hub — the caller sets the k8s context).

When `ni_bmc_from_bmh: true` the role uses a **two-tier firmware lookup**:

1. **CRD-first**: queries `hostfirmwarecomponents.metal3.io` for each node and
   reads `status.components[?component=="bmc"].currentVersion`. This requires no
   out-of-band BMC network access or credentials — only kubeconfig access.
   `currentVersion` reflects the firmware currently running on the BMC;
   `previousVersion` holds the firmware version prior to the most recent update.
2. **Redfish fallback**: if the `HostFirmwareComponents` CRD is absent or carries
   no `currentVersion` for the `bmc` component, the role falls back to direct
   Redfish queries using the BMC address and credentials from the BareMetalHost.

```yaml
- name: Gather node information with BMC data discovered from BareMetalHosts
  ansible.builtin.include_role:
    name: redhatci.ocp.node_info
  vars:
    ni_oc_tool_path: "/usr/bin/oc"
    ni_job_logs_path: "/var/log/cluster-diagnostics"
    ni_collect_bmc: true
    ni_bmc_from_bmh: true
    # Scope discovery to a specific namespace (default: openshift-machine-api).
    # When using an ACM hub, set this to the managed cluster's namespace:
    # ni_hub_kubeconfig_namespace: "spoke-cluster-1"
```

The role uses whatever k8s context is active — the caller is responsible for
setting up the kubeconfig environment, as it is for all other k8s tasks in this
role. The node name is taken from the `bmac.agent-install.openshift.io/hostname`
annotation when present, otherwise from the BareMetalHost's discovered hostname
or its name. Only nodes whose name matches a ready node are queried.

### BIOS settings collection

```yaml
- name: Gather node information with BIOS settings (manual BMC addresses)
  ansible.builtin.include_role:
    name: redhatci.ocp.node_info
  vars:
    ni_collect_bios_settings: true
    ni_bmc_address:
      node1: 192.0.2.10
    ni_bmc_username: admin
    ni_bmc_password: "{{ vault_bmc_password }}"

- name: Gather node information with BIOS settings (from BareMetalHosts)
  ansible.builtin.include_role:
    name: redhatci.ocp.node_info
  vars:
    ni_collect_bios_settings: true
    ni_bmc_from_bmh: true
```

Output sample (`hardware.<node>.json`):

```json
{"hardware": {"data": {"bios_settings": {
  "registry": "BiosAttributeRegistry.v1_0_0",
  "attributes": [{"name": "ProcTurboMode", "value": "Enabled"}]
}}}}
```

## Notes

- The role uses `ignore_errors: true` at the block level, so failures won't stop playbook execution
- In connected environments, the role uses `registry.access.redhat.com/ubi10/ubi-minimal:latest` and installs `lshw` on-the-fly
- In disconnected environments, you must provide a local registry to build and push the lshw container image
- Hardware information collection may take several minutes depending on the number of nodes
- BMC credentials are passed with `no_log: true`; Redfish calls use `failed_when: false` so a missing or unreachable BMC does not abort the play
