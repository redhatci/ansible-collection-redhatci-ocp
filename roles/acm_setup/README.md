# acm_setup role

This role performs the Advanced Cluster Management (ACM) post-installation tasks that include:

1. Validates that an storage class is present.
1. Installation of multicluster-engine and OADP operators
1. Creation of a multicluster engine
1. Disable the ClusterImageSet and channel subscriptions for disconnected environments.

The configuration of the ACM hub can be customized by using the following variables:

## Variables

| Variable                           | Default                       | Required    | Description                                   |
| ---------------------------------- | ----------------------------- | ----------- | ----------------------------------------------|
|hub_availability                    |High                           |No           |Multicluster hub High Availability configuration |
|hub_disable_selfmanagement          |False                          |No           |Do not import the hub cluster as managed in ACM  |
|hub_namespace                       |open-cluster-management        |No           |Namespace where ACM has been installed and will be configured |
|hub_instance                        |multiclusterhub                |No           |Name of the multiclusterhub instance to be created (fail if already exists) |
|hub_disconnected                    |false                          |No           |If true, it will create custom ClusterImageSets and remove the Channel subscriptions |
|hub_sc                              |Undefined                      |If no default StorageClass is available | Desired storage class for ACM resources. If undefined, the default SC will be used |
|hub_hugepages_type                  |hugepages-2Mi                  |No           |Hugepages type to be configured for Postgres search pods. x86_64 support hugepages-2Mi and hugepages-1Gi |
|hub_hugepages_size                  |1024Mi                         |No           |Hugepages `hub_hugepages_type` size              |

## Requirements
1. An Openshift Cluster with a subscription for the ACM operator.
1. On air-gapped environments, the multicluster-engine operator must be available in the mirrored catalog

It is highly recommended to provision a storage class with enough space available for volumes of the Assisted Service Config before starting deploying clusters. See [acm_sno](../acm_sno/README.md) for more details.

In clusters configured with hugepages, the Postgres deployment requires hugepages to be configured too. Please allocate `hugepages-2Mi` to cover the Postgres' search requirement and other workload needs.

## Usage example

See below an example of how to use the acm_setup role to configure ACM.

```yaml
- name: "Setup Advanced Cluster Management"
  include_role:
    name: acm_setup
  vars:
      hub_disable_selfmanagement: true
      hub_availabilityConfig: High
      hub_disconnected: true
```

## References

* [acm_sno](../acm_sno/README.md): A role that deploys an SNO instance using ACM.
* [mirror_ocp_release](../mirror_ocp_release/): A role that mirrors an OCP release to a third-party or local registry.
* [dci-openshfit-agent](https://github.com/redhat-cip/dci-openshift-agent/): An agent that allows the deployment of OCP clusters, it is integrated with DCI (Red Hat Distributed CI).
* [dci-openshfit-app-agent](https://github.com/redhat-cip/dci-openshift-app-agent/): An agent that allows the deployment of workloads and certification testing on top OCP clusters, it is integrated with DCI (Red Hat Distributed CI).
