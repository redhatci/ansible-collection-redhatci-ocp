# acm-sno role

This role allows the deployment of SNO (Single Node Openshift) instances using ACM (Advanced Cluster Management). In order to execute the acm-sno role a running OpenShift cluster and its credentials are required. i.e. through the KUBECONFIG environment variable.

Please see [acm-setup](../acm-setup/README.md) role in case configuring the ACM hub is required.

```shell
export KUBECONFIG=<path_kubeconfig>
```

Main tasks:
- Provisioning the target host using a defined BMC
- Configure the ACM's CIM (Cluster Infrastructure Management) database
- Setup the instance parameters
- Request the cluster deployment
- The role will disable the ClusterImageSet subscription (if disconnected)

The role will pull some data from the Hub cluster (the one running ACM) and apply them to the spoke cluster. Some of the inherited details are:
- The cluster pull_secret
- The SSH public key assigned to the OS user called "core"
- The CA certificate (It is common in in air-gapped environments or with a local registry service)

This role does not perform the mirroring of RHCOS, release images, and operators. Please see [references](#references) for roles that may help with those tasks.

This role only been tested in x86_64 architectures.

## Variables

| Variable                               | Default                       | Required    | Description                                   |
| -------------------------------------- | ----------------------------- | ----------- | ----------------------------------------------|
| acm_cluster_name                       | sno                           | No          | Name of the spoke cluster                     |
| acm_base_domain                        | example.com                   | No          | DNS domain for the SNO instance|
| acm_cluster_location                   | Unknown                       | No          | SNO server location|
| acm_force_deploy                       | false                         | No          | Force the removal of the instance if already exists |
| acm_disconnected                       | false                         | No          | If set to `true` the pull-secret and CA from the hub are inherited to the spoke cluster |
| acm_ocp_version                        | 4.9.47                        | No          | Full OCP version to install on the spoke cluster. <major>.<minor>.<patch> |
| acm_release_image                      | quay.io/openshift-release-dev/ocp-release:4.9.47-x86_64| No        |The specific release image to deploy. See https://quay.io/openshift-release-dev/ocp-release for the options to choose|
| acm_creation_timeout                   | 90                            | No          | Timeout in minutes for a cluster to be created|
| acm_bmc_user                           | None                          | Yes         | Username for the BMC|
| acm_bmc_pass                           | None                          | Yes         | Password for the BMC|
| acm_bmc_address                        | None                          | Yes         | BMC Address. BMC URLs vary based on the type of BMC and the protocol used to communicate with them. See: [BareMetalHost](https://github.com/metal3-io/baremetal-operator/blob/main/docs/api.md) for details|
| acm_boot_mac_address                   | None                          | Yes         | MAC Address of the interface to be used to bootstrap the node |
| acm_machine_cidr                       | None                          | Yes         | A block of IPv4 or IPv6 addresses in CIDR notation used for the target bare-metal host external communication. Also used to determine the API and Ingress VIP addresses when provisioning Distributed Units (DU) single-node clusters|
| acm_cluster_network_host_prefix         | 23                           | No          | Network prefix for cluster nodes|
| acm_cluster_network_cidr                | 10.128.0.0/14                 | No          | A block of IPv4 or IPv6 addresses in CIDR notation used for communication among cluster nodes|
| acm_service_network_cidr                | 172.30.0.0/16                 | NO          | A block of IPv4 or IPv6 addresses in CIDR notation used for internal communication of cluster services|
| acm_iso_url                            | https://rhcos.mirror.openshift.com/art/storage/releases/rhcos-4.9/49.84.202207192205-0/x86_64/rhcos-49.84.202207192205-0-live.x86_64.iso"                                 | No         | ISO boot Image. See: https://mirror.openshift.com/pub/openshift-v4/dependencies/rhcos/ |
| acm_root_fs_url                        | https://rhcos.mirror.openshift.com/art/storage/releases/rhcos-4.9/49.84.202207192205-0/x86_64/rhcos-49.84.202207192205-0-live-rootfs.x86_64.img                         | No                            | Root FS image. See https://mirror.openshift.com/pub/openshift-v4/dependencies/rhcos/|
|acm_sc                                  |Undefined                       | If no default StorageClass is available | Storage class to use for the `AgentServiceConfig` volumes: `acm_db_volume_size`, `acm_fs_volume_size`, and `acm_img_volume_size`. |
|acm_db_volume_size                      |40Gi                           |No           | This value specifies how much storage it is allocated for storing files like database tables and database views for the clusters. You might need to use a higher value if there are many clusters|
|acm_fs_volume_size                      |50Gi                           |No           | This value specifies how much storage is allocated for storing logs, manifests, and kubeconfig files for the clusters. You might need to use a higher value if there are many clusters|
|acm_img_volume_size                     |40Gi                           |No           | This value specifies how much storage is allocated for the images of the clusters. You need to allow 1 GB of image storage for each instance of Red Hat Enterprise Linux CoreOS that is running. You might need to use a higher value if there are many clusters and instances of Red Hat Enterprise Linux CoreOS|
|acm_user_bundle                         |Undefined                      |No           |CA certificate to be injected to spoke nodes. Requires `acm_disconnected` set to true |
|acm_user_registry                       |Undefined                      |Yes, for disconnected environments | Entries added to the registries.conf file during the initial spoke cluster bootstrap. Must include entries for the OCP release and multicluster-engine images. See examples below|

*Important:* The values defined for the `acm_ocp_version` must match with the images provided for `acm_iso_url` and `acm_root_fs_url` variables.

## Role requirements

### Networking

The proper network connectivity between ACM, the target servers, and BMCs should be in place. During the node bootstrapping a virtual media will be configured using IPMI to initiate the preparation of the SNO host. Target BMCs must be able to reach the multicloud-console.apps.<acm_hub> URL of the ACM instance in order to download the RHCOS discovery ISO.

### DHCP configuration

A DHCP serving for the range defined in the `acm_machine_cidr` must exists.

### DNS configuration

It is recommended that the following DNS entries are already configured in order to allow ACM to import the cluster as a managed instance automatically.

<cluster_name>.<base_domain>
api.<cluster_name>.<base_domain>
apps.<cluster_name>.<base_domain>
multicloud-console.apps.<cluster_name>.<base_domain>

## Mirroring configuration

In disconnected environments this role will get the CA Certificate and pull-secrets from the Hub cluster and apply them to the spoke clusters.

## Override the cluster CA certificate

Pulling the mirroring configs from a cluster can be set by the `acm_disconnected` setting. Also, the CA and the registry.conf files can be overridden by setting values for `acm_user_bundle` and `acm_user_registry` variables as shown in the example below.

## Usage example

See below for some examples of how to use the acm-setup role to configure ACM.

*Deployment of a SNO instance in connected mode*
```yaml
- name: "Deploy an SNO node via ACM"
  vars:
    acm_force_deploy: true
    acm_cluster_name: server9
    acm_base_domain: example.com
    acm_ocp_version: 4.10.32
    acm_release_image: quay.io/openshift-release-dev/ocp-release:4.10.32-x86_64
    acm_bmc_address: 192.168.16.158
    acm_boot_mac_address: b4:96:91:ba:16:5b
    acm_machine_cidr: 192.168.16.0/25
    acm_bmc_user: REDACTED
    acm_bmc_pass: REDACTED
    acm_iso_url: https://mirror.openshift.com/pub/openshift-v4/dependencies/rhcos/4.10/latest/rhcos-4.10.16-x86_64-live.x86_64.iso
    acm_root_fs_url: https://mirror.openshift.com/pub/openshift-v4/dependencies/rhcos/4.10/latest/rhcos-installer-rootfs.x86_64.img
    acm_sc: "assisted-service"
  include_role:
    name: acm-sno
```

*Deployment of a SNO instance in disconnected mode*
```yaml
- name: "Deploy an SNO node via ACM"
  vars:
    acm_force_deploy: true
    acm_cluster_name: server9
    acm_base_domain: example.com
    acm_ocp_version: 4.10.32
    acm_release_image: internal-registry.example.com/openshift-release-dev/ocp-release:4.10.32-x86_64
    acm_bmc_address: 192.168.16.158
    acm_boot_mac_address: b4:96:91:ba:16:5b
    acm_machine_cidr: 192.168.16.0/25
    acm_bmc_user: REDACTED
    acm_bmc_pass: REDACTED
    acm_iso_url: https://mirror.example.comrhcos/4.10/latest/rhcos-4.10.16-x86_64-live.x86_64.iso
    acm_root_fs_url: https://mirror.example.comrhcos/4.10/latest/rhcos-installer-rootfs.x86_64.img
    acm_sc: "assisted-service"
    acm_user_bundle: |
      -----BEGIN CERTIFICATE-----
      REDACTED
      -----END CERTIFICATE-----
    acm_user_registry: |
      unqualified-search-registries = ["registry.access.redhat.com", "docker.io"]
      [[registry]]
      prefix = ""
      location = "jumphost.<my-lab>:4443/ocp4"
      mirror-by-digest-only = true

      [[registry.mirror]]
          location = "registry.<my-lab>:4443/ocp4/openshift4"

      [[registry]]
      prefix = ""
      location = "quay.io/openshift-release-dev/ocp-release"
      mirror-by-digest-only = true
      [[registry.mirror]]
          location = "registry.<my-lab>:4443/ocp4/openshift4"

      [[registry]]
        prefix = ""
        location = "registry.redhat.io/multicluster-engine"
        mirror-by-digest-only = true

        [[registry.mirror]]
          location = "registry.<my-lab>:4443/multicluster-engine"
  include_role:
    name: acm-sno
```

*Deployment of a SNO instance in connected mode - Minimal. Default role values will be used*
```yaml
- name: "Deploy an SNO node via ACM"
  vars:
    acm_force_deploy: true
    acm_bmc_address: 192.168.16.158
    acm_boot_mac_address: b4:96:91:ba:16:5b
    acm_machine_cidr: 192.168.16.0/25
    acm_bmc_user: REDACTED
    acm_bmc_pass: REDACTED
    acm_sc: "assisted-service"
  include_role:
    name: acm-sno
```

# Role Outputs

The following facts can be consumed by other playbooks or roles. In the case of DCI integration, those files will be uploaded to the Job's files section.

```yaml
acm_kubeconfig_text: Kubeconfig file for the new spoke cluster.

acm_kubeconfig_user: Username for the new spoke cluster.

acm_kubeconfig_user: Password for the new spoke cluster.
```

Kubeconfig file and initial user's credentials from the new cluster can be obtained using the following commands:
```Shell
$ CLUSTER_NAME=<cluster_name>
$ oc get secret -n $CLUSTER_NAME $CLUSTER_NAME-admin-kubeconfig -o jsonpath="{.data.kubeconfig}" | base64 --decode > <CLUSTER_NAME>_kubeconfig
$ oc get secret -n $CLUSTER_NAME $CLUSTER_NAME-admin-password -o jsonpath="{.data.username}"
$ oc get secret -n $CLUSTER_NAME $CLUSTER_NAME-admin-password -o jsonpath="{.data.password}"
```

# Troubleshooting

In case of issues during the deployment, please review the logs corresponding to the assisted service deployment.

```Shell
$ oc logs -n multicluster-engine -l app=assisted-service
$ oc logs -n multicluster-engine -l app=assisted-image-service
```

# References

* [acm-setup](../acm-setup/README.md): A role that configures and ACM instance on a running cluster.
* [mirror-ocp-release](../mirror-ocp-release/): A role that mirrors an OCP release to a third-party or local registry.
* [dci-openshfit-agent](https://github.com/redhat-cip/dci-openshift-agent/): An agent that allows the deployment of OCP clusters, it is integrated with DCI (Red Hat Distributed CI).
* [dci-openshfit-app-agent](https://github.com/redhat-cip/dci-openshift-app-agent/): An agent that allows the deployment of workloads and certification testing on top OCP clusters, it is integrated with DCI (Red Hat Distributed CI).
