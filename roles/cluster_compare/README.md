# Cluster Compare

A role to facilitate the comparison of Kubernetes cluster configurations against the Red Hat Design References (RDS) by using the kube-compare tool. It leverages reference metadata from the upstream RDS repositories:
  - https://github.com/openshift-kni/telco-reference/ (Core)
  - https://github.com/openshift-kni/cnf-features-deploy/ (RAN)

Features

  - Clones or pulls reference metadata and templates from containers or Git repositories.
  - Executes the kube-compare tool for detailed cluster configuration analysis.
  - Supports both container-based and source-based workflows.
  - Can also **generate** a new reference (`metadata.yaml` + per-Kind CRs) from a
    running cluster or a must-gather, using the kube-compare `-g` flag
    (requires kube-compare v0.13.1 or newer).

## Requirements

  - A reachable OCP cluster running ocp-4.16 or newer.
  - A valid KUBECONFIG file is accessible. The KUBECONFIG file path must be provided as an environment variable.

## Variables

| Variable Name                         | Default Value                      | Required                                          | Description                                                                                            |
|-------------------------------------- |----------------------------------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------|
| `cc_infra_type`                       | core                               | false                                             | OCP deployment type (core, ran). Used in compare mode.                                                 |
| `cc_logging`                          | true                               | false                                             | Controls ansible task's logging output.                                                                |
| `cc_reports_dir`                      |                                    | true                                              | Output directory for the report files (compare) or the generated reference (generate).                 |
| `cc_mode`                             | compare                            | false                                             | `compare` runs kube-compare against a reference; `generate` produces a new reference.                  |
| `cc_version`                          | v0.13.1                            | false                                             | kube-compare release to install. `generate` needs v0.13.1+. Use `latest` to track newest.             |
| `cc_generate_config`                  | ""                                 | false                                             | generate: path to an existing refgen/v1 config. When empty, one is templated from `cc_generate_resources`. |
| `cc_must_gather`                      | ""                                 | false                                             | generate: optional must-gather directory for offline generation (`-f`).                                |
| `cc_generate_output_dir`              | ""                                 | false                                             | generate: where the reference is written. Defaults to `{{ cc_reports_dir }}/reference`.                |
| `cc_generate_resources`               | PTP, SR-IOV, TUNED set             | false                                             | generate: resource types to capture (kind, apiVersion, required, optional namespace/names).            |
| `cc_omit_annotations`                 | []                                 | false                                             | generate: extra annotation keys to strip (defaults still apply).                                       |
| `cc_omit_labels`                      | []                                 | false                                             | generate: extra label keys to strip (defaults still apply).                                            |
<!-- Variables for containerized version
| `cc_reference_container_source`       | ""                                                                                     | Pullspec for the container that holds the reference `metadata.yaml` and templates.                |
| `cc_reference_repository`             | ""                                                                                     | Git repository to clone for obtaining the reference `metadata.yaml` and templates.                     |
| `cc_reference_branch`                 | "main"                                                                                 | Branch of the reference repository to clone for obtaining the reference.                               |
| `cc_reference_metadata_yaml_location` | "/path/to/metadata.yaml"                                                               | Path from the reference repository root or container root to the reference `metadata.yaml`.            |
| `cc_compare_container_source`         | "registry-proxy.engineering.redhat.com/rh-osbs/openshift-kube-compare-artifacts:v4.18" | Pullspec for the kube-compare tool container. Leave empty to build from source.                        |
| `cc_compare_container_executable`     | "/usr/share/openshift/linux_amd64/kube-compare.rhel8"                                  | Path within the container to extract the `kubectl-compare_cluster` executable.                         |
| `cc_compare_repository`               | "https://github.com/openshift/kube-compare.git"                                        | URL of the cluster-compare command source code repository to build from source.                        |
| `cc_compare_branch`                   | "main"                                                                                 | Branch of the compare repository used when building from source.                                       |
| `cc_report_creator_version`           | "latest"                                                                               | Version of reports-creator to install, must match a tag or branch in the `kube-compare` repository.    |
-->

## Usage samples:

```yaml
- name: Run Cluster compare
  vars:
    cc_infra_type: ran
  ansible.builtin.include_role:
    name: redhatci.ocp.cluster_compare
```

Generate a reference from a running cluster (captures the default PTP, SR-IOV and
TUNED/PerformanceProfile set into `{{ cc_reports_dir }}/reference`):

```yaml
- name: Generate a kube-compare reference
  vars:
    cc_mode: generate
    cc_reports_dir: /var/tmp/cluster-compare
  ansible.builtin.include_role:
    name: redhatci.ocp.cluster_compare
```

## ToDo
  - Support for downstream builds from `registry.redhat.io/openshift4/kube-compare-artifacts-rhel9`. Still unavailable.
  - Some of the code for this is commented
