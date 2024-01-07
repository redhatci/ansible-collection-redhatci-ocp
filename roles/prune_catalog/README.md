# prune_catalog role

A role to prune a File Base Catalog (FBC). The role creates a pruned catalog, leaving only the specified operators.

## Parameters

Name                   | Required | Default                                       | Description
---------------------- | -------- | --------------------------------------------- | ------------
pc_source_catalog      | Yes      |                                               | Source catalog to be pruned
pc_destination_catalog | Yes      |                                               | Catalog containing the required operators
pc_operators           | Yes      |                                               | The set of operators to keep in the pruned catalog. See examples below
pc_opm_args            | No       | ""                                            | Arguments for opm command. Those will be applied globally for all opm calls
pc_expire              | No       | false                                         | Whether or not to set an expiration label on the catalog
pc_expire_time         | No       | 5h                                            | The amount of time to set for the expiration label
pc_maintainer          | No       | redhatci.ocp                                  | Value for catalog's image maintainer label
pc_ignore_pull_errors  | No       | false                                         | Makes the role fail if the image to prune is not available

## Requirements

The following application must be already present on the system.

- [Podman](https://podman.io/docs/installation)
- [skopeo](https://github.com/containers/skopeo/blob/main/install.md)
- [jq](https://docs.openshift.com/container-platform/latest/cli_reference/openshift_cli/getting-started-cli.html)

## Example of usage

Prune a list of operators
```yaml
- name: "Prune operators"
  include_role:
    name: redhatci.ocp.prune_catalog
  vars:
    pc_source_catalog: "registry.redhat.io/redhat/redhat-operator-index:v4.13"
    pc_destination_catalog: "<my-local-registry>:4443/pruned-catalog:latest"
    pc_operators:
      - compliance-operator
      - file-integrity-operator
      - cluster-logging
      - lvms-operator
      - advanced-cluster-management
    pc_opm_args: "--skip-tls-verify=true"
```

All channels for the listed operators are mirrored
```ShellSession
$ DOCKER_CONFIG=/home/<user>/.docker oc-mirror list operators --catalog <my-local-registry>:4443/pruned-catalog:latest --package compliance-operator
NAME                 DISPLAY NAME         DEFAULT CHANNEL
compliance-operator  Compliance Operator  stable

PACKAGE              CHANNEL      HEAD
compliance-operator  4.7          compliance-operator.v0.1.32
compliance-operator  release-0.1  compliance-operator.v0.1.61
compliance-operator  stable       compliance-operator.v1.3.1
```

Create a pruned catalog with specific channels
```yaml
- name: "Create a pruned catalog with specific channels"
  include_role:
    name: redhatci.ocp.prune_catalog
  vars:
    pc_source_catalog: "registry.redhat.io/redhat/redhat-operator-index:v4.13"
    pc_destination_catalog: "<my-local-registry>:4443/pruned-catalog:latest"
    pc_operators:
      compliance-operator:
        channel: stable
      file-integrity-operator:
        channel: stable
      cluster-logging:
        channel: stable
    pc_opm_args: "--skip-tls-verify=true"
```

Only the specified channel of the operators are kept in the catalog
```ShellSession
$ DOCKER_CONFIG=/home/<user>/.docker oc-mirror list operators --catalog <my-local-registry>:4443/pruned-catalog:latest 
NAME                     DISPLAY NAME               DEFAULT CHANNEL
cluster-logging          Red Hat OpenShift Logging  stable
compliance-operator      Compliance Operator        stable
file-integrity-operator  File Integrity Operator    stable

$ DOCKER_CONFIG=/home/<user>/.docker oc-mirror list operators --catalog <my-local-registry>:4443/pruned-catalog:latest --package compliance-operator
NAME                 DISPLAY NAME         DEFAULT CHANNEL
compliance-operator  Compliance Operator  stable

PACKAGE              CHANNEL  HEAD
compliance-operator  stable   compliance-operator.v1.3.1
```

Another example of a pruned catalog with specific channels
```yaml
- name: "Create a pruned catalog with custom channels"
  include_role:
    name: redhatci.ocp.prune_catalog
  vars:
    pc_source_catalog: "registry.redhat.io/redhat/redhat-operator-index:v4.13"
    pc_destination_catalog: "<my-local-registry>:4443/pruned-catalog:latest"
    pc_operators:
      compliance-operator:
      file-integrity-operator:
        channel: stable
      cluster-logging:
        channel: cluster-logging.v5.8.0
    pc_opm_args: "--skip-tls-verify=true"
```

In this example, the resulting catalog contains all the channels of the `compliance-operator`, channel `stable-5.8` for cluster-logging and only the `stable` channel for `file-integrity-operator`.
```ShellSession
$ DOCKER_CONFIG=/home/<user>/.docker oc-mirror list operators --catalog <my-local-registry>:4443/pruned-catalog:latest
NAME                     DISPLAY NAME               DEFAULT CHANNEL
cluster-logging          Red Hat OpenShift Logging  stable-5.8
compliance-operator      Compliance Operator        stable
file-integrity-operator  File Integrity Operator    stable

$DOCKER_CONFIG=/home/<user>/.docker oc-mirror list operators --catalog <my-local-registry>:4443/pruned-catalog:latest --package file-integrity-operator
NAME                 DISPLAY NAME         DEFAULT CHANNEL
compliance-operator  Compliance Operator  stable

PACKAGE              CHANNEL      HEAD
compliance-operator  4.7          compliance-operator.v0.1.32
compliance-operator  release-0.1  compliance-operator.v0.1.61
compliance-operator  stable       compliance-operator.v1.3.1

$ DOCKER_CONFIG=/home/<user>/.docker oc-mirror list operators --catalog r<my-local-registry>:4443/pruned-catalog:latest --package file-integrity-operator
NAME                     DISPLAY NAME             DEFAULT CHANNEL
file-integrity-operator  File Integrity Operator  stable

PACKAGE                  CHANNEL  HEAD
file-integrity-operator  stable   file-integrity-operator.v1.3.3
```

### Catalog inspection

To keep specific channels, it is required to inspect the source catalog to identify the available channels. `oc-mirror` can be used to perform the task. Example:

```ShellSession
$ DOCKER_CONFIG=/home/<user>/.docker oc-mirror list operators --catalog registry.redhat.io/redhat/redhat-operator-index:v4.14 --package cluster-logging
NAME             DISPLAY NAME               DEFAULT CHANNEL
cluster-logging  Red Hat OpenShift Logging  stable-5.8

PACKAGE          CHANNEL     HEAD
cluster-logging  stable      cluster-logging.v5.8.0
cluster-logging  stable-5.7  cluster-logging.v5.7.8
cluster-logging  stable-5.8  cluster-logging.v5.8.
```

## Authentication

This role uses [skopeo](https://github.com/containers/skopeo) and [opm](https://github.com/operator-framework/operator-registry) to obtain the container image's metadata. If registry authentication is required, please pass `DOCKER_CONFIG` as an environment variable to the role pointing to the directory that contains the `config.json` file with the proper authentication strings. See [docker-config](https://www.systutorials.com/docs/linux/man/5-docker-config-json/).

The following applications must be already present in the system.
