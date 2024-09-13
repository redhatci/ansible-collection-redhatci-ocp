hostedbm
=========
This role creates hosted guest cluster with BM workers.


Requirements
------------

* Access to an OpenShift hosting cluster
* Properly configured kubeconfig file for the hosting cluster access
* Existing CatalogSource.
* The OpenShift hosting cluster should have a way to configure Persistent Volumes (PVs), which could be through the ODF (OpenShift Data Foundation), LVM Storage Operator, or any other suitable method.
* ACM with MCE installed on the hosting cluster
* Metallb operator installed on the hosting cluster
* Metallb configured on the hosting cluster - MetalLB, L2Advertisement, and IPAddressPool configured for range of IP to be used as `APIServer` for hosted clusters.
* AgentServiceConfig and Provisioning configured on the hosting cluster
* DNS configuration

#### DNS configuration
Wildcard DNS entry required by the OpenShift guest cluster must exist.

```Text
*.<cluster_name>.<base_domain>
```

Role Variables
--------------

The following variables can be set to customize the role behavior:

### Required Variables

| Variable Name                | Description                                   | Required | Default Value |
|------------------------------|-----------------------------------------------|----------|---------------|
| `hostedbm_cluster_base_domain` | Base domain for the cluster                   | Yes      | (empty)       |
| `hostedbm_cluster_name`        | Name of the cluster                           | Yes      | (empty)       |
| `hostedbm_guest_ingress_ip`    | Ingress IP(*wildcard IP) for Guest cluster    | Yes      | (empty)       |
| `hostedbm_inventory`           | Inventory of bare metal hosts                 | Yes      | (empty)       |
| `hostedbm_kubeconfig_file`     | Path to the kubeconfig file                   | Yes      | (empty)       |


### Optional Variables

| Variable Name                     | Description                                                           | Required | Default Value                                             |
|-----------------------------------|-----------------------------------------------------------------------|----------|-----------------------------------------------------------|
| `hostedbm_agent_ns`               | Namespace in which Agents will be created, An Agent represents a host that is booted with a discovery image and is ready to be provisioned. | No       | `{{ hostedbm_cluster_name }}-agent`                                                |
| `hostedbm_availability_policy`    | Policy for availability, Options: HighlyAvailable, SingleReplica      | No       | `SingleReplica`                                           |
| `hostedbm_cluster_ns`             | The HostedCluster's namespace name                                    | No       | `clusters`                                                |
| `hostedbm_inject_dns`             | Enables custom DNS injection. Set to true to pass custom DNS configuration; false disables it. | No       | `false`                                                |
| `hostedbm_inject_dns_nameserver`  | Specifies the custom DNS server(s) to use when `hostedbm_inject_dns` is set to true. | No       | "" (empty string)                                               |
| `hostedbm_infraenv_name`          | Name of the infrastructure environment                                | No       | `{{ hostedbm_cluster_name }}-infraenv`                    |
| `hostedbm_location_label`         | Location label                                                        | No       | `""` (empty string)                                       |
| `hostedbm_node_pool_replicas`     | Number of replicas for the node pool                                  | No       | `1`                                                       |
| `hostedbm_no_log`                 | Logging configuration                                                 | No       | `false`                                                   |
| `hostedbm_out_dir`                | Output directory                                                      | No       | `{{ hostedbm_working_dir }}/out`                          |
| `hostedbm_release_image`          | Release image                                                         | No       | `quay.io/openshift-release-dev/ocp-release:4.15.11-multi` |
| `hostedbm_storage_class`          | Storage class                                                         | No       | `lvms-vg1`                                                |
| `hostedbm_working_root_dir`       | Working root directory                                                | No       | `/tmp/hostedcluster`                                      |
`hostedbm_bm_cpo_override_image`    | Override Hypershift operator image for HCP Control Plane              | No       | undefined |
|-----------------------------------|-----------------------------------------------------------------------|----------|-----------------------------------------------------------|

Example Playbook
----------------

```yaml
---
- hosts: localhost
  tasks:
    - name: Create Guest cluster
      include_role:
        name: hostedbm
      vars:
        hostedbm_cluster_base_domain: <base domain>
        hostedbm_cluster_name: <cluster name>
        hostedbm_guest_ingress_ip: <ingress ip>
        hostedbm_inventory:
          - name: <server#1>
            address: idrac-virtualmedia://<idrac ip>/redfish/v1/Systems/System.Embedded.1
            # for HP servers, use redfish virtual media
            # address: redfish-virtualmedia://<ilo IP>/redfish/v1/Systems/1
            bootMACAddress: <mac address>
            username: <idrac/ilo username>
            password: <idrac/ilo password>
          - name: <server#2>
            address: idrac-virtualmedia://<idrac ip>/redfish/v1/Systems/System.Embedded.1
            # for HP servers, use redfish virtual media
            # address: redfish-virtualmedia://<ilo IP>/redfish/v1/Systems/1
            bootMACAddress: <mac address>
            username: <idrac/ilo username>
            password: <idrac/ilo password>
```
