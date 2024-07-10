# Remove ZTP GitOps resources

Remove all GitOps related resources for a given spoke cluster, excepting the cluster namespace, which is not deleted because this will imply the spoke cluster is detached from the hub cluster.

For performing a cluster detachment, then use the [acm_detach_spoke_cluster](../acm_detach_spoke_cluster) role accordingly.

## Requirements

* Hub cluster configured for launching ZTP.
* ArgoCD configured in the hub cluster.
* Spoke cluster deploying thanks to ArgoCD applications already configured.

## Role Variables

Default values for role variables are based on default values used in [gitops_configure_repo](../gitops_configure_repo) and [configure_ztp_gitops_apps](../configure_ztp_gitops_apps) roles. Being more precise for the second case, it's using the default resource names applied by the ZTP Site Generator container.

Please adapt the values of these variables for your use case.

Name                        | Type   | Required | Default                                            | Description
--------------------------- | ------ | -------- | -------------------------------------------------- | -------------------------------------------------------------
rzgr_gitops_applications    | list   | no       | ["clusters", "policies"]                           | GitOps Applications related to SiteConfig and Policy resources.
rzgr_gitops_appprojects     | list   | no       | ["ztp-app-project", "policy-app-project"]          | GitOps AppProjects related to SiteConfig and Policy resources.
rzgr_policies_namespace     | string | no       | policies-sub                                       | Namespace for the policy generator template resources. It can not be the sabe as the clusters namespace.
rzgr_extra_namespaces       | list   | no       | ["ztp-common", "ztp-group", "ztp-site"]            | Extra namespaces that are created for GitOps policy creation by default.
rzgr_cluster_role_bindings  | list   | no       | ["gitops-policy", "gitops-cluster"]                | ClusterRoleBindings created for the deployment of GitOps Policy and SiteConfig.
rzgr_private_repo_secret    | string | no       | private-repo                                       | Secret that will hold the private repo credentials.
rzgr_argo_cd_known_host_cm  | string | no       | argocd-ssh-known-hosts-cm                          | ConfigMap that will save the ArgoCD SSH known hosts.

## Example

Following example is the most basic call to this role, using the default arguments for each role variable:

```
- name: Remove ZTP GitOps resources
  ansible.builtin.include_role:
    name: redhatci.ocp.remove_ztp_gitops_resources
```

If you want to override any default value of any role variable, then you need to provide it with `vars`, for example:

```
- name: Remove ZTP GitOps resources
  ansible.builtin.include_role:
    name: redhatci.ocp.remove_ztp_gitops_resources
  vars:
    rzgr_policies_namespace: "mycluster-policies"
```
