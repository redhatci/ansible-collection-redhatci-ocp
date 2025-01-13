# Cluster Compare

A role to facilitate the comparison of Kubernetes cluster configurations against the Red Hat Design References (RDS) by using the kube-compare tool. It leverages reference metadata from the upstream RDS repositories:
  - https://github.com/openshift-kni/telco-reference/ (Core)
  - https://github.com/openshift-kni/cnf-features-deploy/ (RAN)

Features

  - Clones or pulls reference metadata and templates from containers or Git repositories.
  - Executes the kube-compare tool for detailed cluster configuration analysis.
  - Supports both container-based and source-based workflows.

## Requirements

  - A reachable OCP cluster running ocp-4.16 or newer.
  - A valid KUBECONFIG file is accessible. The KUBECONFIG file path must be provided as an environment variable.

## Variables

| Variable Name                         | Default Value                      | Required                                          | Description                                                                                            |
|-------------------------------------- |----------------------------------- | ------------------------------------------------- | -------------------------------------------------------------------------------------------------------|
| `cc_infra_type`                       | core                               | false                                             | OCP deployment type (core, ran)                                                                        |
| `cc_logging`                          | true                               | false                                             | Controls ansible task's logging output.                                                                |
| `cc_reports_dir`                      |                                    | true                                              | Output directory for the report files                                                                  |
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

## ToDo
  - Support for downstream builds from `registry.redhat.io/openshift4/kube-compare-artifacts-rhel9`. Still unavailable.
  - Some of the code for this is commented
