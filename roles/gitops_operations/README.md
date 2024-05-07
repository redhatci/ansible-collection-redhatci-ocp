gitops_operations
=================

This Ansible role contains varios tasks for GitOps operations.

Requirements
------------

* Access to an OpenShift cluster
* Properly configured kubeconfig file for cluster access

Role Variables
--------------

* `gops_kubeconfig_file`: (string) The file path of kubeconfig file for cluster. Default: undefined, If not provided, and no other connection options are provided, the Kubernetes client will attempt to load the default configuration file from ~/.kube/config. Can also be specified via `K8S_AUTH_KUBECONFIG` environment variable.
* `gops_app_name`: (string) The name of Application in GitOps.
* `gops_namespace`: (string) The namespace to use.

Example Playbook
----------------

* Sync repo for ArgoCD if autosync is disabled

```yaml
    - hosts: localhost
      tasks:

        - name: Force sync repo for "clusters" Applicaion in ArgoCD
          include_role:
            name: gitops_operations
          tasks_from: sync_repo
          vars:
            gops_kubeconfig_file: /path/to/kubeconfig
            gops_app_name: clusters
```
