# generate_seed_image

Generates an IBI/IBU seed image for a ZTP-deployed SNO site. The role stops once
the `openshift/seed:<tag>` image is published to the hub registry; reattaching the
site to ACM or recreating the ClusterInstance for an IBI install is left to the
downstream deploy pipeline.

Ported from `eco.validation.tests.du.op.generate_seed_image_v1`.

## What it does

1. Ensures the OADP and Lifecycle Agent (LCA) operators are installed on the
   seed cluster (via `redhatci.ocp.olm_operator`).
2. Optionally configures a PVC-backed image registry on the hub and publishes
   its route.
3. Adds the hub registry to the seed cluster `insecureRegistries` (in-place MCO
   update, no reboot on OCP 4.14+).
4. Creates the `seedgen` secret in `openshift-lifecycle-agent`.
5. Detaches the site's `ManagedCluster` with `pruneManifests` (avoids the ArgoCD
   cascade that can crash OVN during klusterlet cleanup), then waits for the
   spoke klusterlet / OCM agent namespaces to disappear.
6. Applies the `SeedGenerator` CR and polls the spoke CR and hub imagestream
   until the `openshift/seed:<tag>` image is available.
7. Writes a timing report and finishes. The site is left detached
   (`pruneManifests` in place); any reattach/recreate is a downstream step.

## Requirements

- `oc` on the controller.
- `kubernetes.core` and `community.general` collections.
- Access to both the seed (spoke) and hub cluster kubeconfigs.

## Role Variables

| Name | Required | Default | Description |
| ---- | -------- | ------- | ----------- |
| `sno_sites_list` | yes | `{{ sites_list }}` | Sites to generate a seed image for. |
| `kubeconfig_path` | no | `$KUBECONFIG` / `~/.kube/config` | Seed cluster kubeconfig. |
| `kubeconfig_mgmt_cluster` | yes | - | Hub cluster kubeconfig. |
| `du_hostname` | no | derived from kubeconfig | Hostname used in artifact names. |
| `du_upgraded_ocp_version` | yes | - | Version used to build `seed_tag` (dashes removed). |
| `sno_du_ocp_version` | no | `{{ du_ocp_version }}` | Seed cluster OCP version (selects the OADP channel). |
| `ibu_configure_hub_cluster_storage` | no | `false` | Configure the hub image registry backend/route. |
| `oadp_namespace` / `oadp_catalog_source` / `oadp_channel` | no | `openshift-adp` / `redhat-operators` / `stable-1.4` (>=4.14) | OADP install settings. |
| `lca_namespace` / `lca_catalog_source` / `lca_channel` | no | `openshift-lifecycle-agent` / `redhat-operators` / `stable` | LCA install settings. |
| `seed_spoke_detach_retries` / `seed_spoke_detach_delay` | no | `40` / `15` | Spoke detach polling. |
| `seed_generation_poll_retries` / `seed_generation_poll_delay` | no | `120` / `15` | Seed generation polling (30 min by default). |
| `ztp_sites_gitops_repo` / `ztp_sites_gitops_repo_dst_branch` | yes | - | GitOps repository and branch for `pruneManifests`. |
| `ztp_sites_path` / `ztp_site_group` | yes | - | Site path and group inside the GitOps repo. |
| `gsi_collect_logs` | no | `true` | Run a must-gather on the seed cluster at the end. |

## Example

```yaml
- name: Generate seed image
  ansible.builtin.include_role:
    name: redhatci.ocp.generate_seed_image
  vars:
    sno_sites_list:
      - sno1
    kubeconfig_path: /home/slcm/.kube/spoke_kubeconfig
    kubeconfig_mgmt_cluster: /home/slcm/.kube/hub_kubeconfig
    du_upgraded_ocp_version: "4.16.0"
    ztp_sites_gitops_repo: ssh://git@git.example.lab:10022/dci/gitops.git
    ztp_sites_gitops_repo_dst_branch: main_rendered_site_sno1
    ztp_sites_path: gitops-sno/target
    ztp_site_group: "."
    ibu_configure_hub_cluster_storage: true
```
