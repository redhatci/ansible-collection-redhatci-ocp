Role Name
=========

Role to setup Openshift Container Storage (OCS)
and integrate with Internal Local Storage operators in OCP 4.X
or integrate with External RHCS cluster (ODF External Mode)


Requirements
------------

- oc client
- python3-kubernetes (community.kubernetes.k8s)
- Bash session and OCP account with cluster-admin privileges
- In ODF External Mode requires access to RHCS cluster


Role Variables
--------------

```YAML
# defaults variables for ocs-setup

### Local Storage Operator variables
# (Required) Channel versions to use, namespace and operators names
local_storage_operator: local-storage-operator
local_storage_namespace: openshift-local-storage

# (Required) Name of the LSO Storage Class
local_storage_class: localblock

# (Required) Type of LSO Volume Mode, either filesystem or block
local_volume_mode: block

# (Required) Replica size
replica_size: 3

### OCS Storage Operator variables
# (Required) Channel versions to use, namespace and operators names
ocs_storage_operator: ocs-operator
ocs_storage_namespace: openshift-storage

# (Optional) Whether to enable Multicloud Object Gateway (nooba)
enable_object_gateway: false

# (Required) default storageclass annotation
default_storageclass_annotation: '{"storageclass.kubernetes.io/is-default-class": "true"}'
```

Inventory Groups and Variables
--------------

```YAML
[all:vars]
# (Required) whether to enable or not Local Storage Operator, true or false
# required when using enable_ocs=true and ocs_install_type=internal
enable_lso=

# (Required) whether to enable or not OCS, true or false
enable_ocs=

# (Required) when enable_ocs=true to specify the integration type with ODF/OCS
# Two possible options: internal or external
ocs_install_type=

# (Required) when ocs_install_type=external, then pass JSON output generated from RHCS
# with ceph-external-cluster-details-exporter.py script
external_ceph_data='JSON_PAYLOAD'

# (Optional) when enable_lso=true List of disk devices per node to use for LSO
# If not specified, it will use all the local disks available
# comma separated, all servers must have the same
local_storage_devices=["/dev/sdX", "/dev/sdY", "/dev/sdZ"]

# (Optional) when enable_ocs=true name of the storageclass to set as default
ocs_default_storage_class=ocs-storagecluster-cephfs

# (Required) Group of nodes where to install OCS
[ocs_nodes:children]
masters

# (Required) Label to identify the Storage Nodes
[ocs_nodes:vars]
lso_label='{"cluster.ocs.openshift.io/openshift-storage": ""}'
```

Dependencies
------------
- olm-operator

This role does not installs the operators, it depends on olm-operator.
See [olm-operator readme](https://github.com/redhat-cip/dci-openshift-agent/blob/master/common-roles/olm-operator/README.md) for more details.


Example Inventory
----------------

File: /etc/dci-openshift-agent/hosts
```YAML
[all:vars]
...
enable_lso=true
enable_ocs=true
ocs_install_type=internal
local_storage_devices=["/dev/sdb", "/dev/sdc", "/dev/sdd"]

[ocs_nodes:children]
masters

[ocs_nodes:vars]
lso_label='{"cluster.ocs.openshift.io/openshift-storage": ""}'
```

Example Playbook
----------------

File: deploy-odf.yml
```YAML
---
- name: "Deploy OCS and LocalStorage"
  hosts: provisioner
  roles:
    - odf-setup
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
