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
| installation_disk_path        |                                   | No        | Disk to use for install if you don't want the first found disk |
| root_device_hints             | {}                                | No        | Install device hints [^1] per node, in case installation_disk_path is not enough |
| use_local_mirror_registry     | true                              | No        | Use the configured mirror registry |
| mirror_registry               | $REGISTRY_HOST_FQDN:5000          | No        | Local container image mirror |
| ocp_registry_namespace        | ocp4                              | No        | Namespace for image mirror |
| ocp_registry_image            | openshift4                        | No        | Name for image in the image mirror |
| single_node_openshift_enabled | false                             | No        | Install OCP in single-node mode |

## Usage Examples

```yaml
- name: "Generate manifests"
  vars:
    static_network_config:  # if you want to specify static configuration
      mynode-1:
        mac_interface_map:
          - logical_nic_name: enp0s0
            mac_address: DE:AD:BE:EF:00:11
        network_yaml:
          # valid nmstate configuration in here
    installation_disk_path: /dev/sdb  # this maps to rootDeviceHints.deviceName
    root_device_hints:  # you can also use more specific device hints. This overrides installation_disk_path
      hctl: 0:0:0:1
      wwn: '0x5000000000'  # remember to quote hex values
  ansible.builtin.include_role:
    name: redhatci.ocp.generate_manifests
```

[^1]: As per the [OCP 4.17 docs](https://docs.redhat.com/en/documentation/openshift_container_platform/4.17/html-single/installing_an_on-premise_cluster_with_the_agent-based_installer/index#root-device-hints_preparing-to-install-with-agent-based-installer)
