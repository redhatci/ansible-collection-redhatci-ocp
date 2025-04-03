# utils

This is a helper role that is meant to be consumed by acm related roles (acm_sno, acm_hypershift, etc).
Brings functionality that is commonly used among those roles.

## Variables

| Variable                     | Default   | Required by     | Description
| ---------------------------- | --------- | --------------- | -----------
| acm_utils_cluster_name       | None      | get-credentials | Name of the spoke cluster
| acm_utils_cluster_namespace  | None      | get-credentials | Namespace for the spoke cluster


## Utilities

### Get credentials

Gets kubeadmin password and kubeconfig from the hub cluster for the managed/spoke cluster and generates 3 variables with that information

- acm_kubeconfig_text
- acm_kubeconfig_user
- acm_kubeconfig_pass

## Usage example

See below some examples of how to use the redhatci.ocp.acm.utils role 

Get credentials from a deployed cluster through ACM

```yaml
- name: Get credentials from deployed cluster
  vars:
    acm_cluster_name: spoke-cluster
    acm_cluster_namespace: my-ns
  ansible.builtin.include_role:
    name: redhatci.ocp.acm.utils
    tasks_from: get-credentials
```
