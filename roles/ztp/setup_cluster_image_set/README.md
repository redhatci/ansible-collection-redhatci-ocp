# Setup Cluster Image Set

This role creates a Cluster Image Set with the OCP release to install in a ZTP spoke cluster and matches it to the Cluster Image Set Name Ref value specified in the Site Config manifest in the GitOps repository.

To achieve this, it receives the URL to the release image as in input variable and gets the name of the Cluster Image Set object from the Site Config manifest, after cloning the GitOps repository and reading the ClusterImageSetNameRef field in the manifest.

This means the value in the ClusterImageSetNameRef has no effect or control on the actual OCP version to be deployed. The version is determined by the provided URL. Therefore, the ClusterImageSetNameRef may take any value, and this role will make sure a valid Cluster Image Set of that name exists in the hub cluster.

It's worth mentioning that, for your spoke cluster deployment to work, the hub cluster must have network access to the provided release image URL.

## Variables

Variable               | Default | Required      | Description
-----------------------|---------|---------------|-------------
scis_repo_url          |         | yes           | URL to the repository with the GitOps manifests.
scis_sites_path        |         | yes           | Path in the repository to the directory containing the site config manifests.
scis_branch            | main    | no            | Branch to clone.
scis_key_path          |         | when SSH git  |
scis_username          |         | when HTTP git | Username to log into the repository.
scis_password          |         | when HTTP git | Password to log into the repository.
scis_release_image_url |         | yes           | URL to the OCP release image to use.

## Usage example

```yaml
- name: Setup Cluster Image Sets
  ansible.builtin.include_role:
    name: redhatci.ocp.ztp.cluster_image_set
  vars:
    scis_repo_url: https://github.com/ztp/gitops.git
    scis_site_configs_path: sites
    scis_username: gituser
    scis_password: gitpassword123!
    scis_release_image_url: "quay.io/openshift-release-dev/ocp-release@sha256:80078b22e5e6e215141bd8300c0e0392ada651334a6f3f4fc340f6a8076d1166"
```