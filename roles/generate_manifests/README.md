# generate_manifests role

Generates the manifests required for openshift_installer's agent sub-command

## Variables

All of the variables have sane defaults which you can override to force things, but you shouldn't need to

| Variable                      | Default                           | Required  | Description           |
| ----------------------------- | --------------------------------- | --------- | --------------------- |
| generated_dir                 | $REPO_ROOT_PATH/generated         | No        | Base path for all generated files |
| manifests_dir                 | $GENERATED_DIR/$CLUSTER_NAME      | No        | Path to store all rendered manifests |
| cluster_manifest_dir          | $MANIFESTS_DIR/cluster-manifests  | No        | Path for cluster manifests |
| extra_manifest_dir            | $MANIFESTS_DIR/openshift          | No        | Path for extra manifests |
| static_network_config         | {}                                | No        | Static network config for every node |
| root_device_hints             | {}                                | No        | Device Hints per node |
| use_local_mirror_registry     | true                              | No        | Use the configured mirror registry |
| mirror_registry               | $REGISTRY_HOST_FQDN:5000          | No        | Local container image mirror | | ocp_registry_namespace        | ocp4                              | No        | Namespace for image mirror |
| ocp_registry_image            | openshift4                        | No        | Name for image in the image mirror |
| single_node_openshift_enabled | false                             | No        | Install OCP in single-node mode |
