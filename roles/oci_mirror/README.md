# oci_mirror

Mirror OpenShift operator catalogs into a registry using oc-mirror v2.

Either you point the role at an existing **ImageSetConfiguration**, or you let it build one from a catalog index, a mirroring mode, and an optional operator list. If that list is missing or empty, the role mirrors the **full** index; if it is non-empty, only those operators are included.

## Operation modes

| Mode | Description |
|------|-------------|
| `mirror` (default) | Mirror directly from a registry to another registry (`docker://` → `docker://`). |
| `m2d` | Mirror from a registry to local disk (`docker://` → `file://`). Requires `om_workspace_dir`. |
| `d2m` | Push a previously saved disk workspace to a registry (`file://` → `docker://`). Requires `om_workspace_dir` and `om_target`. |

A typical disconnected workflow: run `m2d` on a connected host to save content to disk, transfer the workspace, then run `d2m` on the disconnected host to push to the local registry.

## Requirements

- Reachable download URLs for bundled tooling (`oc-mirror`, `opm`, `jq`) and for the registries you mirror from/to
- Registry credentials when the index or target needs them (`om_auths_file`, or env such as `DOCKER_CONFIG`)

## Role variables

### Always relevant

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `om_operation` | string | `mirror` | Operation mode: `mirror`, `m2d`, or `d2m`. |
| `om_target` | string | (none) | Target registry (e.g. `registry.example.com:5000`). Required for `mirror` and `d2m` modes. |
| `om_workspace_dir` | string | `''` | Local disk workspace path. Required for `m2d` and `d2m` modes. |
| `om_helm_charts` | list | `[]` | Helm chart repositories to include in the ImageSetConfiguration. |
| `om_custom_config` | string | (none) | Path to your own ImageSetConfiguration. When set, the standard index/operator variables below are not used. |
| `om_allow_insecure_registries` | bool | `false` | Disables TLS verify for source and dest where `oc-mirror` supports it. |
| `om_auths_file` | string | (none) | Pull secret / registry auth JSON path. |
| `om_keep_working_dir` | bool | `false` | Keep the temp workspace after the role finishes (useful for debugging). |
| `om_remove_signatures` | bool | `false` | Pass `--remove-signatures` to `oc-mirror` (needed for some unsigned images). |
| `om_ignore_errors` | bool | `false` | Sets Ansible `ignore_errors` on the mirror task. |

### Standard path only (`om_custom_config` not set)

These are checked in `tasks/main.yml` once you are on the standard branch: `om_target_versions` must be `latest` or `all`, and `om_source_index` must be a non-empty string.

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `om_target_versions` | string | (none) | `latest` or `all` — channel scope for the generated ImageSet. |
| `om_source_index` | string | (none) | Default catalog index image (e.g. `registry.redhat.io/redhat/redhat-operator-index:v4.20`). |
| `om_operators` | dict | (none) | Keys are operator names; values are often `{}` or include `catalog:` to pull from another index. Omit or use `{}` with no keys for **full** index mirroring. |

For custom ImageSet mirroring you only need what that file implies plus `om_target` (and auth / TLS flags as usual); `mirror-custom.yml` validates `om_custom_config` and that the file exists.

### Helm chart mirroring (`om_helm_charts`)

Each entry in `om_helm_charts` supports:

```yaml
om_helm_charts:
  - name: my-repo            # repository alias
    url: https://charts.example.com
    charts:                  # optional: specific charts to mirror
      - name: my-chart
        version: 1.2.3       # optional: pinned version
```

If `om_helm_charts` is empty (the default), no `helm:` section is added to the generated ImageSetConfiguration.

## Examples

### Mirrors what is defined in the custom imageset

```yaml
- name: Mirrors what is defined in the custom imageset
  ansible.builtin.include_role:
    name: redhatci.ocp.oci_mirror
  vars:
    om_target: registry.lab:4443
    om_custom_config: /tmp/imagesets/custom.yml
```

### Mirror latest version of the listed operators

```yaml
- name: Mirror latest version of the listed operators
  ansible.builtin.include_role:
    name: redhatci.ocp.oci_mirror
  vars:
    om_target_versions: latest
    om_source_index: registry.redhat.io/redhat/redhat-operator-index:v4.20
    om_target: registry.lab:4443
    om_operators:
      mcg-operator:
      ocs-client-operator:
      ocs-operator:
      odf-csi-addons-operator:
      odf-prometheus-operator:
      rook-ceph-operator:
```

### Full index

```yaml
- name: Full index
  ansible.builtin.include_role:
    name: redhatci.ocp.oci_mirror
  vars:
    om_target_versions: all
    om_source_index: registry.redhat.io/redhat/redhat-operator-index:v4.20
    om_target: registry.lab:4443
```

```yaml
- name: Mirror entire index with latest operators versions
  ansible.builtin.include_role:
    name: redhatci.ocp.oci_mirror
  vars:
    om_target_versions: latest
    om_source_index: registry.redhat.io/redhat/redhat-operator-index:v4.20
    om_target: registry.lab:4443
```

### Multiple catalogs (per-operator `catalog`)

Some operators stay on `om_source_index`; others use another index via `catalog` on that operator entry.

```yaml
- name: Mirror operators from mixed catalogs
  ansible.builtin.include_role:
    name: redhatci.ocp.oci_mirror
  vars:
    om_target_versions: latest
    om_source_index: registry.redhat.io/redhat/redhat-operator-index:v4.20
    om_target: registry.lab:4443
    om_ignore_errors: true
    om_remove_signatures: true
    om_operators:
      zabbix-operator-certified:
        catalog: registry.redhat.io/redhat/certified-operator-index:v4.20
      nim-operator-certified:
        catalog: registry.redhat.io/redhat/certified-operator-index:v4.20
      sriov-fec:
        catalog: registry.redhat.io/redhat/certified-operator-index:v4.20
      mcg-operator:
      ocs-client-operator:
      ocs-operator:
      odf-csi-addons-operator:
      odf-prometheus-operator:
```

### Keep the working directory

```yaml
- name: Mirror and keeps temp workspace
  ansible.builtin.include_role:
    name: redhatci.ocp.oci_mirror
  vars:
    om_target_versions: latest
    om_source_index: registry.redhat.io/redhat/redhat-operator-index:v4.20
    om_target: registry.example.com:5000
    om_operators:
      odf-operator:
      local-storage-operator:
    om_keep_working_dir: true
```

### Mirror-to-disk (M2D) then disk-to-mirror (D2M)

Use this pattern for air-gapped environments where a connected host saves content to disk,
and a disconnected host later pushes it to a local registry.

```yaml
# Step 1: On the connected host — save to disk
- name: Mirror operators to local disk
  ansible.builtin.include_role:
    name: redhatci.ocp.oci_mirror
  vars:
    om_operation: m2d
    om_workspace_dir: /mnt/transfer/mirror-workspace
    om_custom_config: /tmp/my-imageset.yaml

# Step 2: Transfer /mnt/transfer/mirror-workspace to the disconnected host

# Step 3: On the disconnected host — push from disk to registry
- name: Push mirrored content to local registry
  ansible.builtin.include_role:
    name: redhatci.ocp.oci_mirror
  vars:
    om_operation: d2m
    om_workspace_dir: /mnt/transfer/mirror-workspace
    om_target: registry.disconnected.lab:5000
```

### Including Helm charts in the ImageSetConfiguration

```yaml
- name: Mirror operators and Helm charts
  ansible.builtin.include_role:
    name: redhatci.ocp.oci_mirror
  vars:
    om_target_versions: latest
    om_source_index: registry.redhat.io/redhat/redhat-operator-index:v4.20
    om_target: registry.lab:4443
    om_helm_charts:
      - name: redhat-charts
        url: https://redhat-developer.github.io/redhat-helm-charts
        charts:
          - name: ibm-db2uoperator-icr
            version: 3.2.0
```

## Output / facts

When mirroring produces manifests, they land under the **`om_output_dir`** fact (a temp dir unless you keep it).

Typical files:

- `idms-oc-mirror.yaml` — ImageDigestMirrorSet
- `cs-*.yaml` or `cc-*.yaml` — catalog manifests; which shape you get depends on OpenShift version (classic OLM vs OLM v1). See `tasks/mirroring.yml` for details.

For `m2d` mode, `om_output_dir` is set to `om_workspace_dir` after the mirror completes.
