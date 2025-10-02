# acm_setup role

This role performs the Advanced Cluster Management (ACM) post-installation tasks that include:

1. Validates that an storage class is present.
1. Installation of multicluster-engine and OADP operators
1. Creation of a multicluster engine
1. Disable the ClusterImageSet and channel subscriptions for disconnected environments.

The configuration of the ACM hub can be customized by using the following variables:

## Variables

| Variable                           | Default                       | Required    | Description
| ---------------------------------- | ----------------------------- | ----------- | ----------------------------------------------
|hub_availability                    |High                           |No           | Multicluster hub High Availability configuration
|hub_disable_selfmanagement          |False                          |No           | Do not import the hub cluster as managed in ACM
|hub_namespace                       |open-cluster-management        |No           | Namespace where ACM has been installed and will be configured
|hub_instance                        |multiclusterhub                |No           | Name of the multiclusterhub instance to be created (fail if already exists)
|hub_disconnected                    |false                          |No           | If true, it will create custom ClusterImageSets and remove the Channel subscriptions
|hub_sc                              |Undefined                      |If no default StorageClass is available | Desired storage class for ACM resources. If undefined, the default SC will be used
|hub_hugepages_type                  |hugepages-2Mi                  |No           | Hugepages type to be configured for Postgres search pods. x86_64 support hugepages-2Mi and hugepages-1Gi
|hub_hugepages_size                  |1024Mi                         |No           | Hugepages `hub_hugepages_type` size
|hub_db_volume_size                  |40Gi                           |No           | This value specifies how much storage it is allocated for storing files like database tables and database views for the clusters. You might need to use a higher value if there are many clusters
|hub_fs_volume_size                  |50Gi                           |No           | This value specifies how much storage is allocated for storing logs, manifests, and kubeconfig files for the clusters. You might need to use a higher value if there are many clusters
|hub_img_volume_size                 |40Gi                           |No           | This value specifies how much storage is allocated for the images of the clusters. You need to allow 1 GB of image storage for each instance of Red Hat Enterprise Linux CoreOS
|hub_img_svc_skip_tls_verify     |false                          |No           | Skip TLS verification in the AgentServiceConfig for image service operations. Useful in environments with self-signed certificates or certificate issues.
|hub_os_images                       |<Undefined>                    |No           | Locations of OS Images to be used when generating the discovery ISOs for different OpenShift versions. See [OS images](./README.md#os-images). It is mandatory for disconnected environments.

## Requirements
1. An OpenShift Cluster with a subscription for the ACM operator.
1. On air-gapped environments, the multicluster-engine operator must be available in the mirrored catalog

It is highly recommended to provision a storage class with enough space available for volumes of the Assisted Service Config before starting deploying clusters. See [acm_sno](../acm_sno/README.md) for more details.

In clusters configured with hugepages, the Postgres deployment requires hugepages to be configured too. Please allocate `hub_hugepages_type` and hub_hugepages_size according to the your cluster configuration.

## Usage example

See below an example of how to use the acm_setup role to configure ACM.

```yaml
- name: "Setup Advanced Cluster Management"
  ansible.builtin.include_role:
    name: redhatci.ocp.acm_setup
  vars:
      hub_disable_selfmanagement: true
      hub_availabilityConfig: High
      hub_disconnected: true
      hub_os_images:
        - openshiftVersion: "4.15.0-0.nightly-2024-04-21-051624"
          version: "4.15"
          url: "http://example.com/rhcos-415.92.202402201450-0-live.x86_64.iso"
          cpuArchitecture: x86_64

- name: "Setup Advanced Cluster Management with TLS verification disabled"
  ansible.builtin.include_role:
    name: redhatci.ocp.acm_setup
  vars:
      hub_disable_selfmanagement: true
      hub_availabilityConfig: High
      hub_disconnected: true
      hub_img_svc_skip_tls_verify: true
      hub_os_images:
        - openshiftVersion: "4.15.0-0.nightly-2024-04-21-051624"
          version: "4.15"
          url: "http://example.com/rhcos-415.92.202402201450-0-live.x86_64.iso"
          cpuArchitecture: x86_64
```

## OS images

See below some examples of how to define a list of OS maintained by the Agent service config.

```yaml
hub_os_images:
  - cpuArchitecture: x86_64
      openshiftVersion: "4.<minor-version>"
      rootFSUrl: https://<host>/<path>/rhcos-live-rootfs.x86_64.img
      url: https://<mirror-registry>/<path>/rhcos-live.x86_64.iso
  - cpuArchitecture: x86_64
      openshiftVersion: "4.<minor-version>"
      url: https://<mirror-registry>/<path>/rhcos-4.<minor-version>-live.x86_64.iso

hub_os_images:
  - cpuArchitecture: x86_64
      openshiftVersion: "4.<minor-version>"
      url: https://<mirror-registry>/<path>/rhcos-live.x86_64.iso
```

## References

* [acm_sno](../acm_sno/README.md): A role that deploys an SNO instance using ACM.
* [mirror_ocp_release](../mirror_ocp_release/): A role that mirrors an OCP release to a third-party or local registry.
* [dci-openshfit-agent](https://github.com/redhat-cip/dci-openshift-agent/): An agent that allows the deployment of OCP clusters, it is integrated with DCI (Red Hat Distributed CI).
* [dci-openshfit-app-agent](https://github.com/redhat-cip/dci-openshift-app-agent/): An agent that allows the deployment of workloads and certification testing on top OCP clusters, it is integrated with DCI (Red Hat Distributed CI).
