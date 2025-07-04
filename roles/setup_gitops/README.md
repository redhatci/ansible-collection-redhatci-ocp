# GitOps setup

A role that enables support for the Kustomize plugin and the Policy Generator in ArgoCD.
This requires access to pull-secrets with permission to pull the following Red Hat images:

* registry.redhat.io/openshift4/ztp-site-generate-rhel8
* registry.redhat.io/rhacm2/multicluster-operators-subscription-rhel9

Also, openshift-gitops operator must be installed in the clusters via OLM.

## Variables

| Variable                            | Default                             | Description
| ----------------------------------- | ----------------------------------- | -----------
| sg_ztp_tag                          | v4.19.0                             | Tag for ZTP site generator image
| sg_mce_tag                          | v2.13                               | Tag for Multicluster Engine subscription image
| sg_local_registry                   | ""                                  | Local registry \<address\>[:\<port\>]  if the images need to be mirrored to a local registry
| sg_pullsecret_file                  | None                                | Registry pull/push secret file. Required if `sg_local_registry` is set
| sg_namespace                 | openshift-gitops                    | Namespace where ArgoCD is installed

## Usage example

```yaml
- name: Configure ArgoCD for Kustomize and Policy Generator
  vars:
    sg_ztp_tag: v4.19.0
    sg_mce_tag: v2.13
    sg_namespace: openshift-gitops
    sg_local_registry: local-registry.lab
    sg_pullsecret_file: .docker/auths.json
  ansible.builtin.include_role:
    name: redhatci.ocp.setup_gitops
```
