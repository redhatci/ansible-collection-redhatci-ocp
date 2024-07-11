# Example-cnf Deploy role
This role allows the deployment of example-cnf on OCP, a DPDK based application. See the main project [here](https://github.com/openshift-kni/example-cnf)

## Prerequisites
OpenShift 4 Cluster should be deployed with additional operators:
 * SR-IOV operator should be deployed and necessary resources for
   `SriovNetworkNodePolicy` and `SriovNetwork` should be created with
   target namespace (default namespace used to deploy example-cnf
   is `example-cnf`).

 * Node Tuning Operator should be deployed and a `PerformanceProfile` should be created.

## Variables

| Variable                      | Default                                                          | Required | Description                                                                                    |
|-------------------------------|------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------|
| ecd_action                   | None                                                             | yes      | Defines which actions to perform. Possible values: ["deploy", "validate, "draining" "catalog"] |
| ecd_cnf_app_networks          | []                                                               | yes      | Connection between LB-CNF in LB mode (or TRex-CNF in direct mode)                              |
| ecd_packet_generator_networks | []                                                               | no       | Connection between TRex-LB in LB mode (not used in direct mode)                                |
| ecd_operator_version          | ""                                                               | yes      | Version of the index to be used                                                                |
| example_cnf_index_image       | quay.io/rh-nfv-int/nfv-example-cnf-catalog:{{ operator_version}} | yes      | Index image to be used                                                                         |
| cnf_namespace                 | "example-cnf"                                                    | no       | Name of the namespace where example-cnf is deployed                                            |                                                              |
| enable_lb                     | false                                                            | no       | [WIP] enabling a builtin loadbalancer                                                          |
| trex_duration                 | 120                                                              | no       | Main TRexApp job duration. If set to -1, it will run in continuous burst mode                  |

### SR-iov configuration
Here is an example of the `SriovNetworkNodePolicy` and `SriovNetwork` that is expected by the role:
```yaml
---
sriov_network_configs:
  - resource: intel_numa0_res1
    node_policy:
      name: intel-numa0-policy1
      device_type: vfio-pci
      is_rdma: false
      mtu: 9000
      nic_selector:
        device_id: 158b
        pf_names:
          - ens2f0#0-7
        vendor: "8086"
      node_selector:
        node-role.kubernetes.io/worker: ""
      num_vfs: 16
      priority: 99
  - resource: intel_numa0_res1
    network:
      name: intel-numa0-net1
      network_namespace: example-cnf
      spoof_chk: "off"
      trust: "on"
      vlan: 407
      capabilities: '{"mac": true}'
```