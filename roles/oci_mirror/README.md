# oci_mirror

Mirror OpenShift operator catalogs into a registry.

Either you point the role at an existing **ImageSetConfiguration**, or you let it build one from a catalog index, a mirroring mode, and an optional operator list. If that list is missing or empty, the role mirrors the **full** index; if it is non-empty, only those operators are included.

## Requirements

- Reachable download URLs for bundled tooling (`oc-mirror`, `opm`, `jq`) and for the registries you mirror from/to
- Registry credentials when the index or target needs them (`om_auths_file`, or env such as `DOCKER_CONFIG`)

## Role variables

### Always relevant

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `om_target` | string | (none) | **Required.** Target registry (e.g. `registry.example.com:5000`). |
| `om_custom_config` | string | (none) | Path to your own ImageSetConfiguration. When set, the standard index/operator variables below are not used. |
| `om_allow_insecure_registries` | bool | `false` | Disables TLS verify for source and dest where `oc-mirror` supports it. |
| `om_auths_file` | string | (none) | Pull secret / registry auth JSON path. |
| `om_keep_working_dir` | bool | `false` | Keep the temp workspace after the role finishes (useful for debugging). |
| `om_remove_signatures` | bool | `false` | Pass `--remove-signatures` to `oc-mirror` (needed for some unsigned images). |
| `om_ignore_errors` | bool | `false` | Sets Ansible `ignore_errors` on the mirror task. |
| `om_validate_manifests` | bool | `true` | Validate all generated manifests after mirroring. See [Manifest Validation](#manifest-validation). |

### Standard path only (`om_custom_config` not set)

These are checked in `tasks/main.yml` once you are on the standard branch: `om_target_versions` must be `latest` or `all`, and `om_source_index` must be a non-empty string.

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `om_target_versions` | string | (none) | `latest` or `all` — channel scope for the generated ImageSet. |
| `om_source_index` | string | (none) | Default catalog index image (e.g. `registry.redhat.io/redhat/redhat-operator-index:v4.20`). |
| `om_operators` | dict | (none) | Keys are operator names; values are often `{}` or include `catalog:` to pull from another index. Omit or use `{}` with no keys for **full** index mirroring. |

For custom ImageSet mirroring you only need what that file implies plus `om_target` (and auth / TLS flags as usual); `mirror-custom.yml` validates `om_custom_config` and that the file exists.

## Examples

### Mirrors what is defined in the custom imageset

- name: Mirrors what is defined in the custom imageset
  ansible.builtin.include_role:
    name: redhatci.ocp.oci_mirror
  vars:
    om_target: registry.lab:4443
    om_custom_config: /tmp/imagesets/custom.yml

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

## Manifest Validation

When `om_validate_manifests` is `true` (the default), the role runs
`tasks/validate-manifests.yml` after copying manifests to `_om_output_dir`.
Each YAML file in that directory is parsed and checked for:

- `apiVersion`, `kind`, and `metadata.name` must be non-empty strings.
- `status` must not be an empty dict (`{}`). An empty status field can
  indicate a serialization defect in the mirroring tool output.
- **IDMS** (`idms-*.yaml`): `spec.imageDigestMirrors` must be a non-empty list.
- **ITMS** (`itms-*.yaml`): `spec.imageTagMirrors` must be a non-empty list.
- **CatalogSource** (`cs-*.yaml`): `spec.sourceType` and `spec.image` must be
  non-empty strings.
- **ClusterCatalog** (`cc-*.yaml`): `spec.source` must be defined.

Set `om_validate_manifests: false` to skip validation (e.g. when you know the
mirroring tool produces partial output intentionally).

### GitOps and ACM Policy Compliance

When using the generated manifests in a GitOps workflow or as ACM policy
sources, validation failures indicate that one or more manifests are incomplete
and must not be committed to the policy repository. Resolve the root cause
before propagating the manifests downstream.

## Output / facts

When mirroring produces manifests, they land under the **`om_output_dir`** fact (a temp dir unless you keep it).

Typical files:

- `idms-oc-mirror.yaml` — ImageDigestMirrorSet
- `cs-*.yaml` or `cc-*.yaml` — catalog manifests; which shape you get depends on OpenShift version (classic OLM vs OLM v1). See `tasks/mirroring.yml` for details.
