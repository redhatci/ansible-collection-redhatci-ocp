# ocp_remove_nodes

Remove (worker) nodes from an OCP cluster.

# Requirements

- Python [jmespath](https://pypi.org/project/jmespath) library
- Access to a valid kubeconfig file via an `KUBECONFIG` environment variable.
  

# Variables

| Variable  | Required | Description
| --------- | -------- | -----------
| orn_nodes | Yes      | A list of worker nodes to remove from a cluster.


> [!IMPORTANT]
> The name of the node must be exactly as listed in the cluster

## Usage example

- Removing a single node from an OCP cluster

```yaml
- name: Remove a single node from the cluster
  ansible.builtin.include_role:
    name: redhatci.ocp.ocp_remove_nodes
  vars:
    orn_nodes:
      - worker-8
```

- Removing a multiple nodes from an OCP cluster

```yaml
- name: Remove a single node from the cluster
  ansible.builtin.include_role:
    name: redhatci.ocp.ocp_remove_nodes
  vars:
    orn_nodes:
      - my-worker-2
      - my-worker-3
      - my-worker-4
      - my-worker-5
      - my-worker-6
```
