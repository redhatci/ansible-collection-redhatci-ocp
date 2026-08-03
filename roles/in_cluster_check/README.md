# in_cluster_check Role

This role uses the [Pen Drive](https://catalog.redhat.com/en/software/containers/pen-drive/pen-drive-scanner-rhel9/68a605de092c681dd3e05d67) tool powered by Red Hat Lightspeed to run cluster system tests for disconnected clusters. It provides a solution for running Insights rules on-premises. The container image is based on the ubi9-minimal base image.

The role runs the Pen Drive scanner against an OpenShift cluster via `containers.podman.podman_container`, collects HTML and JSON reports from the job logs directory, and converts JSON results into JUnit XML.

Available Pen Drive flows: `gather`, `scan`, `full-run`, `in-cluster-check`, `kube-compare`.

## Variables

| Variable | Default | Required | Description |
| -------- | ------- | -------- | ----------- |
| icc_pullsecret_file | undefined | Yes | Registry auth file for podman |
| icc_kubeconfig_path | undefined | Yes | Host kubeconfig path mounted into the scanner container |
| icc_job_logs_path | undefined | Yes | Directory for Pen Drive output and generated JUnit XML files |
| icc_image | `registry.redhat.io/pen-drive/pen-drive-scanner-rhel9:1.0` | No | In-cluster check container image |
| icc_flow | `in-cluster-check` | No | Flow option passed to the container entrypoint |
| icc_keep_must_gather_data | `false` | No | Retain must-gather data after the run (only for `gather`, `scan`, and `full-run` flows) |
| icc_json2junit_patterns | `*.in_cluster_checks.json` | No | Glob patterns used to find JSON result files to convert into JUnit XML |
| icc_json2junit_output_dir | `{{ icc_job_logs_path }}` | No | Directory where generated JUnit XML files are written |
| icc_json2junit_suite_name | `In-cluster checks` | No | JUnit testsuite name written into the generated XML report |

## Requirements

- `podman` on the Ansible controller (jumphost)
- `containers.podman` Ansible collection

## Example

```yaml
---
- name: Run in-cluster check
  ansible.builtin.include_role:
    name: redhatci.ocp.in_cluster_check
  vars:
    icc_pullsecret_file: "{{ pullsecret_file }}"
    icc_kubeconfig_path: "{{ KUBECONFIG_PATH }}"
    icc_job_logs_path: "{{ job_logs.path }}"
```
