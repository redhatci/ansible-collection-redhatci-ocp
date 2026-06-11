# in_cluster_check Role

This Role uses Pen Drive tool powered by Red Hat Lightspeed that delivers cluster system tests for disconnected clusters. It aims to provide a solution for running Insights rules on-premises. The container image is based on the ubi9-minimal base image

It Runs the [Pen Drive](https://catalog.redhat.com/en/software/containers/pen-drive/pen-drive-scanner-rhel9/68a605de092c681dd3e05d67) tool for in-cluster-check container against an OpenShift cluster, collects HTML test reports from the job logs directory.

The available options for this tool are , [gather|scan|full-run|in-cluster-check|kube-compare]
## Variables

| Variable | Default | Required | Description |
| -------- | ------- | -------- | ----------- |
| icc_pullsecret_file | undefined | Yes | Registry auth file |
| icc_kubeconfig_path | undefined | Yes | path to kubeconfig mounted into the container |
| icc_image | `registry.redhat.io/pen-drive/pen-drive-scanner-rhel9:1.0` | Yes | In-cluster check container image |
| icc_flow | `full-run` | No | flow option passed to the container entrypoint |
| icc_keep_must_gather_data | `false` | Yes | Retain must-gather data after the run |
| icc_tls_verify | false | Yes | Verify tls flag |

## Requirements

- `podman` on the Ansible controller (jumphost)

## Example

DCI success hook:

```yaml
---
- name: Run in-cluster check
  ansible.builtin.include_role:
    name: redhatci.ocp.in_cluster_check
  vars:
    icc_pullsecret_file: "{{ pullsecret_file }}"
    icc_kubeconfig_path: "{{ KUBECONFIG_PATH }}"
  
```
