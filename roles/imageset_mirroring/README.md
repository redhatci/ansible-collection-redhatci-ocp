# imageset_mirroring

Mirror OpenShift operator catalogs and images using oc-mirror.

## Description

This role provides three different approaches to mirror operators from a source catalog to a target registry:

- **mirror-latest**: Mirror only the latest version of specified operators
- **mirror-all**: Mirror all channels and versions of specified operators
- **mirror-custom**: Mirror using a pre-defined custom ImageSetConfiguration file

## Requirements

- `oc-mirror` binary (automatically downloaded by the role)
- Network access to source and target registries
- Valid authentication for registries (if required)

## Role Variables

### Common Variables

| Variable                       | Type    | Required | Default | Description                                                                                          |
|--------------------------------|---------|----------|---------|------------------------------------------------------------------------------------------------------|
| `im_task`                      | string  | yes*     | -       | Mirroring action to perform. Valid values: `latest`, `all`, `custom`.                                |
| `im_target`                    | string  | yes      | -       | Target registry for mirroring (e.g., `registry.example.com:5000`)                                    |
| `im_allow_insecure_registries` | boolean | no       | `false` | Allow insecure registries (sets `--dest-tls-verify=false` and `--src-tls-verify=false`)              |
| `im_keep_working_dir`          | boolean | no       | `false` | Keep temporary working directory after mirroring completes                                           |
| `im_auths_file`                | string  | no       | -       | Path to registry authentication file (e.g., `/path/to/pull-secret.json`)                             |

### Task-Specific Variables

#### mirror-latest & mirror-all

| Variable          | Type       | Required | Description                                                                               |
|-------------------|------------|----------|-------------------------------------------------------------------------------------------|
| `im_source_index` | string     | yes      | Source catalog index (e.g., `registry.redhat.io/redhat/redhat-operator-index:v4.20`)      |
| `im_operators`    | dictionary | yes      | Dictionary of operators to mirror (keys are operator names)                               |

#### mirror-custom

| Variable                         | Type   | Required | Description                                         |
|----------------------------------|--------|----------|-----------------------------------------------------|
| `im_custom_config`               | string | yes      | Path to custom ImageSetConfiguration YAML file      |

## Examples

### Example 1: Mirror Latest Version of Operators (using im_mirror_task)

```yaml
- name: "Mirror latest operators"
  ansible.builtin.include_role:
    name: redhatci.ocp.imageset_mirroring
  vars:
    im_task: latest
    im_source_index: registry.redhat.io/redhat/redhat-operator-index:v4.20
    im_target: registry.lab:4443
    im_operators:
      mcg-operator:
      ocs-client-operator:
      advanced-cluster-management:
    im_allow_insecure_registries: true
    im_auths_file: /path/to/pull-secret.json
```

### Example 1b: Mirror Latest Version (using tasks_from - legacy)

```yaml
- name: "Mirror latest operators"
  ansible.builtin.include_role:
    name: redhatci.ocp.imageset_mirroring
    tasks_from: mirror-latest.yml
  vars:
    im_source_index: registry.redhat.io/redhat/redhat-operator-index:v4.20
    im_target: registry.lab:4443
    im_operators:
      mcg-operator:
      ocs-client-operator:
      advanced-cluster-management:
    im_allow_insecure_registries: true
    im_auths_file: /path/to/pull-secret.json
```

### Example 2: Mirror All Versions of Operators

```yaml
- name: "Mirror all operators"
  ansible.builtin.include_role:
    name: redhatci.ocp.imageset_mirroring
  vars:
    im_task: all
    im_source_index: registry.redhat.io/redhat/redhat-operator-index:v4.20
    im_target: registry.lab:4443
    im_operators:
      openshift-gitops-operator:
      rhacm-operator:
```

### Example 3: Mirror Using Custom ImageSetConfiguration

```yaml
- name: "Mirror custom imageset-config"
  ansible.builtin.include_role:
    name: redhatci.ocp.imageset_mirroring
  vars:
    im_task: custom
    im_custom_config: /tmp/my-custom-imagesetconfig.yaml
    im_target: registry.lab:4443
    im_auths_file: /path/to/pull-secret.json
```

### Example 4: Generate Configuration Only (No Mirror)

```yaml
- name: "Generate ImageSetConfiguration without mirroring"
  ansible.builtin.include_role:
    name: redhatci.ocp.imageset_mirroring
    tasks_from: mirror-latest
  vars:
    im_source_index: registry.redhat.io/redhat/redhat-operator-index:v4.20
    im_target: registry.example.com:5000
    im_operators:
      odf-operator:
      local-storage-operator:
    im_keep_working_dir: true
```

### Example 5: Complete Playbook

```yaml
---
- name: Mirror operators to disconnected registry
  hosts: localhost
  gather_facts: true
  vars:
    im_source_index: registry.redhat.io/redhat/redhat-operator-index:v4.20
    im_target: registry.lab:4443
    im_auths_file: /run/user/1000/containers/auth.json
    im_allow_insecure_registries: true
    
  tasks:
    - name: "Mirror latest ODF operators"
      ansible.builtin.include_role:
        name: redhatci.ocp.imageset_mirroring
      vars:
        im_task: latest
        im_operators:
          mcg-operator:
          ocs-client-operator:
          ocs-operator:
          odf-csi-addons-operator:
          odf-prometheus-operator:
          rook-ceph-operator:
    
    - name: "Mirror all ACM operators"
      ansible.builtin.include_role:
        name: redhatci.ocp.imageset_mirroring
      vars:
        im_task: all
        im_operators:
          advanced-cluster-management:
          multicluster-engine:
```

## How It Works

### mirror-latest

1. Downloads the latest `oc-mirror` binary
2. Queries the source catalog for each operator's default channel
3. Identifies the latest CSV version for the default channel
4. Generates an ImageSetConfiguration with specific version constraints
5. Executes `oc-mirror` to perform the mirroring

### mirror-all

1. Downloads the latest `oc-mirror` binary
2. Generates an ImageSetConfiguration with `full: true` for all operators
3. Executes `oc-mirror` to mirror all channels and versions

### mirror-custom

1. Downloads the latest `oc-mirror` binary
2. Uses the provided custom ImageSetConfiguration file
3. Executes `oc-mirror` to perform the mirroring

## Output

The role creates a temporary directory (e.g., `/tmp/im_tmp.xxxxx`) containing:
- Downloaded `oc-mirror` binary
- Generated `imagesetconfig.yaml` (if applicable)
- oc-mirror workspace with mirror metadata

By default, this directory is removed after completion unless `im_keep_working_dir: true` is set.

## Outputs facts

The role copies generated IDMS and CatalogSource manifest files into a temporary directory with `_im_output_dir.` prefix.

These manifest files can be used directly to apply the image sources and catalog sources into a running cluster.

The role sets the following output variables:

- `im_image_source_file`: The path to the IDMS/ICSP manifest file (e.g., ImageDigestMirrorSet.yaml or imageContentSourcePolicy.yaml)
- `im_catalog_source_file`: The path to the CatalogSource manifest file
