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

czga_oc_tool_path | string | no | {{ oc_tool_path | default('/usr/local/bin/oc) }} | Path to the OpenShift Command Line Interface binary.