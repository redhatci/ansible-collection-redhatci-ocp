# oci_mirror

Use `oc-mirror` to copy operator catalog images from a source index into a target registry.

For supported layouts, the role builds an ImageSetConfiguration, then runs `oc-mirror` so content is pushed to **`om_target`**. You can instead set **`om_custom_config`**.

## Requirements

- Network access to download tooling and to reach source/target registries
- Valid registry authentication when needed (e.g. `om_auths_file` or `DOCKER_CONFIG`)

## Role Variables

### Common variables

| Variable                       | Type    | Required | Default | Description                                                                                                                   |
|--------------------------------|---------|----------|---------|-------------------------------------------------------------------------------------------------------------------------------|
| `om_target`                    | string  | yes      |         | Target registry (e.g. `registry.example.com:5000`)                                                                            |
| `om_target_versions`           | string  | yes\*    |         | `latest` or `all` for standard branches. Ignored when `om_custom_config` is set.                                              |
| `om_custom_config`             | string  | no       |         | Path to a custom ImageSetConfiguration YAML. When set, runs the custom mirror after requirements and skips standard branches. |
| `om_allow_insecure_registries` | boolean | no       | `false` | Sets `--dest-tls-verify=false` and `--src-tls-verify=false` where applicable                                                  |
| `om_keep_working_dir`          | boolean | no       | `false` | Keep the temp working directory after the role finishes                                                                       |
| `om_auths_file`                | string  | no       |         | Pull secret / registry auth JSON path                                                                                         |
| `om_remove_signatures`         | boolean | no       | `false` | Passes `--remove-signatures` to `oc-mirror` when `true`. Required when there are images are not signed.                       |
| `om_ignore_errors`             | boolean | no       | `false` | Sets Ansible `ignore_errors` on the mirror task when `true`                                                                   |

\*Required for standard operator mirroring when `om_custom_config` is not used.

### Standard operator mirroring (`om_custom_config` unset)

| Variable          | Type   | Required | Description                                                                                                                    |
|-------------------|--------|----------|--------------------------------------------------------------------------------------------------------------------------------|
| `om_source_index` | string | yes\*    | Default catalog index (e.g. `registry.redhat.io/redhat/redhat-operator-index:v4.20`). Overridable per operator with `catalog`. |
| `om_operators`    | dict   | yes\*    | Operators to mirror (keys = operator names). Value may be `{}` or `catalog: <index image>`.                                    |

### Custom mirroring (`om_custom_config` set)

| Variable           | Type   | Required | Description                                                        |
|--------------------|--------|----------|--------------------------------------------------------------------|
| `om_custom_config` | string | yes      | Path to the ImageSetConfiguration file used.                       |

## Examples

The snippets below show some common mirroring use cases.

### Mirror latest — operators from multiple catalogs

Some operators use the default `om_source_index`; others can be taken from separate catalogs. The following is the only case supported with multiple catalogs.
```yaml
- name: Mirror custom operators from multiple catalogs
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

### Mirror using a custom ImageSetConfiguration

`om_custom_config` is a custom imagesetconfig file used as is to mirror the defined artifacts.

```yaml
- name: Mirror custom imageset configuration
  ansible.builtin.include_role:
    name: redhatci.ocp.oci_mirror
  vars:
    om_source_index: registry.redhat.io/redhat/redhat-operator-index:v4.20
    om_target: registry.lab:4443
    om_custom_config: /tmp/imagesets/custom.yml
```

### Mirror latest — listed operators

```yaml
- name: Mirror latest versions of operators
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

### Mirror all channels/versions

```yaml
- name: Mirror custom operators
  ansible.builtin.include_role:
    name: redhatci.ocp.oci_mirror
  vars:
    om_target_versions: all
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

### Mirror full index

```yaml
- name: Mirror index
  ansible.builtin.include_role:
    name: redhatci.ocp.oci_mirror
  vars:
    om_target_versions: all
    om_source_index: registry.redhat.io/redhat/redhat-operator-index:v4.20
    om_target: registry.lab:4443
```

### Mirror full index (latest channel only)

```yaml
- name: Mirror latest versions of operators (full catalog)
  ansible.builtin.include_role:
    name: redhatci.ocp.oci_mirror
  vars:
    om_target_versions: latest
    om_source_index: registry.redhat.io/redhat/redhat-operator-index:v4.20
    om_target: registry.lab:4443
```

### Keep the working directory

```yaml
- name: Mirror and keep temp workspace
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

### Playbook with shared vars

```yaml
---
- name: Mirror operators to disconnected registry
  hosts: localhost
  gather_facts: true
  vars:
    om_source_index: registry.redhat.io/redhat/redhat-operator-index:v4.20
    om_target: registry.lab:4443
    om_auths_file: /run/user/1000/containers/auth.json
    om_allow_insecure_registries: true

  tasks:
    - name: Mirror latest ODF operators
      ansible.builtin.include_role:
        name: redhatci.ocp.oci_mirror
      vars:
        om_target_versions: latest
        om_operators:
          mcg-operator:
          ocs-client-operator:
          ocs-operator:
          odf-csi-addons-operator:
          odf-prometheus-operator:
          rook-ceph-operator:

    - name: Mirror all channels for listed operators
      ansible.builtin.include_role:
        name: redhatci.ocp.oci_mirror
      vars:
        om_target_versions: all
        om_operators:
          advanced-cluster-management:
          multicluster-engine:
```

### Facts set after mirroring

After `mirroring.yml` copies at least one generated manifest (IDMS and/or catalogs) into a dedicated temp directory under **`om_output_dir`** fact.

- `idms-oc-mirror.yaml` — ImageDigestMirrorSet
- `cs-*.yaml` or `cc-*.yaml` — CatalogSource vs ClusterCatalog, per OpenShift **`version`** (see `mirroring.yml`)

`cs-*.yaml` for catalogSources are aimed to be used in cluster with OLM classic.
`cc-*.yaml` for catalogSources are aimed to be used in cluster with OLMv1.
