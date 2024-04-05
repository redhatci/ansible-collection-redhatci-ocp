# Sideload-kernel utility role

This role will side-load a given realtime kernel onto an OpenShift SNO instance for
development and testing purposes.  It will replace the stock standard kernel, or
the stock realtime kernel if that has been enabled via MachineConfig or
NodeTuningOperator CRs.

Note: Only supported for side-loading custom realtime kernels, and only tested
on SNO installations.

## Variables

| Variable                    | Default     | Required | Description           |
| --------------------------- | ----------- | -------- | --------------------- |
| sideload_kernel_uri         | undefined   | Yes      | The full URI to the kernel-rt-core rpm package to be installed, or the special value `"reset"` to reset back to the original kernel. |
| sideload_kernel_namespace   | `"default"` | No       | The namespace where the job and pods run that conduct the change. Must be privileged. |
| sideload_kernel_force       | `false`     | No       | Forces re-creation of the kubernetes job even if no changes occurred. |
| sideload_kernel_job_timeout | `15`        | No       | The amount of time to wait for the sideload operation to complete (in minutes) |
| sideload_kernel_base_image  | `"ubi9"`    | No       | The image used to run the script on the cluster. |
| k8s_auth                    | `{}`        | No       | See the "Authentication" section below. |

## Requirements

- python3-kubernetes (or [kubernetes python library](https://pypi.org/project/kubernetes/))

## Authentication

The steps taken by this role require proper kubernetes authentication be set up
on the Ansible host (or localhost) for the cluster in question.  This may be
done in 3 ways:

- If the Ansible host has a valid kubeconfig in ~/.kube/config, this will be
  used by default.
- You can set the appropriate environment variables via the `k8s_auth` role
  variable. These will be named K8S_AUTH_* and are outlined in [kubernetes.core.k8s](https://galaxy.ansible.com/ui/repo/published/kubernetes/core/content/module/k8s/)

## Usage example

- Side-load a kernel, assuming ~/.kube/config is authenticated to
  the proper kubernetes cluster:

```yaml
- name: Sideload a kernel
  ansible.builtin.include_role:
    name: redhatci.ocp.sideload_kernel
  vars:
    sideload_kernel_uri: "https://example.com/packages/kernel/5.14.0/417.el9/x86_64/kernel-rt-core-5.14.0-417.el9.x86_64.rpm"
```

- Side-load a kernel, specifying the path to an alternative
  kubeconfig file:

```yaml
- name: Sideload a kernel
  ansible.builtin.include_role:
    name: redhatci.ocp.sideload_kernel
  vars:
    sideload_kernel_uri: "https://mymirror.local/kernels/kernel-rt-core-5.14.0-417.el9.x86_64.rpm"
    k8s_auth:
      K8S_AUTH_KUBECONFIG: /var/lib/clusterauth/kubeconfig
```

- Reset back to the original kernel

```yaml
- name: Reset to the custom standard kernel
  ansible.builtin.include_role:
    name: redhatci.ocp.sideload_kernel
  vars:
    sideload_kernel_uri: "reset"
    k8s_auth:
      K8S_AUTH_KUBECONFIG: /var/lib/clusterauth/kubeconfig
```
