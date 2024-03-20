# sriov_config

Configure SR-IOV node policies and/or networks

## Requirements

SR-IOV Operator needs to be installed already in the cluster for this role to interact with it.

Nodes must have SR-IOV capable network interfaces.

## Variables

| Variable                      | Required  | Type    | Default   | Description
| ----------------------------- | --------- | ------- | --------- | -----------
| sriov_config_file             | Yes       | String  | Undefined | The configuration file for SR-IOV Node policy and/or network.
| sriov_config_wait_node_policy | No        | Boolean | True      | Whether or not wait for node policies to apply
| sriov_config_wait_network     | No        | Boolean | True      | Whether or not wait for networks to apply the proper NetworkAttachmentDefinition resources
| sriov_config_retries_per_node | No        | Int     | 60        | Number of retries for Node readiness
| sriov_config_delay_per_node   | No        | Int     | 10        | Seconds to wait between retries for Node readiness

### SR-IOV Network configs

The `sriov_config_file` **must** meet the following requirements

| Variable              | Required  | Type    | Description
| --------------------- | --------- | ------- | -----------
| sriov_network_configs | Yes       | String  | Single variable including the Resource name and the SR-IOV Node Policies and/or Network configurations.
| resource              | Yes       | String  | The name of the resource created by SR-IOV Node Policy and the name to be consumed by the SR-IOV Network.
| node_policy           | See Note  | String  | The SR-IOV Node Policy to create a resource consumed by the SR-IOV Network.
| network               | See Note  | String  | The SR-IOV Network using the resource form the Node Policy.

> NOTE:
> - It's possible to omit a SR-IOV `network` when only a `node_policy` is applied.
> - It's possible to omit a `node_policy` when the SR-IOV `network` to apply is mapped to an existing SR-IOV Network Node Policy

#### SR-IOV Node Policy

| Variable         | Required | Type    | Description
| ---------------- | -------- | ------- | -----------
| name             | Yes      | String  | Name of the SR-IOV Network Node Policy.
| device_type      | No       | String  | The driver type for configured VFs. Allowed value "netdevice", "vfio-pci".
| e_switch_mode     | No       | String  | NIC Device Mode. Allowed value "legacy","switchdev".
| exclude_topology | No       | Boolean | Exclude device's NUMA node when advertising this resource by SR-IOV network device plugin.
| is_rdma          | No       | Boolean | RDMA mode.
| link_type        | No       | String  | NIC Link Type. Allowed value "eth", "ETH", "ib", and "IB"
| mtu              | No       | Int     | MTU of VF.
| need_vhost_net   | No       | Boolean | Mount vhost-net device
| nic_selector     | Yes      | List    | List of NICs to configure, see table below
| node_selector    | No       | Dict    | Selects the nodes to be configured. Default: `"node-role.kubernetes.io/worker": ""`
| num_vfs          | Yes      | Int     | Number of VFs for each PF
| priority         | No       | Int     | Priority of the policy, higher priority policies can override lower ones
| vdpa_type        | No       | String  | VDPA device type. Allowed value "virtio", "vhost"

#### NIC Selector

| Variable     | Required | Type    | Description
| ------------ | -------- | ------- | -----------
| device_id    | Yes      | String  | The device hex code of SR-IoV device. Allowed value "0d58", "1572", "158b", "1013", "1015", "1017", "101b".
| net_filter   | No       | String  | Infrastructure Networking selection filter. Allowed value "openstack/NetworkID:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
| pf_names     | Yes      | List    | List of Names of SR-IoV PF.
| root_devices | No       | List    | List of PCI address of SR-IoV PF.
| vendor       | Yes      | String  | The vendor hex code of SR-IoV device. Allowed value "8086", "15b3".

### SR-IOV Network

| Variable          | Required | Type    | Description
| ----------------- | -------- | ------- | -----------
| name              | Yes      | String  | Name of the SR-IOV Network.
| capabilities      | No       | String  | Capabilities to be configured for this network.
| ipam              | No       | String  | IPAM configuration to be used for this network.
| link_state        | No       | String  | VF link state (enable|disable|auto).
| max_tx_rate       | No       | Int     | Maximum tx rate, in Mbps, for the VF.
| meta_plugins      | No       | String  | MetaPluginsConfig configuration to be used in order to chain metaplugins to the sriov interface returned by the operator.
| min_tx_rate       | No       | Int     | Minimum tx rate, in Mbps, for the VF, min_tx_rate should be <= max_tx_rate.
| network_namespace | No       | String  | Namespace of the NetworkAttachmentDefinition custom resource
| spoof_chk         | No       | String  | VF spoof check, (on|off)
| trust             | No       | String  | VF trust mode (on|off)
| vlan              | No       | Int     | VLAN ID to assign for the VF.
| vlan_qos          | No       | Int     | VLAN QoS ID to assign for the VF.

## Examples

### Using the role

```yaml
- name: "Configure SR-IOV"
  ansible.builtin.include_role:
    name: redhatci.ocp.sriov_config
  vars:
    sriov_config_file: /path/to/sriov-config-file.yaml
```

### Configuration file

#### SR-IOV Node policy and network

A Node Policy and a Network configuration using the same resource `sriov_port0`:

```YAML
sriov_network_configs:
  - resource: sriov_port0
    node_policy:
      name: sriov-policy0
      device_type: vfio-pci
      is_rdma: true
      mtu: 9000
      nic_selector:
        device_id: "1017"
        pf_names:
          - ens2f1#0-15
        root_devices:
          - "0000:12:00.0"
        vendor: "15b3"
      node_selector:
        node-role.kubernetes.io/sriov: ""
      num_vfs: 16
      priority: 99
    network:
      name: sriov-net0
      vlan: 10
      network_namespace: my-app-namespace
      spoof_chk: on
      trust: on
      capabilities: '{ "mac": true, "ips": true }'
```

> NOTE: SR-IOV operator requires nodes to use the `worker` role.
> Additional tags are valid as long as those nodes are also `workers`

#### SR-IOV Node Policy

A singel Node Policy for a resource called `intel_port0`

```YAML
sriov_network_configs:
  - resource: intel_port0
    node_policy:
      name: intel-i40e-p0
      device_type: vfio-pci
      mtu: 9000
      nic_selector:
        device_id: 1592
        pf_names:
          - ens3f0#0-8
        vendor: 8086
      num_vfs: 8
```

#### SR-IOV Networks

Two network configurations tied to two node policies with the resources `sriov_port0` and `intel_port0`

```YAML
sriov_network_configs:
  - resource: sriov_port0
    network:
      name: sriov-net1
      vlan: 20
      network_namespace: my-dev-namespace
      trust: on
  - resource: intel_port0
    network:
      name: intel-net1
      vlan: 21
      network_namespace: my-test-namespace
      spoof_chk: on
```
