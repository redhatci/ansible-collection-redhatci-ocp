# ACM Spoke Management operations

This role allows to perform multiple management operations on a given spoke cluster.

Tasks must be executed on the hub cluster that is controlling/going to control the given spoke cluster.

## Actions allowed

The following variable controls the action that can be performed within this role:

Name                         | Type   | Required | Default                                            | Description
---------------------------- | ------ | -------- | -------------------------------------------------- | ------------------------------------------------------------
asm_action                   | string | yes      | -                                                  | Action to be performed. Accepted values are `detach`, `attach`, and `delete-ztp-by-ref`.

## Detach a spoke cluster

This action allows to detach a spoke cluster from a given hub cluster.

This is based on the following [OCP documentation](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.5/html/clusters/managing-your-clusters#remove-a-cluster-by-using-the-cli).

### Requirements

* Spoke cluster running in a given hub cluster.

### Role Variables

Name                        | Type   | Required | Default                                            | Description
--------------------------- | ------ | -------- | -------------------------------------------------- | -------------------------------------------------------------
asm_cluster_name            | string | yes      | -                                                  | Cluster name, used for identifying the ManagedCluster and the Namespace

### Example

```yaml
- name: Detach spoke cluster from hub cluster
  ansible.builtin.include_role:
    name: redhatci.ocp.acm_spoke_mgmt
  vars:
    asm_action: "detach"
    asm_cluster_name: "mycluster"
```

## Attach a spoke cluster

This action allows to attach a spoke cluster to a given hub cluster.

This is based on the following [OCP documentation](https://docs.redhat.com/en/documentation/red_hat_advanced_cluster_management_for_kubernetes/2.5/html/clusters/managing-your-clusters#importing-a-target-managed-cluster-to-the-hub-cluster).

Three resources are created in this role:

- ManagedCluster resource (and related Namespace is automatically created after its creation).
- Autoimport Secret.
- KlusterletAddonConfig.

### Requirements

* Active spoke cluster already created, having access to its kubeconfig.

### Role Variables

Name                         | Type   | Required | Default                                            | Description
---------------------------- | ------ | -------- | -------------------------------------------------- | ------------------------------------------------------------
asm_cluster_kubeconfig_path  | string | yes      | -                                                  | Path to spoke cluster's kubeconfig file
asm_cluster_name             | string | yes      | -                                                  | Cluster name, used for identifying the ManagedCluster and the Namespace


### Example

```yaml
- name: Attach spoke cluster to hub cluster
  ansible.builtin.include_role:
    name: redhatci.ocp.acm_spoke_mgmt
  vars:
    asm_action: "attach"
    asm_cluster_kubeconfig_path: "/path/to/spoke/kubeconfig"
    asm_cluster_name: "mycluster"
```

## Remove ZTP ArgoCD resources

This action allows to remove the ArgoCD resources used to deploy a ZTP cluster. This could remove all the created resources in cascading. The role locates the ArgoCD applications used to create a cluster using the GitOps repository and source branch as references. It finally waits for the Managed Cluster to be destroyed, so a fresh deployment may be launched.

Two resources are deleted by this role.

- Application - Cluster
- Application - Policies

### Requirements

* A `KUBECONFIG` environment variable pointing to the management cluster's kubeconfig file.

### Role Variables

Name                         | Type   | Required | Default                                            | Description
---------------------------- | ------ | -------- | -------------------------------------------------- | ------------------------------------------------------------
asm_source_repo              | string | yes      | -                                                  | GitOps repository that was used to deploy the ZTP cluster
asm_target_revision          | string | yes      | -                                                  | Branch used to deploy the ZTP cluster
asm_delete_ztp_resources     | boolean| no       | true                                               | Deletes the ArgoCD applications and all the related cluster deployments resources
asm_cluster_name             | string | no       | If asm_delete_ztp_resources is set to true, name of the Managed Cluster the role must wait to be destroyed after removing the GitOps applications.

### Example

```yaml
- name: Remove a ZTP managed cluster from ArgoCD
  ansible.builtin.include_role:
    name: redhatci.ocp.acm_spoke_mgmt
  vars:
    asm_action: "delete-ztp-by-ref"
    asm_cluster_kubeconfig_path: "/path/to/spoke/kubeconfig"
    asm_cluster_name: clusterN
    asm_source_repo: "http://<gitops-repository>/gituser/gitops"
    asm_target_revision: main
```
