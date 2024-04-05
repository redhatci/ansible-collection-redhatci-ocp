Configure ZTP GitOps Repo
=========

This Role creates the tracking branch for ArgoCD. It makes it from an existing branch.

Requirements
------------

* Repository already exist

Role Variables
--------------

Variable | Required | Default | Description
---------|----------|---------|-------------
target_ztp_gitops_repo | yes | | 
target_ztp_gitops_repo_src_branch | no | main | Name of the branch containing the pre-created site config and policy manifests.
target_ztp_gitops_repo_dst_branch | yes | | Name of the branch configured in the hub cluster to pull the manifests from.
czgr_ssh_key_file | no | *null* | Local path to the repository's SSH private key file.
czgr_sites_path | no | SiteConfig | Repo path to the directory containing the site config manifests. Required when building the manifests from the template.
czgr_from_template | no | false | If set to "true", the role will attempt to build the repository from scratch based on the site_config template. If set to "false" the role assumes the src branch already contains a working set of manifests that must be copied to the target branch.