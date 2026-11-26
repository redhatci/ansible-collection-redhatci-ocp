# image_based_upgrade

Performs an Image-Based Upgrade (IBU) of a ZTP-deployed single-node OpenShift
cluster managed by ACM and TALM, and writes a phase-level timing report.

The SNO is reached with `ibu_sno_kubeconfig`, the ACM hub with
`ibu_hub_kubeconfig`.

## What it does

1. Records the starting OCP version from the SNO `ClusterVersion`.
2. Installs OADP and the Lifecycle Agent with `redhatci.ocp.olm_operator` when
   `ibu_install_operators` is true, then checks both CSVs succeeded.
3. Ensures OADP has a `DataProtectionApplication` (the IBU `oadpContent`
   Backup/Restore targets a `default` BackupStorageLocation). An existing one is
   left untouched; when none exists and `ibu_configure_oadp` is true, the role
   creates one from `ibu_backup_s3_url`, `ibu_backup_bucket` and either an
   existing credentials Secret or `ibu_backup_access_key` /
   `ibu_backup_secret_key`.
4. Resolves the seed image registry — the hub internal registry default route
   when `ibu_seed_registry` is empty, otherwise the external registry — adds it
   to the SNO `insecureRegistries` (waiting for the MachineConfigPool update when
   `ibu_wait_mcp` is true), and creates the LCA image pull Secret from a hub
   `registry-user` token or from `ibu_seed_registry_authfile`.
5. Sets the site labels in the ZTP GitOps repository: the configuration version
   is moved to `ibu_target_version` and `ibu` is set to `true`.
6. Runs the Preparation, Upgrade and optional Rollback `ClusterGroupUpgrade`s,
   waiting for the matching policies to report `Compliant`.
7. After the Upgrade, writes an IBU timing report to `ibu_output_dir` when it is
   set (TALM overhead, PrePivot, reboot, PostPivot, policy reconciliation and
   totals), and saves the raw CGU/IBU/LCA/MCO artifacts.
8. Resets the site `ibu` label to `false` on exit when the role manages labels.

## Requirements

- `oc` on the controller.
- The `kubernetes.core` collection.
- ACM, TALM and the ZTP GitOps repository already configured for the site.
- Push access to the GitOps repository when `ibu_gitops_update_labels` is true.
- Hub registry: a `registry-user` service account in the `openshift`
  namespace (as created by `redhatci.ocp.generate_seed_image`).
- External registry: `ibu_seed_registry` plus `ibu_seed_registry_authfile`
  (or the usual pull secret variables).

## Role Variables

Name                              | Required | Default               | Description
--------------------------------- | -------- | --------------------- | -----------
ibu_hub_kubeconfig                | Yes      |                       | Kubeconfig of the ACM hub cluster.
ibu_sno_kubeconfig                | Yes      |                       | Kubeconfig of the single-node cluster to upgrade.
ibu_site                          | Yes      |                       | SNO site name (ManagedCluster and policy namespace).
ibu_target_version                | Yes      |                       | Target configuration version, used in labels and policy names.
ibu_oc_path                       | No       | `/usr/local/bin/oc`   | Path to the `oc` binary.
ibu_install_operators             | No       | `false`               | Install OADP and LCA. When false, only check they are installed.
ibu_operators_source              | No       | `redhat-operators`    | CatalogSource used to install the operators.
ibu_operators_source_ns           | No       | `openshift-marketplace` | Namespace of `ibu_operators_source`.
ibu_oadp_namespace                | No       | `openshift-adp`       | OADP namespace.
ibu_oadp_channel                  | No       | `""` (operator default) | OADP channel. Empty uses the operator's default.
ibu_lca_namespace                 | No       | `openshift-lifecycle-agent` | LCA namespace.
ibu_lca_channel                   | No       | `stable`              | LCA channel.
ibu_configure_oadp                | No       | `false`               | Create a DPA when none exists. Existing DPAs are never overwritten.
ibu_oadp_name                     | No       | `ibu`                 | Name of the DataProtectionApplication created by the role.
ibu_backup_s3_url                 | No       | `""`                  | S3 endpoint for the created DPA.
ibu_backup_s3_region              | No       | `minio`               | S3 region for the created DPA.
ibu_backup_s3_insecure            | No       | `false`               | Skip TLS verification for the S3 endpoint.
ibu_backup_bucket                 | No       | `""`                  | Bucket used for IBU backups.
ibu_backup_bucket_prefix          | No       | `backups`             | Backups prefix inside the bucket.
ibu_backup_credentials_secret     | No       | `cloud-credentials`   | Secret with the S3 credentials under the `cloud` key.
ibu_backup_access_key             | No       | `""`                  | S3 access key; with the secret key, creates the credentials Secret.
ibu_backup_secret_key             | No       | `""`                  | S3 secret key; with the access key, creates the credentials Secret.
ibu_seed_registry                 | No       | `""` (hub registry)   | External seed image registry `host[:port]`. Empty uses the hub registry.
ibu_seed_registry_authfile        | No       | `""` / pull secret    | Authfile with the external registry credentials.
ibu_seed_registry_insecure        | No       | `false`               | Add the external registry to SNO `insecureRegistries`.
ibu_configure_insecure_registry   | No       | `true`                | Add the seed image registry to SNO `insecureRegistries`.
ibu_wait_mcp                      | No       | `true`                | Wait for the MachineConfigPool update.
ibu_mcp_retries / _delay          | No       | `40` / `15`           | MachineConfigPool wait.
ibu_configure_lca_secret          | No       | `true`                | Create the LCA image pull Secret.
ibu_registry_user                 | No       | `registry-user`       | Hub service account used to pull the seed image.
ibu_registry_user_namespace       | No       | `openshift`           | Namespace of `ibu_registry_user`.
ibu_lca_pull_secret_name          | No       | `ibu-pull-secret`     | Name of the pull Secret in the LCA namespace.
ibu_gitops_update_labels          | No       | `true`                | Update site labels in the GitOps repository.
ibu_gitops_repo                   | No       | `""`                  | GitOps repository holding the site manifest.
ibu_gitops_branch                 | No       | `""`                  | Branch of `ibu_gitops_repo`.
ibu_gitops_site_file              | No       | `""`                  | Site manifest path, relative to the repository root.
ibu_configuration_version_label   | No       | `configuration-version` | Site label holding the configuration version.
ibu_ibu_label                     | No       | `ibu`                 | Site label that enables the IBU policies.
ibu_site_policy_namespace         | No       | `{{ ibu_site }}`      | Namespace of the policies on the hub.
ibu_oadp_policy                   | No       | `ibu-oadp-oadp-cm-policy` | OADP ConfigMap policy in the Preparation CGU.
ibu_policy_prefix                 | No       | `group-ibu-cv{{ ibu_target_version }}` | Prefix of the per-version IBU policies.
ibu_prep_policy                   | No       | `prep-policy`         | Preparation policy name fragment.
ibu_upgrade_policy                | No       | `upgrade-policy`      | Upgrade policy name fragment.
ibu_rollback_policy               | No       | `rollback-policy`     | Rollback policy name fragment.
ibu_prep_cgu_namespace            | No       | `ztp-install`         | Namespace of the Preparation CGU.
ibu_upgrade_cgu_namespace         | No       | `default`             | Namespace of the Upgrade CGU.
ibu_rollback_cgu_namespace        | No       | `default`             | Namespace of the Rollback CGU.
ibu_policy_retries / _delay       | No       | `120` / `30`          | Policy wait (default 60 minutes).
ibu_run_rollback                  | No       | `true`                | Run the Rollback stage after a successful Upgrade.
ibu_collect_timing                | No       | `true`                | Write the IBU timing report after the Upgrade.
ibu_output_dir                    | No       | `""`                  | Directory for the timing report and raw artifacts. Empty skips them.

## Facts set

Name                        | Description
--------------------------- | -----------
ibu_ocp_version_pre_upgrade | Starting OCP version captured before the upgrade.
ibu_hub_registry            | Host of the hub image registry route (hub registry only).
ibu_seed_image_registry     | Registry the seed image is pulled from.
ibu_ocp_version_current     | OCP version reported after the upgrade.
ibu_ocp_version_target      | Seed image version from the IBU CR.

## Example

```yaml
- name: Perform the Image-Based Upgrade
  ansible.builtin.include_role:
    name: redhatci.ocp.image_based_upgrade
  vars:
    ibu_hub_kubeconfig: /home/dci/clusterconfigs-hub/kubeconfig
    ibu_sno_kubeconfig: /home/dci/clusterconfigs-sno1/kubeconfig
    ibu_site: sno1
    ibu_target_version: "4.18.3-1"
    ibu_gitops_repo: ssh://git@git.example.lab:10022/dci/gitops.git
    ibu_gitops_branch: main_rendered_site_sno1
    ibu_gitops_site_file: gitops-sno/target/sno1/sno1.yaml
    ibu_install_operators: true
    ibu_configure_oadp: true
    ibu_backup_s3_url: https://s3.example.lab
    ibu_backup_bucket: ibu
    ibu_backup_access_key: "{{ lookup('env', 'IBU_S3_ACCESS_KEY') }}"
    ibu_backup_secret_key: "{{ lookup('env', 'IBU_S3_SECRET_KEY') }}"
    ibu_output_dir: "{{ job_logs.path }}"
```
