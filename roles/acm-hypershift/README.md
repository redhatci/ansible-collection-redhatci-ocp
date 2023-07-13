# acm-hypershift role

This role allows the deployment of Hypershift (Hosted Control Planes) through ACM (Advanced Cluster Management).

## Requirements

To execute the acm-hypershift role a running OpenShift cluster and its credentials are required. i.e. through the KUBECONFIG environment variable.

- OpenShift Cluster with ACM operator. Please see [acm-setup](../acm-setup/README.md) role to deploy ACM through a role.
- A default storage class
- DNS configuration

### DNS configuration

The API Server for the hosted hypershift cluster is exposed as a NodePort service. A DNS entry must exist. Example: `api.hypershift.example.com` that points to the destination where the API Server can be reached.

These are the required DNS entries to allow interaction with the hosted hypershift cluster:

```Text
<ah_cluster_name>.<ah_base_domain>
api.<ah_cluster_name>.<ah_base_domain>
apps.<ah_cluster_name>.<ah_base_domain>
```

## Variables

| Variable                | Default                                   | Required  | Description                                                                    |
| ----------------------- | ----------------------------------------- | --------- | ------------------------------------------------------------------------------ |
| ah_base_domain          | example.com                               | No        | The base domain                                                                |
| ah_cluster_name         | hypershift                                | No        | Name of the hosted cluster                                                     |
| ah_cluster_network_cidr | 10.132.0.0/14                             | No        | Cluster network CIDR                                                           |
| ah_clusters_ns          | clusters                                  | No        | The prefix for the namespace                                                   |
| ah_cluster_type         | None                                      | No        | The type of cluster, currently only supported "None". No workers               |
| ah_force_deploy         | false                                     | No        | Force redeploy of a cluster                                                    |
| ah_no_log               | true                                      | No        | Allow logging on sensitive tasks                                               |
| ah_ocp_version          | 4.13.4                                    | No        | Full OCP version to install on the hypershift cluster. <major>.<minor>.<patch> |
| ah_pullsecret_file      | ""                                        | Yes*      | Required to pull and/or push images to public and/or disconnected repositories |
| ah_release_image        | quay.io/openshift-release-dev/ocp-release | No        | The release image to install, from the specified OCP version                   |

## Usage Example

See below for some examples of how to use the `acm-hypershift` role

```yaml
- name: Deploy hypershift cluster
  vars:
    ah_cluster_name: hypershift
    ah_ocp_version: 4.13.4
  include_role:
    name: acm-hypershift
```

## Role Outputs

The following facts can be consumed by other playbooks or roles. In the case of DCI integration, those files will be uploaded to the Job's files section.

```yaml
hypershift_kubeconfig_text: Kubeconfig file for the new cluster.
hypershift_kubeconfig_user: Username for the new cluster.
hypershift_kubeconfig_user: Password for the new cluster.
```
