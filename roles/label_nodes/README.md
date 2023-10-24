# label_nodes role

This role applies labels defined at inventory level to the OCP cluster nodes.

> NOTE:
- This role has been tested only in IPI, UPI and SNO installers
- Other installers that require a hosts file should work

## Variables

| Variable               | Default        | Type         | Required    | Description                                                              |
| ---------------------- | ---------------|------------- | ----------- | -------------------------------------------------------------------------|
| hosts_list             | []             | List         | No          | A list of host that need its labels applied to OCP nodes                 |

## Role requirements for BGP mode
  - An Openshift cluster.
  - Access to the kubeconfig file via the `KUBECONFIG` environment variable
  - The inventory host should have the labels needed in JSON format

```toml
[workers:vars]
labels={"Location": "Boston", "owner": "OCP operators", "cost_center", "IT"} 

[ocs_nodes:vars]
labels={"cluster.ocs.openshift.io/openshift-storage": ""}    

## Usage example

Get all the inventory hosts and apply the defined labels

```yaml
- name: "Merge all hosts"
  set_fact:
    all_hosts: "{{ all_hosts | default([]) + groups[item] }}"
  loop: "{{ groups.keys() }}"

- name: "Apply node labels"
  include_role: 
    name: redhatci.ocp.label_nodes
  vars:
    hosts_list: "{{ all_hosts | list | unique }}"
```
