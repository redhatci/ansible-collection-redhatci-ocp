# eco_gotests

This role runs [eco-gotests](https://github.com/rh-ecosystem-edge/eco-gotests) for OpenShift CNF (Cloud Native Functions) testing. It supports PTP (Precision Time Protocol), SRIOV (Single Root I/O Virtualization), and a generic test runner for any eco-gotests feature with configurable label filtering.

## Requirements

- Podman installed on the target system
- Access to the eco-gotests container image
- Valid kubeconfig for the OpenShift cluster

### PTP requirements

- The ptp-operator has to be installed
- Need apiVersion set to 2 on PtpOperatorConfig

## Role Variables

### Required Variables

- `eco_gotests_test_suites`: List of test suites to run (e.g., `['ptp', 'sriov', 'generic']`)
- `eco_gotests_log_dir`: Path where test logs and reports will be stored
- `eco_gotests_kubeconfig_dir`: Directory containing kubeconfig files
- `eco_gotests_registry_auth_file`: Path to the registry authentication file

### Optional Variables

#### General Configuration
- `eco_gotests_image` (default: `"quay.io/ocp-edge-qe/eco-gotests:latest"`): Container image for eco-gotests
- `eco_gotests_run_labels_ptp` (default: `[]`): List of Ginkgo labels to **run** for PTP tests. When non-empty, only tests matching these labels are selected; multiple entries are combined with ` && ` (AND). When empty, no positive label filter is applied (all PTP tests in the suite are candidates, subject to skips). Common PTP labels include: `node-reboot`, `process-restart`, `event-consumer`, `events-and-metrics`, `interfaces`, `leap-file`, `ntp-fallback`. Example: `['events-and-metrics']` to run only that category.
- `eco_gotests_skip_labels_ptp` (default: `[]`): List of test labels to skip for PTP tests. These labels will be excluded using Ginkgo label filter syntax (`!label`). When combined with `eco_gotests_run_labels_ptp`, the effective filter is `run_label_1 && ... && !skip_label_1 && ...`. Common PTP labels are the same as above. Example: `['node-reboot', 'process-restart']` to skip node reboot and process restart tests.
- `eco_gotests_eco_test_features_ptp` (default: `"ptp"`): Value passed to the eco-gotests container as `ECO_TEST_FEATURES` for the PTP run. Override if you need a different feature selector supported by eco-gotests.
- `eco_gotests_ptp_check_prerequisites` (default: `true`): Enable or disable PTP prerequisites validation (`PtpOperatorConfig` checks for `enableEventPublisher` and `apiVersion`).
- `eco_gotests_ptp_run_timeout_sec` (default: `3600`): Maximum wall-clock time in **seconds** that the PTP test container is allowed to run. The role passes this to `containers.podman.podman_container` as `timeout` (Podman `--timeout`); the runtime stops the container when the limit is reached. The default is one hour.
- `eco_gotests_path` (default: undefined): path where to find the source code to build the container. If this is specified, the `eco_gotests_image` is ignored.
- `eco_gotests_dump_failed_tests` (default: `false`): When true, eco-gotests sets `ECO_DUMP_FAILED_TESTS` and writes per-failure logs and must-gather under the suite reports directory.

#### SRIOV Test Configuration
- `eco_gotests_eco_test_features_sriov` (default: `"sriov"`): Value passed to the eco-gotests container as `ECO_TEST_FEATURES` for the SRIOV run.
- `eco_gotests_run_labels_sriov` (default: `[]`): List of Ginkgo labels to **run** for SRIOV tests. When non-empty, only tests matching these labels are selected; multiple entries are combined with ` || ` (OR). When empty, no positive label filter is applied (all SRIOV tests in the suite are candidates, subject to skips). Common SRIOV labels include: `sriov`, `sriov-hw-enabled`, `externallymanaged`, `paralleldraining`, `qinq`, `exposemtu`, `sriovmetrics`, `rdmametricsapi`, `mlxsecureboot`, `webhook-resource-injector`, `sriovnet-app-ns`. Example: `['qinq']` to run only QinQ tests.
- `eco_gotests_skip_labels_sriov` (default: `[]`): List of test labels to skip for SRIOV tests. These labels will be excluded using Ginkgo label filter syntax (`!label`). When combined with `eco_gotests_run_labels_sriov`, the effective filter is `run_label_1 || ... && !skip_label_1 && ...`. Common SRIOV labels are the same as above. Example: `['paralleldraining', 'mlxsecureboot']` to skip parallel draining and Mellanox secure boot tests.
- `eco_gotests_sriov_labels` (default: `"sriov-hw-enabled"`): Test labels for SRIOV tests
- `eco_gotests_worker_label` (default: `"worker"`): Worker node label
- `eco_gotests_sriov_interface_list` (default: `"ens3f0np0,ens3f1np1"`): SRIOV interface list
- `eco_gotests_network_test_container` (default: `"quay.io/ocp-edge-qe/eco-gotests-network-client:v4.19"`): Network test container
- `eco_gotests_dpdk_test_container` (default: `"quay.io/ocp-edge-qe/eco-gotests-rootless-dpdk:v4.16.0"`): DPDK test container
- `eco_gotests_frr_image` (default: `"quay.io/ocp-edge-qe/frr:stable_7.5"`): FRR image
- `eco_gotests_sriov_timeout` (default: `"12h"`): Timeout for SRIOV tests
- `eco_gotests_verbose_level` (default: `100`): Verbosity level
- `eco_gotests_test_verbose` (default: `true`): Enable verbose test output

SRIOV uses the same `eco_gotests_dump_failed_tests` toggle; reports are written at `/tmp/reports` in the container, mapped to `{{ eco_gotests_log_dir }}/eco_gotests/sriov` on the host.

#### Generic Test Runner Configuration
- `eco_gotests_generic_features` (default: `''`): The ECO_TEST_FEATURES value (e.g., `'network'`, `'ran'`). **Required** when using `'generic'` in `eco_gotests_test_suites`.
- `eco_gotests_generic_run_labels` (default: `[]`): List of Ginkgo labels to run (joined with `||`). Example: `['lacp-bond-stability']`.
- `eco_gotests_generic_skip_labels` (default: `[]`): List of Ginkgo labels to skip (prefixed with `!` and joined with `&&`).
- `eco_gotests_generic_env` (default: `{}`): Additional environment variables to pass to the container. Merged on top of the base environment using `combine()`.
- `eco_gotests_generic_timeout` (default: `'12h'`): Timeout for the test run.
- `eco_gotests_generic_run_label_operator` (default: `'||'`): Operator used to join run labels. Use `'||'` for OR semantics (default) or `'&&'` for AND semantics (used internally by PTP).

> **Note:** PTP and SRIOV test suites now delegate to the generic runner internally. All PTP/SRIOV user-facing variables remain unchanged — they are mapped to generic runner variables automatically.

## Example Playbook

```yaml
---
- name: Run eco-gotests for PTP and SRIOV
  hosts: localhost
  gather_facts: false
  vars:
    eco_gotests_test_suites: ['ptp', 'sriov']
    eco_gotests_kubeconfig_dir: /home/user/clusterconfigs
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

## Example with Skipped Tests

```yaml
---
- name: Run eco-gotests skipping specific test categories
  hosts: localhost
  gather_facts: false
  vars:
    eco_gotests_test_suites: ['ptp']
    eco_gotests_skip_labels_ptp: ['node-reboot', 'process-restart']
    eco_gotests_kubeconfig_dir: /home/user/clusterconfigs
    eco_gotests_registry_auth_file: /home/user/pull-secret.json
  roles:
    - redhatci.ocp.eco_gotests
```

This example will run all PTP tests except those labeled with `node-reboot` and `process-restart`.

## Example with Generic Runner (LACP Bond Stability)

```yaml
---
- name: Run LACP bond stability tests via generic eco-gotests runner
  hosts: localhost
  gather_facts: false
  vars:
    eco_gotests_test_suites: ['generic']
    eco_gotests_generic_features: 'network'
    eco_gotests_generic_run_labels: ['lacp-bond-stability']
    eco_gotests_generic_env:
      ECO_LACP_BONDED_NODES: "worker-0,worker-1"
    eco_gotests_kubeconfig_dir: /home/user/clusterconfigs
    eco_gotests_registry_auth_file: /home/user/pull-secret.json
  roles:
    - redhatci.ocp.eco_gotests
```

This example uses the generic runner to launch only the `lacp-bond-stability` labeled tests from the `network` feature, passing the `ECO_LACP_BONDED_NODES` environment variable to the container.
