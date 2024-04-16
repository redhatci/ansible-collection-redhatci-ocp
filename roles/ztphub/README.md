ZTP GitOps ACM based role
=========

This Ansible role installs ACM based ZTP GitOps workflow from scratch

Requirements
------------

* Access to an OpenShift cluster
* ACM with MCE installed on Openshift cluster
* Properly configured kubeconfig file for cluster access
* Existing CatalogSource.
* Podman and Ansible installed

Role Variables
--------------

* `ztphub_working_dir`: (string) Local working directory path for files.
* `ztphub_gitops_operator_install_channel`: (string) GitOps (ArgoCD) operator channel version (default is `latest`)
* `ztphub_talm_operator_install_channel`: (string) TALM operator channel version (default is `stable`)
* `ztphub_image`: (string) Image for ZTP generator (default is `quay.io/openshift-kni/ztp-site-generator`)
* `ztphub_out_dir`: (string) Directory path for extracting files from ZTP image (default is `{{ ztphub_working_dir }}/out`)
* `ztphub_automatic_update`: (bool) Whether to update automatically operators (`installPlanApproval`) (default is `true`)
* `ztphub_install_ops_mode`: (string) `Manual` or `Automatic` depends on `ztphub_automatic_update`.

* `ztphub_install_gitops_operator_from_image`: (bool) Whether to install GitOps (ArgoCD) operator from image provided file (default is `false`)
* `ztphub_app_autosync`: (bool) Enable autosync in ArgoCD for repository (default is `false`)
* `ztphub_gitops_repo_insecure`: (bool) Disable TLS verify for repository settings in ArgoCD (default is `true`)
* `ztphub_gitops_repo_project`: (string) ArgoCD project for repository settings (default is `default`)
* `ztphub_gitops_repo`: (string) HTTP Git repository with GitOps files (siteconfigs)
* `ztphub_gitops_path`: (string) Git repository path to directory with `SiteConfig` configurations
* `ztphub_gitops_revision`: (string) Git repository version/branch for siteconfigs
* `ztphub_policy_gitops_repo`: (string) HTTP Git repository with GitOps Policy files
* `ztphub_policy_gitops_path`: (string) Git repository path to directory with `Policy` configurations
* `ztphub_policy_gitops_revision`: (string) Git repository version/branch for policies

* `ztphub_custom_images`: (list) Add another images (like nightlies) to the cluster.
* `ztphub_agent_service_config_spec`: (string) Configuration for AgentServiceConfig for Assisted Installer

Example Playbook
----------------

* Install ACM ZTP GitOps

```yaml
    - hosts: localhost
      tasks:
      - name: Install ACM ZTP GitOps
        include_role:
          name: ztphub
        vars:
          ztphub_working_dir: ~/tmp/ztphub
          ztphub_kubeconfig_file: my-kubeconfig-file
          ztphub_gitops_repo: https://gitlab.cee.redhat.com/telco-5g-devops-ci-infra/gitops.git
          ztphub_gitops_path: install
          ztphub_gitops_revision: master
          ztphub_policy_gitops_repo: https://gitlab.cee.redhat.com/telco-5g-devops-ci-infra/gitops.git
          ztphub_policy_gitops_path: configuration
          ztphub_policy_gitops_revision: master
          ztphub_custom_images:
            - name: openshift-v4.15.0
              image: quay.io/openshift-release-dev/ocp-release:4.15.0-x86_64
```
