# eco_gotests

This role runs [eco-gotests](https://github.com/rh-ecosystem-edge/eco-gotests) for OpenShift CNF (Cloud Native Functions) testing, specifically for PTP (Precision Time Protocol) and SRIOV (Single Root I/O Virtualization) test suites.

## Requirements

- Podman installed on the target system
- Access to the eco-gotests container image
- Valid kubeconfig for the OpenShift cluster

### PTP requirements

- The ptp-operator has to be installed
- Need apiVersion set to 2 on PtpOperatorConfig

## Role Variables

### Required Variables

- `eco_gotests_test_suites`: List of test suites to run (e.g., `['ptp', 'sriov']`)
- `eco_gotests_log_dir`: Path where test logs and reports will be stored
- `eco_gotests_kubconfig_dir`: Directory containing kubeconfig files
- `eco_gotests_registry_auth_file`: Path to the registry authentication file

### Optional Variables

#### General Configuration
- `eco_gotests_image` (default: `"quay.io/ocp-edge-qe/eco-gotests:latest"`): Container image for eco-gotests
- `eco_gotests_path` (default: undefined): path where to find the source code to build the container. If this is specified, the `eco_gotests_image` is ignored.

#### SRIOV Test Configuration
- `eco_gotests_sriov_labels` (default: `"sriov-hw-enabled"`): Test labels for SRIOV tests
- `eco_gotests_worker_label` (default: `"worker"`): Worker node label
- `eco_gotests_sriov_interface_list` (default: `"ens3f0np0,ens3f1np1"`): SRIOV interface list
- `eco_gotests_network_test_container` (default: `"quay.io/ocp-edge-qe/eco-gotests-network-client:v4.19"`): Network test container
- `eco_gotests_dpdk_test_container` (default: `"quay.io/ocp-edge-qe/eco-gotests-rootless-dpdk:v4.16.0"`): DPDK test container
- `eco_gotests_frr_image` (default: `"quay.io/ocp-edge-qe/frr:stable_7.5"`): FRR image
- `eco_gotests_sriov_timeout` (default: `"12h"`): Timeout for SRIOV tests
- `eco_gotests_reports_dump_dir` (default: `"/tmp/reports"`): Directory for dumping reports
- `eco_gotests_verbose_level` (default: `100`): Verbosity level
- `eco_gotests_test_verbose` (default: `true`): Enable verbose test output
- `eco_gotests_dump_failed_tests` (default: `true`): Dump failed test information

## Example Playbook

```yaml
---
- name: Run eco-gotests for PTP and SRIOV
  hosts: localhost
  gather_facts: false
  vars:
    eco_gotests_test_suites: ['ptp', 'sriov']
    eco_gotests_kubconfig_dir: /home/user/clusterconfigs
    eco_gotests_registry_auth_file: /home/user/pull-secret.json
  roles:
    - redhatci.ocp.eco_gotests
```

## Example with Custom Configuration

```yaml
---
- name: Run eco-gotests with custom settings
  hosts: localhost
  gather_facts: false
  vars:
    eco_gotests_test_suites: ['sriov']
    eco_gotests_sriov_interface_list: "ens1f0,ens1f1"
    eco_gotests_worker_label: "cnf-worker"
  roles:
    - redhatci.ocp.eco_gotests
```
