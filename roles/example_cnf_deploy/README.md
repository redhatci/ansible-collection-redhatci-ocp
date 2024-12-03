# example_cnf_deploy

This role allows the deployment of example-cnf on OCP, a DPDK based application. See the main project [here](https://github.com/openshift-kni/example-cnf)

## Prerequisites

OpenShift 4 Cluster with at least 3 worker nodes should be deployed with additional operators:

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
| ecd_enable_mac_fetch                  | true                                                                                            | no       | Enable MAC fetch, which implies the creation of the CNFAppMac CR |
| ecd_enable_testpmd                    | true                                                                                            | no       | Enable TestPMD, also known as CNFApp |
| ecd_enable_trex                       | true                                                                                            | no       | Enable TRex server, to send traffic to TestPMD |
| ecd_enable_trex_app                   | true                                                                                            | no       | Enable TRex application, to manage the creation of TRex jobs and profiles |
| ecd_testpmd_channel                   | alpha                                                                                           | no       | TestPMD operators channel |
| ecd_trex_channel                      | alpha                                                                                           | no       | TRex operator channel |
| ecd_trex_mac_list                     | ["20:04:0f:f1:89:01","20:04:0f:f1:89:02"]                                                       | no       | Static MAC addresses used by TRex |
| ecd_testpmd_app_mac_list              | ["80:04:0f:f1:89:01","80:04:0f:f1:89:02"]                                                       | no       | Static MAC addresses used by CNFApp |
| ecd_sriov_networks                    | []                                                                                              | yes      | SRIOV networks used in the connection between TRex and CNF Application, together with the number of interfaces to be used per network. See example above
| ecd_networks_testpmd_app              | []                                                                                              | no       | Networks for the CNF, including the hardcoded MAC addresses |
| ecd_termination_grace_period_seconds  | 30                                                                                              | no       | Termination grace period for TestPMD |
| ecd_trex_test_config                  | []                                                                                              | no       | TRex test configuration. See an example below |
| ecd_trex_cr_name                      | trexconfig                                                                                      | no       | Name of the TRex CR |
| ecd_trex_app_cr_name                  | trex-app                                                                                        | no       | Name of the TRexApp CR |
| ecd_trex_duration                     | 120                                                                                             | no       | Main TRexApp job duration. If set to -1, it will run in continuous burst mode |
| ecd_default_trex_duration             | 1800                                                                                            | no       | Default duration of TRex execution |
| ecd_packet_rate                       | 10kpps                                                                                          | no       | Default packet rate from TRex |
| ecd_trex_core_count                   | 0                                                                                               | no       | Variable that can be used to restrict the cores that TRex uses to create tx queues |
| ecd_trex_continuous_mode              | false                                                                                           | no       | If set to true, the automation behaves as if TRex job is deployed in continuous mode |
| ecd_trex_tests_wait                   | true                                                                                            | no       | If set to true, wait until the end of the profile duration before continue |
| ecd_trex_app_run_passed               | false                                                                                           | no       | By default, till having a positive result, it is supposed that TRex job failed |
| ecd_trex_job_failed                   | false                                                                                           | no       | Track if TRex job has failed or not |
| ecd_trex_tests_skip_failures          | false                                                                                           | no       | If set to true, even if TRex job fails, the job will progress |
| ecd_try_running_migration_tests       | true                                                                                            | no       | The idea is always to try to run the migration test, unless TRex job failed before |
| ecd_numa_aware_topology               | None                                                                                            | no       | If defined, allows to provide the NUMA aware topology for TestPMD and TRexServer CRs |
| ecd_high_perf_runtime                 | None                                                                                            | no       | If defined, allows to provide the RuntimeClass name for TestPMD, TRexApp and TRexServer CRs |
| ecd_trex_app_version                  | None                                                                                            | yes      | TRexApp version, required in deploy_extra_trex action |

## SR-IOV configuration

Here is an example of the `SriovNetworkNodePolicy` and `SriovNetwork` configuration that can be passed to [redhatci.ocp.sriov_config](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/sriov_config/README.md) role. Note the proper network configuration must be applied to your network devices to match with the SR-IOV configuration proposed:

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
  include_role:
    name: redhatci.ocp.example_cnf_deploy
```

- validate action:

```yaml
---
- name: Run migration test
  vars:
    ecd_action: "validate"
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
  include_role:
    name: redhatci.ocp.example_cnf_deploy
```
