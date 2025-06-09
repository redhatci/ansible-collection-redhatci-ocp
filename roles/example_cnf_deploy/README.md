# example_cnf_deploy

This role allows the deployment of example-cnf on OCP, a DPDK-based application. See the main project [here](https://github.com/openshift-kni/example-cnf).

The DPDK workload to be launched could be either [TestPMD](https://doc.dpdk.org/guides/testpmd_app_ug/) or [Grout](https://github.com/DPDK/grout/) (default one). It can be switched with `ecd_cnfapp_name` variable.

## Prerequisites

OpenShift >=4.14 Cluster with at least 3 worker nodes should be deployed with additional operators:

- SR-IOV operator should be deployed and necessary resources for `SriovNetworkNodePolicy` and `SriovNetwork` should be created with target namespace (default namespace used to deploy example-cnf is `example-cnf`).
- Node Tuning Operator should be deployed and a `PerformanceProfile` should be created.

Also, exported `kubeconfig` file is required to run the Ansible tasks on the target cluster.

## Variables

| Variable                              | Default                                                                                         | Required | Description                                                                                     |
|---------------------------------------|-------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------|
| ecd_action                            | None                                                                                            | yes      | Defines which actions to perform. Possible values: ['catalog', 'deploy', 'validate', 'deploy_extra_trex', 'draining'] |
| ecd_cnf_namespace                     | example-cnf                                                                                     | no       | Name of the namespace where example-cnf is deployed |
| ecd_registry_url                      | quay.io                                                                                         | no       | Registry URL |
| ecd_repo_name                         | rh-nfv-int                                                                                      | no       | Repository name |
| ecd_catalog_name                      | nfv-example-cnf-catalog                                                                         | no       | Catalog name |
| ecd_operator_version                  | ""                                                                                              | yes      | Version of the index to be used |
| ecd_catalog_image                     | "{{ ecd_registry_url }}/{{ ecd_repo_name }}/{{ ecd_catalog_name }}:{{ ecd_operator_version }}"  | no       | Index image to be used |
| ecd_image_pull_policy                 | IfNotPresent                                                                                    | no       | Pull policy used for the images to be deployed |
| ecd_oc_path                           | /usr/local/bin/oc                                                                               | no       | File path to find the oc binary |
| ecd_opm_path                          | /usr/local/bin/opm                                                                              | no       | File path to find the opm binary |
| ecd_job_logs_path                     | /tmp                                                                                            | no       | File path to find the logs folder |
| ecd_cnfapp_name                       | grout                                                                                           | no       | CNFApp to be used. Could be "grout" or "testpmd" |
| ecd_enable_testpmd                    | false                                                                                           | no       | Enable TestPMD, one of the possible CNFApp you can launch with example-cnf. It is false by default because default CNFApp is grout |
| ecd_enable_grout                      | true                                                                                            | no       | Enable Grout, one of the possible CNFApp you can launch with example-cnf. This is the default CNFApp |
| ecd_enable_trex                       | true                                                                                            | no       | Enable TRex server, to send traffic to TestPMD |
| ecd_enable_trex_app                   | true                                                                                            | no       | Enable TRex application, to manage the creation of TRex jobs and profiles |
| ecd_testpmd_channel                   | alpha                                                                                           | no       | TestPMD operators channel |
| ecd_grout_channel                     | alpha                                                                                           | no       | Grout operator channel |
| ecd_trex_channel                      | alpha                                                                                           | no       | TRex operator channel |
| ecd_network_config_file               | ""                                                                                              | no       | (Required for Grout deployment) Path to the network configuration file to be used to set the IP and MAC addresses for each interface of both CNFApp and TRex. You can check an example on [this section](#network-configuration). If not providing a file and using TestPMD as CNFApp, default IP-MAC addresses will be used: no IP addresses, and MAC addresses defined on `ecd_trex_mac_list` and `ecd_cnfapp_mac_list` default values
| ecd_trex_mac_list                     | ["20:04:0f:f1:89:01","20:04:0f:f1:89:02"]                                                       | no       | Default static MAC addresses used by TRex (if providing `ecd_network_config_file`, they are updated) |
| ecd_cnfapp_mac_list                   | ["80:04:0f:f1:89:01","80:04:0f:f1:89:02"]                                                       | no       | Default static MAC addresses used by CNFApp (if providing `ecd_network_config_file`, they are updated) |
| ecd_trex_ip_list                      | ["",""]                                                                                         | no       | No default static IP addresses are provided for TRex by default. To update them, they must be provided on `ecd_network_config_file` (just required when using Grout, optional for TestPMD since it is launched on MAC forwarding mode) |
| ecd_cnfapp_ip_list                    | ["",""]                                                                                         | no       | No default static IP addresses are provided for CNFApp by default. To update them, they must be provided on `ecd_network_config_file` (just required when using Grout, optional for TestPMD since it is launched on MAC forwarding mode) |
| ecd_sriov_networks                    | []                                                                                              | yes      | SRIOV networks used in the connection between TRex and CNF Application, together with the number of interfaces to be used per network. See example above
| ecd_networks_cnfapp                   | []                                                                                              | no       | Networks for CNFApp, including MAC addresses and (if provided) IP addresses |
| ecd_networks_trex                     | []                                                                                              | no       | Networks for TRex, including MAC addresses and (if provided) IP addresses |
| ecd_run_deployment                    | 1                                                                                               | no       | Run all deployment automation. If different than 1, the automation will only create the pods and prepare the scripts to launch testpmd/grout and trex manually afterwards |
| ecd_enable_privileged_mode            | false                                                                                           | no       | Enable container privileged mode, instead of setting specific capabilities. This is required when using Mellanox cards, because it requires access to /dev/vfio/vfio from host since it uses netdevice instead of vfio-pci. To achieve that, using a volume with hostPath is not enough, so that privileged mode is required (see [this](https://access.redhat.com/solutions/6560521) for an example of this). |
| ecd_termination_grace_period_seconds  | 30                                                                                              | no       | Termination grace period for TestPMD |
| ecd_testpmd_reduced_mode              | 0                                                                                               | no       | Use reduced mode for TestPMD (if different than 0), where only three cores are used, and txd/rxd parameters are doubled |
| ecd_trex_test_config                  | []                                                                                              | no       | TRex test configuration. See an example below |
| ecd_trex_cr_name                      | trexconfig                                                                                      | no       | Name of the TRex CR |
| ecd_trex_app_cr_name                  | trex-app                                                                                        | no       | Name of the TRexApp CR |
| ecd_trex_duration                     | 120                                                                                             | no       | TRex job duration. If set to -1, it will run in continuous burst mode |
| ecd_trex_packet_rate                  | 10kpps                                                                                          | no       | TRex packet rate, in packets per second. Note the amount of bits sent per second cannot exceed the link capacity, else TRexApp job will fail |
| ecd_trex_packet_size                  | 64                                                                                              | no       | TRex packet size, in bytes |
| ecd_default_trex_duration             | 1800                                                                                            | no       | Default duration of TRex execution during draining validation |
| ecd_packet_rate                       | 10kpps                                                                                          | no       | Default packet rate from TRex |
| ecd_trex_core_count                   | 0                                                                                               | no       | Variable that can be used to restrict the cores that TRex uses to create tx queues |
| ecd_trex_continuous_mode              | false                                                                                           | no       | If set to true, the automation behaves as if TRex job is deployed in continuous mode |
| ecd_trex_tests_wait                   | true                                                                                            | no       | If set to true, wait until the end of the profile duration before continue |
| ecd_trex_app_run_passed               | false                                                                                           | no       | By default, till having a positive result, it is supposed that TRex job failed |
| ecd_trex_job_failed                   | false                                                                                           | no       | Track if TRex job has failed or not |
| ecd_trex_tests_skip_failures          | false                                                                                           | no       | If set to true, even if TRex job fails, the job will progress |
| ecd_try_running_migration_tests       | true                                                                                            | no       | The idea is always to try to run the migration test, unless TRex job failed before |
| ecd_numa_aware_topology               | None                                                                                            | no       | If defined, allows to provide the NUMA aware topology for TestPMD/Grout and TRexServer CRs |
| ecd_high_perf_runtime                 | None                                                                                            | no       | If defined, allows to provide the RuntimeClass name for TestPMD/Grout, TRexApp and TRexServer CRs |
| ecd_trex_app_version                  | None                                                                                            | yes      | TRexApp version, required in deploy_extra_trex action |

## SR-IOV configuration

Here is an example of the `SriovNetworkNodePolicy` and `SriovNetwork` configuration that can be passed to [redhatci.ocp.sriov_config](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/sriov_config/README.md) role, if using L3 network configuration. Note the proper network configuration must be applied to your network devices to match with the SR-IOV configuration proposed:

```yaml
---
sriov_network_configs:
  - resource: example_cnf_res1
    node_policy:
      name: example-cnf-policy1
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
  - resource: example_cnf_res1
    network:
      name: example-cnf-net1
      network_namespace: example-cnf
      spoof_chk: "off"
      trust: "on"
      vlan: 407
      capabilities: '{"mac": true, "ips": true}'
      ipam: '{"type": "static"}'
```

If using L2 network configuration (only allowed for TestPMD), you need to change the SriovNetwork resource description not to use IP configuration; so, moving from:

```yaml
      capabilities: '{"mac": true, "ips": true}'
      ipam: '{"type": "static"}'
```

to:

```yaml
      capabilities: '{"mac": true}'
```

This configuration is related to Intel cards. If you are using other type of cards, you need to apply the corresponding modifications (`device_id` and `vendor` will change, among others). For example, [for Mellanox cards](https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/networking/hardware-networks#example-vf-use-in-dpdk-mode-mellanox_using-dpdk-and-rdma), you need to use `netdevice` instead of `vfio-pci`, and also enable RDMA (`is_rdma: true`). It's also recommended to use `need_vhost_net: true`, and in case you want to include RDMA subsystem, you can do it with `meta_plugins: '{"type": "rdma"}'`.

> Remember that Mellanox requires containers to run in privileged mode. Enable it with `ecd_enable_privileged_mode: true`.

### NIC support

The deployment is fully compliant with Intel NICs.

However, we found difficulties when trying to test Mellanox NICs with TRex pod. With the current setup, when launching TRex, it's not able to find the requested interfaces.

According to TRex documentation, [OFED driver](https://trex-tgn.cisco.com/trex/doc/trex_appendix_mellanox.html) should be required. Its deployment in an OpenShift cluster is out of the scope of this project and has not been fully validated, so it's not guaranteed that Mellanox NICs can be used with the TRex pod. Only DPDK-related pods (Grout and TestPMD) can be deployed without any problem.

## Network configuration

To apply a proper network configuration for both CNFApp and TRex, you need to follow a YAML structure like this, to be provided in a file pointed by `ecd_network_config_file` (e.g. `/path/to/net-config.yml`). This is just required when using Grout, since TestPMD acts in MAC forwarding mode, so no IP addresses are required for it (but you can define them anyway, only thing is that they're not going to be considered for traffic forwarding):

```yaml
ecd_network_config:
  cnfapp:
    net1:
      mac: 80:04:0f:f1:89:01
      ip: 172.16.16.60/24
    net2:
      mac: 80:04:0f:f1:89:02
      ip: 172.16.21.60/24
  trex:
    net1:
      mac: 20:04:0f:f1:89:01
      ip: 172.16.16.61/24
    net2:
      mac: 20:04:0f:f1:89:02
      ip: 172.16.21.61/24
```

Remember that each container is deployed with two network interfaces attached to VFs. For each of them, you can specify the IP and the MAC address.

## TRex extra profiles

These profiles can be configured by using the `ecd_trex_test_config` variable, so that you can manage to launch several TRexApp jobs with different TRex setups:

```yaml
# When duration is '-1', the trex will run in continous burst mode
ecd_trex_test_config:
  - name: pkt-64-10kpps
    packet_size: 64
    packet_rate: 10kpps
    duration: 120
    trex_profile_name: ''
    trex_profile_path: ''
    trex_profile_cm_name: ''
```

## Actions

Each action allows you to do different operations with the example-cnf workload:

- catalog: builds the example-cnf catalog.
- deploy: allows you to deploy the example-cnf operators and workloads.
- validate: performs validations to the example-cnf workloads to address specific scenarios, e.g. validations after cluster upgrade.
- deploy_extra_trex: gives you the chance to create a new TRex job, in an already deployed example-cnf instance.
- draining: while a TRex job is running, runs a node cordoning-draining, selecting the node where TestPMD is running, then it measures the downtime in the TRex job and the packet loss.

> deploy_extra_trex and draining actions require TestPMD to be the CNFApp that is deployed in the cluster.

### Examples

- catalog action:

```yaml
---
- name: Deploy NFV Example CNF catalog
  vars:
    ecd_action: "catalog"
    ecd_operator_version: "{{ operator_version }}"
  include_role:
    name: redhatci.ocp.example_cnf_deploy
```

- deploy action:

```yaml
---
- name: Deploy the Example CNF applications
  vars:
    ecd_action: "deploy"
    ecd_sriov_networks:
      - name: example-cnf-net1
        count: 1
      - name: example-cnf-net2
        count: 1
    ecd_operator_version: "latest"
    ecd_high_perf_runtime: "performance-blueprint"
    ecd_cnfapp_name: "grout"
    ecd_network_config_file: /path/to/net-config.yml
  include_role:
    name: redhatci.ocp.example_cnf_deploy
```

- validate action:

```yaml
---
- name: Run migration test
  vars:
    ecd_action: "validate"
    ecd_cnfapp_name: "grout"
  include_role:
    name: redhatci.ocp.example_cnf_deploy
```

- deploy_extra_trex action:

```yaml
---
- name: Run a new TRex job
  vars:
    ecd_action: "deploy_extra_trex"
    ecd_trex_app_cr_name: "trex-app-new"
    ecd_trex_app_version: "trex-app-version"
    ecd_cnfapp_name: "testpmd"
  include_role:
    name: redhatci.ocp.example_cnf_deploy
```

- draining action:

```yaml
---
- name: "Perform node draining process"
  vars:
    ecd_action: "draining"
    ecd_trex_app_cr_name: "trex-app-new"
    ecd_cnfapp_name: "testpmd"
  include_role:
    name: redhatci.ocp.example_cnf_deploy
```
