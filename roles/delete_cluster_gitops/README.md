delete_cluster_gitops
=====================

This Ansible role deletes installed cluster from GitOps.
Based on the following docs:

- [Removing a cluster by using the command line](https://access.redhat.com/documentation/en-us/red_hat_advanced_cluster_management_for_kubernetes/2.10/html/clusters/cluster_mce_overview#remove-a-cluster-by-using-the-cli)
- [Cannot delete managed cluster namespace manually](https://access.redhat.com/documentation/en-us/red_hat_advanced_cluster_management_for_kubernetes/2.10/html-single/clusters/index#no-delete-cluster-namespace-before-remove-cluster)
- [Process to destroy a cluster does not complete](https://access.redhat.com/documentation/en-us/red_hat_advanced_cluster_management_for_kubernetes/2.10/html-single/clusters/index#cluster-might-not-be-destroyed)

Requirements
------------

* Access to an OpenShift cluster
* Properly configured kubeconfig file for cluster access

Role Variables
--------------

* `dcg_kubeconfig_file`: (string) The file path of kubeconfig file for cluster. Default: undefined, If not provided, and no other connection options are provided, the Kubernetes client will attempt to load the default configuration file from ~/.kube/config. Can also be specified via `K8S_AUTH_KUBECONFIG` environment variable.
* `dcg_cluster_name`: (string) The name of installed cluster in ACM GitOps.
* `dcg_namespace`: (string) The namespace of installed cluster in ACM GitOps.
* `dcg_timeout`: (int) Timeout in seconds for namespace deletion. (Default: `90`)
* `dcg_finalizers_timeout`: (int) Timeout in seconds for finalizers deletion. (Default: `90`)

Example Playbook
----------------

* Delete cluster with namespace from GitOps

```yaml
    - hosts: localhost
      tasks:

        - name: Delete cluster cnfdd4-sno in namespace cnfdd4
          include_role:
            name: delete_cluster_gitops
          vars:
            dcg_kubeconfig_file:
            dcg_namespace: cnfdd4
            dcg_cluster_name: cnfdd4-sno
```
