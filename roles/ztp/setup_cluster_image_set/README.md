# Setup Cluster Image Set

This role clones the ZTP GitOps repository, reads the clusterImageSetRef fields in the site config manifests and creates the required clusterImageSet objects in the hub cluster for the spoke cluster deployment to work.

## Variables

Variable               | Default | Required | Description
-----------------------|---------|----------|-------------
scis_repo_url          |         | yes      | URL to the repository with the GitOps manifests.
scis_site_configs_path |         | yes      | Path in the repository to the directory containing the site config manifests.
scis_branch            | main    | no       | Branch to clone.
scis_username          |         | yes      | Username to log into the repository.
scis_password          |         | yes      | Password to log into the repository.

## Usage example

```yaml
- name: Setup Cluster Image Sets
  ansible.builtin.include_role:
    name: redhatci.ocp.ztp.cluster_image_set
  vars:
    scis_repo_url: https://github.com/ztp/gitops.git
    scis_site_configs_path: sites
    scis_username: gituser
    scis_username: gitpassword123!
```