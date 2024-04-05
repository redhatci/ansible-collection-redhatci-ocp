# acm_hypershift role

This role allows the deployment of Hypershift (Hosted Control Planes) through ACM (Advanced Cluster Management).

## Requirements

To execute the acm_hypershift role a running OpenShift cluster and its credentials are required. i.e. through the KUBECONFIG environment variable.

- OpenShift Cluster with ACM operator. Please see [acm_setup](../acm_setup/README.md) role to deploy ACM through a role. The hub must have the following operators already installed:
  - Advanced Cluster Manager
  - Multicluster Engine
  - Metal LB operator is required when using kvirt provider in Bare Metal environments
  - Hyperconverged Operator for kubevirt provider
- A default storage class capabilities for DataVolumes provisioning
- A metalLB instance on baremetal environments
- DNS configuration

### DNS configuration

The API Server for the hosted hypershift cluster is exposed using the LoadBalancer service. All DNS entries required by the OpenShift must exist. Example: `api.hypershift.<hub-cluster-domain>`.

These are the required DNS entries to allow interaction with the hosted hypershift cluster:

```Text
<ah_cluster_name>.<ah_base_domain>
api.<ah_cluster_name>.<ah_base_domain>
apps.<ah_cluster_name>.<ah_base_domain>
```

At this time the role supports creating the OpenShift required endpoints under the Hub cluster subdomain. example: https://console-openshift-console.apps.<hosted-cluster-name>.apps.<cluster-domain>

## Variables

| Variable                | Default                                   | Required  | Description                                                                             |
| ----------------------- | ----------------------------------------- | --------- | --------------------------------------------------------------------------------------  |
| ah_cluster_name         | Random string                             | No        | Name of the hosted cluster                                                              |
| ah_base_domain          |                                           | No        | The base domain, DNS resolution for OCP endpoints must be prepared in advance. If undefined, the hosted cluster routes will be created as subdomains for \<hc\>.apps.\<hub-cluster-domain\>|
| ah_node-pool-replicas   | 2                                         | No        | Number of pool replicas, minimum 2 is required                                          |
| ah_cluster_network_cidr | 10.132.0.0/14                             | No        | Cluster network CIDR                                                                    |
| ah_clusters_ns          | clusters                                  | No        | The prefix for the namespace                                                            |
| ah_cluster_type         | kubevirt                                  | No        | The type infrastructure provider, currently only only supports "kubevirt"               |
| ah_force_deploy         | false                                     | No        | Force redeploy of a cluster                                                             |
| ah_no_log               | true                                      | No        | Allow logging on sensitive tasks                                                        |
| ah_ocp_version          | 4.14.0                                    | No        | Full OCP version to install on the hypershift cluster. <major>.<minor>.<patch>          |
| ah_pullsecret_file      | ""                                        | Yes       | Required to pull the hosted cluster release image                                       |
| ah_release_image        | quay.io/openshift-release-dev/ocp-release | No        | The release image to install, from the specified OCP version                            |
| ah_node_memory          | 8Gi                                       | No        | Memory which is visible inside the Guest OS (type BinarySI, e.g. 5Gi, 100Mi)            |

## Usage Example

See below for some examples of how to use the `acm_hypershift` role

```yaml
- name: Deploy hypershift cluster
  vars:
    ah_cluster_name: hypershift
    ah_ocp_version: 4.14.0
    ah_pullsecret_file: /<path_to_ps>
  ansible.builtin.include_role:
    name: redhatci.ocp.acm_hypershift
```

## Role Outputs

The following facts can be consumed by other playbooks or roles. In the case of DCI integration, those files will be uploaded to the Job's files section.

```yaml
hypershift_kubeconfig_text: Kubeconfig file for the new cluster.
hypershift_kubeconfig_user: Username for the new cluster.
hypershift_kubeconfig_user: Password for the new cluster.
```
