Configure ZTP GitOps Apps
=========

This Role downloads the clusters and sites from a ZTP site generator image. It replaces several values to configure the tracking repositories.

Requirements
------------

* ArgoCD/GitOps already installed
* Repositories already exist

Role Variables
--------------

* ztp_sites_gitops_repo
* ztp_sites_branch
* ztp_sites_path

* ztp_policies_gitops_repo
* ztp_policies_branch
* ztp_policies_path

* ztp_site_generator_image
* ztp_site_generator_version

czga_podman_runner_host | string | no | podman-runner | Identity of the inventory host pulling the sites template generator image.
czga_clusters_namespace | string | no | clusters-sub | Namespace for the site config resources.
czga_kubeconfig_path | string | no | *omit* | Path to the ACM hub kubeconfig file.
czga_ocp_pull_secret | string | yes | | Pull secret for the Spoke cluster.
czga_policies_namespace | string | no | policies-sub | Namespace for the policy generator template resources. It can not be the sabe as the clusters namespace.
czga_oc_tool_path | string | no | {{ oc_tool_path | default('/usr/local/bin/oc) }} | Path to the OpenShift Command Line Interface binary.