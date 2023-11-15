# prune_catalog role

A role to prune a File Base Catalogs (FBC), based on a list of required operators.

By default, the catalog image sets a label "quay.expires-after" to define an expiration. The label can be removed or the time can be modified as needed.

## Parameters

Name                   | Required | Default                                       | Description
-----------------------|----------|---------------------------------------------- |-------------
pc_source_catalog      | Yes      |                                               | Source catalog to be pruned
pc_destination_catalog | Yes      |                                               | Catalog containing the required operators
pc_operators_list      | Yes      |                                               | List of operators to include in the pruned catalog
pc_opm_args            | No       | ""                                            | Arguments for opm command. Those will be applied globally for all opm calls
pc_opm_auths           | No       | /usr/share/dci-openshift-agent/utils/opm-auths| Path to opm-auths a wrapper script to allow multi-registry auths in opm
pc_expire              | No       | false                                         | Whether or not to set an expiration label on the catalog
pc_expire_time         | No       | 5h                                            | The amount of time to set for the expiration label

## Requirements

The following application must be already present on the system.

* Podman
* jq
* skopeo

## Example of usage

```yaml
- name: "Prune a catalog"
  include_role:
    name: redhatci.ocp.prune_catalog
  vars:
    pc_source_catalog: "registry.redhat.io/redhat/redhat-operator-index:v4.13"
    pc_destination_catalog: "<my-local-registry>:4443/pruned/redhat-operator-index:4.13"
    pc_operators_list:
      - compliance-operator
      - file-integrity-operator
      - cluster-logging
      - lvms-operator
      - advanced-cluster-management
    pc_opm_args: "--skip-tls-verify=true"
```

## Authentication

This role uses [skopeo](https://github.com/containers/skopeo) and [opm](https://github.com/operator-framework/operator-registry) to obtain the container image's metadata. If registry authentication is required, please pass `DOCKER_CONFIG` as an environment variable to the role pointing to the directory that contains the `config.json` file with the proper authentication strings. See [docker-config](https://www.systutorials.com/docs/linux/man/5-docker-config-json/).
