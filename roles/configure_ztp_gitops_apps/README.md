Configure ZTP GitOps Apps
=========

This Role downloads the clusters and sites from a ZTP site generator image. It replaces several values to configure the tracking repositories.

Requirements
------------

* ArgoCD/GitOps already installed
* Repositories already exist

Role Variables
--------------

Name                        | Type   | Required | Default                                            | Description
--------------------------- | ------ | -------- | -------------------------------------------------- | -------------------------------------------------------------
czga_sites_gitops_repo      | string | yes      | -                                                  | Repository where SiteConfig can be found.
czga_sites_branch           | string | yes      | -                                                  | SiteConfig repo's branch.
czga_sites_path             | string | yes      | -                                                  | Path to find SiteConfig's kustomize file in the repo.
czga_policies_gitops_repo   | string | yes      | -                                                  | Repository where Policies can be found.
czga_policies_branch        | string | yes      | -                                                  | Policies repo's branch.
czga_policies_path          | string | yes      | -                                                  | Path to find Policies' kustomize file in the repo.
czga_site_generator_version | string | yes      | -                                                  | ZTP site generator container version
czga_multicluster_version   | string | yes      | -                                                  | Multicluster operators subscription container version
czga_site_generator_image   | string | no       | `registry.redhat.io/openshif4/ztp-site-generate-rhel8` | ZTP site generator container image
czga_multicluster_image     | string | no       | `registry.redhat.io/rhacm2/multicluster-operators-subscription-rhel9` | Multicluster operators subscription container image
czga_podman_runner_host     | string | no       | podman-runner                                      |  Identity of the inventory host pulling the sites template generator image.
czga_clusters_namespace     | string | no       | cluster-sub                                        | Namespace for the site config resources.
czga_kubeconfig_path        | string | no       | `{{ omit }}`                                       | Path to the ACM hub kubeconfig file.
czga_ocp_pull_secret        | string | yes      | -                                                  | Pull secret for the Spoke cluster.
czga_policies_namespace     | string | no       | policies-sub                                       | Namespace for the policy generator template resources. It can not be the sabe as the clusters namespace.
czga_oc_tool_path           | string | no       | `{{ oc_tool_path | default('/usr/local/bin/oc) }}` | Path to the OpenShift Command Line Interface binary.

License
-------

GNU GENERAL PUBLIC LICENSE version 3
