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
- A metalLB instance on baremetal environments. The [metallb_setup](./metallb_setup/README.md) role can help to configure a load balancer instance.
- DNS configuration
- jq

### DNS configuration

The API Server for the hosted hypershift cluster is exposed using the LoadBalancer service. All DNS entries required by the OpenShift must exist. Example: `api.hypershift.<hub-cluster-domain>`.

These are the required DNS entries to allow interaction with the hosted hypershift cluster:

```Text
<ah_cluster_name>.<ah_base_domain>
api.<ah_cluster_name>.<ah_base_domain>
apps.<ah_cluster_name>.<ah_base_domain>
```

At this time the role supports creating the OpenShift required endpoints under the Hub cluster subdomain. Example: https://console-openshift-console.apps.<hosted-cluster-name>.apps.<cluster-domain>

## Variables

| Variable                | Default                                   | Required  | Description
| ----------------------- | ----------------------------------------- | --------- | ------------
| ah_cluster_name         | Random string                             | No        | Name of the hosted cluster
| ah_base_domain          |                                           | No        | The base domain, DNS resolution for OCP endpoints must be prepared in advance. If undefined, the hosted cluster routes will be created as subdomains for \<hc\>.apps.\<hub-cluster-domain\>
| ah_node-pool-replicas   | 2                                         | No        | Number of pool replicas, minimum 2 is required
| ah_cluster_network_cidr | 10.132.0.0/14                             | No        | Cluster network CIDR
| ah_clusters_ns          | clusters                                  | No        | The prefix for the namespace
| ah_cluster_type         | kubevirt                                  | No        | The type infrastructure provider, currently supports "kubevirt" and "agent" (baremetal)
| ah_force_deploy         | false                                     | No        | Force redeploy of a cluster, if a HCP already exist with the same name it will be deleted
| ah_no_log               | true                                      | No        | Allow logging on sensitive tasks
| ah_pullsecret_file      | Pullsecret from management cluster        | No        | Pull secret file
| ah_release_image        | OCP release from Management cluster       | No        | The release image to install. In disconnected, it must be the image already mirrored.
| ah_node_memory          | 8Gi                                       | No        | Memory which is visible inside the Guest OS (type BinarySI, e.g. 5Gi, 100Mi)
| ah_download_cli         | True                                      | No        | Download some of the required binaries: oc, hcp.
| ah_hcp_cli_path         |                                           | No        | Path to the hcp CLI, if `ah_download_cli` the role will get the binary from the Management Cluster
| ah_ssh_key              | `sshKey` from Management cluster          | No        | SSH key to be added to the `authorized_keys` file in NodePool's instances
| ah_disconnected         | true                                      | No        | Defines if the hub is in an air-gapped environment

## Disconnected control planes

For disconnected environments it is required to already have the assets listed below available in a local registry instance. The [mirror_ocp_release](./mirror_ocp_release/README.md) role can help setup a disconnected registry with the needed assets.

* RHCOs images
* OCP release images

### Variables required for disconnected environments
| Variable                | Default                                                    | Required  | Description
| ----------------------- | ---------------------------------------------------------- | --------- | -----------
| ah_ca_bundle_file       | `addittionalTrustBundle` applied to the Management cluster | No        | Path to the CA trust bundle applied to the Management cluster in disconnected environments
| ah_hcp_annotations      | ""                                                         | No        | Annotations for the the HCP instance
| ah_ics                  | IDMS from Management cluster                               | No        | File with additional Image Content Source Type (ICSP/IDMS) to be passed to the Hosted Cluster

The role migrates the cluster's ICSP to IDMS, and those are passed to the Hosted Cluster if ah_ics is omit and the the deployment is set as disconnected.

Example of a file with Image Contents Sources definition.
```yaml
- mirrors:
  - myregistry:4443/ocp-4.14/4.14.20
  source: quay.io/openshift-release-dev/ocp-release
- mirrors:
  - myregistry:4443/ocp-4.14/4.14.20
  source: quay.io/openshift-release-dev/ocp-v4.0-art-dev
- mirrors:
  - myregistry:4443/rhacm2/memcached-rhel8
  source: registry.redhat.io/rhacm2/memcached-rhel8
- mirrors:
  - myregistry:4443/rhacm2/metrics-collector-rhel8
  source: registry.redhat.io/rhacm2/metrics-collector-rhel8
- mirrors:
  - myregistry:4443/container-native-virtualization/kubevirt-tekton-tasks-disk-virt-customize-rhel9
  source: registry.redhat.io/container-native-virtualization/kubevirt-tekton-tasks-disk-virt-customize-rhel9
- mirrors:
  - myregistry:4443/rhacm2/acm-prometheus-rhel8
  source: registry.redhat.io/rhacm2/acm-prometheus-rhel8
- mirrors:
  - myregistry:4443/openshift-logging/fluentd-rhel9
  source: registry.redhat.io/openshift-logging/fluentd-rhel9
<snip>
```

### Disconnected using the Agent (baremetal) provisioner

Baremetal deployments in disconnected requires the local availability of multiple artifacts like:

1. A web server with the RHCOS images for the version to install
1. A local copy of all the images of the target OCP release
1. A local copy of all the operator images to be installed on the Hosted Cluster

This role relies [DCI Openshift Agent](https://github.com/redhat-cip/dci-openshift-agent/tree/master/) to prepare the environment. Using the individual roles from the [redhatci.ocp](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/) is valid.

### Disconnected using the Kubevirt provisioner

Kubevirt provisioner in disconnected environments requires:

1. Setting an annotation with the Control Plan Operator Image from the target OCP release
1. Extract the RHCOS images required for the Kubevirt VMs
1. Mirror the RHCOS images to the local registry. The role mirrors the image into the same registry path as the release image.

This role takes cares of the tasks listed above.

Important:
1. In disconnected environments is required to set `ah_release_image` pointing to the release image already mirrored in a local registry.
1. At this time the release image for the hosted cluster must be the same used to deploy the Managed cluster. It is supported only to deploy HCP of the same version as the Management Cluster.

## Usage Example

See below for some examples of how to use the `acm_hypershift` role

```yaml
- name: Deploy a hosted cluster cluster
  vars:
    ah_cluster_name: myhc
    ah_release_image: quay.io/openshift-release-dev/ocp-release:4.14.17-x86_64
    ah_cluster_type: agent
  ansible.builtin.include_role:
    name: redhatci.ocp.acm_hypershift
```

```yaml
- name: Deploy a hosted cluster in disconnected with custom ICS
  vars:
    ah_download_cli: false
    ah_release_image: myregistry:4443/ocp-4.14/4.14.20@sha256:e64464879cd1acdfa7112c1ac1d90039e1689189e0af197f34881c79decda933
    ah_disconnected: true
    ah_ssh_key: /home/beto/.ssh/id_rsa.pub
    ah_ics: /home/beto/icsp.yml
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
