# generate_seed_image

Generates a Lifecycle Agent (LCA) seed image from a ZTP-deployed single-node
OpenShift cluster, for image-based install (IBI) or image-based upgrade (IBU).
The image is pushed to the hub image registry as
`openshift/seed_<gsi_site>:<gsi_seed_tag>`.

The seed cluster is the one selected by the `KUBECONFIG` environment variable.
The ACM hub is reached with `gsi_hub_kubeconfig`.

## What it does

1. Backs the hub image registry with a PVC, exposes its default route, and
   creates a `registry-user` service account allowed to push to the `openshift`
   namespace.
2. Installs OADP and the Lifecycle Agent on the seed cluster when
   `gsi_install_operators` is true, then checks that both CSVs succeeded.
3. Adds the hub registry to the seed cluster `insecureRegistries` and waits for
   the in-place MachineConfigPool update (no reboot on OCP 4.14+).
4. Creates the `seedgen` Secret with the hub registry push credentials.
5. Detaches the seed cluster: adds `pruneManifests` for the `ManagedCluster` to
   its ClusterInstance in the GitOps repository, waits for the hub
   `ManagedCluster` and the seed cluster klusterlet agent to be removed, and
   deletes leftover ACM `hub-alertmanager-router-ca` Secrets (they make recert
   fail). The ClusterInstance and BareMetalHost are kept, and the cluster is
   left detached.
6. Creates the `SeedGenerator`, waits for the image on the hub imagestream
   (the seed cluster API is down during the build), then waits for the seed
   cluster to report `SeedGenCompleted`.
7. Writes a timing report to `gsi_output_dir` when it is set.

## Requirements

- `oc` on the controller.
- The `kubernetes.core` collection.
- Push access to the GitOps repository.

## Role Variables

Name                              | Required | Default                     | Description
--------------------------------- | -------- | --------------------------- | -----------
gsi_hub_kubeconfig                | Yes      |                             | Kubeconfig of the ACM hub cluster.
gsi_seed_tag                      | Yes      |                             | Seed image tag, pushed as `openshift/seed_<gsi_site>:<tag>`.
gsi_site                          | Yes      |                             | Seed cluster name (ManagedCluster and ClusterInstance name).
gsi_gitops_repo                   | Yes      |                             | GitOps repository holding the seed cluster ClusterInstance.
gsi_gitops_branch                 | Yes      |                             | Branch of `gsi_gitops_repo` to update.
gsi_gitops_clusterinstance_file   | Yes      |                             | ClusterInstance file path, relative to the repository root.
gsi_output_dir                    | No       | `""`                        | Directory for the timing report. Empty skips it.
gsi_oc_path                       | No       | `/usr/local/bin/oc`         | Path to the `oc` binary.
gsi_install_operators             | No       | `false`                     | Install OADP and LCA. When false, only check they are installed.
gsi_operators_source              | No       | `redhat-operators`          | CatalogSource used to install the operators.
gsi_operators_source_ns           | No       | `openshift-marketplace`     | Namespace of `gsi_operators_source`.
gsi_oadp_namespace                | No       | `openshift-adp`             | OADP namespace.
gsi_oadp_channel                  | No       | `""` (operator default)     | OADP channel. Empty uses the operator's default.
gsi_lca_namespace                 | No       | `openshift-lifecycle-agent` | LCA namespace, also holds the `seedgen` Secret.
gsi_lca_channel                   | No       | `stable`                    | LCA channel.
gsi_registry_storage_class        | No       | `ocs-storagecluster-cephfs` | StorageClass of the hub registry PVC, when it is created.
gsi_registry_storage_size         | No       | `100Gi`                     | Size of the hub registry PVC, when it is created.
gsi_detach_retries / _delay       | No       | `40` / `15`                 | Wait for the hub and seed cluster detach.
gsi_mcp_retries / _delay          | No       | `40` / `15`                 | Wait for the seed cluster MachineConfigPool update.
gsi_seed_retries / _delay         | No       | `120` / `15`                | Wait for the seed image, then for the seed cluster restore.

## Facts set

Name                        | Description
--------------------------- | -----------
gsi_seed_imagestream        | Hub imagestream holding the seed image (`seed_<gsi_site>`, in `openshift`).
gsi_seed_image              | Full seed image reference on the hub registry.
gsi_seed_started_at         | Seed generation start time (UTC).
gsi_seed_created_at         | Time the image was pushed to the hub (UTC).
gsi_seed_duration           | Seconds between start and push.
gsi_seed_cluster_restored   | Whether the seed cluster reported `SeedGenCompleted` in time.

## Example

```yaml
- name: Generate the seed image
  ansible.builtin.include_role:
    name: redhatci.ocp.generate_seed_image
  vars:
    gsi_hub_kubeconfig: /home/dci/clusterconfigs-hub/kubeconfig
    gsi_seed_tag: "4.18.59"
    gsi_site: sno1
    gsi_gitops_repo: ssh://git@git.example.lab:10022/dci/gitops.git
    gsi_gitops_branch: main_rendered_site_sno1
    gsi_gitops_clusterinstance_file: gitops-sno/target/sno1/sno1.yaml
    gsi_output_dir: "{{ job_logs.path }}"
```
