Role Name
=========

Role to setup Openshift Container Storage (OCS) and integrate with Internal Local Storage operators in OCP 4.X or integrate with External RHCS cluster (ODF External Mode)

Requirements
------------

- oc client
- python3-kubernetes (community.kubernetes.k8s)
- Bash session and OCP account with cluster-admin privileges
- In ODF External Mode requires access to RHCS cluster


Role Variables
--------------

| Variable                         | Default                       | Type         | Required    | Description                                                              |
| -------------------------------- | ----------------------------- |------------- | ----------- | -------------------------------------------------------------------------|
| local_storage_operator           | local-storage-operator        | String       | No          | LSO operator name                                                        |
| openshift-local-storage          | openshift-local-storage       | String       | No          | LSO namespace                                                            |
| local_storage_class              | localblock                    | String       | No          | Type of LSO Volume Mode, either filesystem or block                      |
| local_volume_mode                | localblock                    | String       | No          | Type of LSO Volume Mode, either filesystem or block                      |
| replica_size                     | 3                             | String       | No          | Replica size                                                             |
| ocs_storage_operator             | ocs-operator                  | String       | No          | OCS operator name                                                        |
| ocs_storage_namespace            | openshift-storage             | String       | No          | OCS namespace                                                            |
| default_storageclass_annotation  | '{"storageclass.kubernetes.io/is-default-class": "true"}'  | String       | No          | Default storageclass annotation             |
| external_ceph_data               |                               | JSON         | No          | A JSON payload generated from RHCS                                       |
| ocs_install_type                 |                               | String       | Yes         | `internal` for LSO, `external` for Ceph/RHCS                             |
| local_storage_devices            |                               | List         | No          | For LSO, a list of local devices that will be use as backend             |
| ocs_default_storage_class        | storagecluster-cephfs         | String       | No          | Default storage class name                                               |
| gatherer_image                   | registry.access.redhat.com/ubi8/ubi | String | No          | Image for disk-gatherer deployment                                       |

Inventory Groups and Variables
--------------

```YAML
[all:vars]
# Two possible options: internal or external
ocs_install_type=

# (Required) when ocs_install_type=external, then pass JSON output generated from RHCS
# with ceph-external-cluster-details-exporter.py script
external_ceph_data='JSON_PAYLOAD'

# (Optional) when enable_lso=true List of disk devices per node to use for LSO
# If not specified, it will use all the local disks available
# comma separated, all servers must have the same
local_storage_devices=["/dev/sdX", "/dev/sdY", "/dev/sdZ"]

# (Optional) Default storage class name
ocs_default_storage_class=ocs-storagecluster-cephfs

# (Required) Group of nodes where to install OCS
[ocs_nodes:children]
workers

# (Required) Label to identify the Storage Nodes
[ocs_nodes:vars]
labels={"cluster.ocs.openshift.io/openshift-storage": ""}
```

Dependencies
------------
- olm_operator
This role does not installs the operators, it depends on olm_operator.
See [olm_operator readme](https://github.com/redhatci/ansible-collections-redhatci-ocp/blob/master/common-roles/olm_operator/README.md) for more details.

- label_node
This role can help to apply the inventory defined label to the OCP cluster nodes.
See [olm_operator readme](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/master/common-roles/label_nodes/README.md) for more details

Example Inventory
----------------

File: /etc/dci-openshift-agent/hosts
```toml
[all:vars]
...
ocs_install_type=internal
local_storage_devices=["/dev/sdb", "/dev/sdc", "/dev/sdd"]

[ocs_nodes:children]
workers

[ocs_nodes:vars]
labels={"cluster.ocs.openshift.io/openshift-storage": ""}
```

Example Playbook
----------------

File: deploy-odf.yml
```YAML
---
- name: "Deploy OCS and LocalStorage"
  hosts: provisioner
  roles:
    - odf_setup
```

Run Playbook
----------------


```bash
# Authenticate
$ export KUBECONFIG=/path/of/your/kubeconfig

# Perform installation
$ ansible-playbook -i /etc/dci-openshift-agent/hosts deploy-odf.yml
```

License
-------

Apache 2.0


Author Information
------------------
author: Telco Partner CI
company: Red Hat
