# setup_lvms

An Ansible role to setup and manage the LVMS (Logical Volume Manager Storage) operator on OpenShift clusters.

## Description

This role configures the LVMS operator (which must already be installed) by creating LVMCluster resources, waiting for them to become ready, and creating associated StorageClass resources. It also provides cleanup functionality to remove all LVMS-related resources.

## Requirements

- OpenShift 4.x cluster with LVMS operator already installed
- Ansible 2.9 or higher
- `kubernetes.core` collection installed (`ansible-galaxy collection install kubernetes.core`)
- Valid kubeconfig with sufficient permissions to manage LVMCluster, StorageClass, and PVC resources
- An ansible inventory with at least one node in the openshift cluster with an available disk to use for local storage

## Role Variables

### Required Variables

These variables **must** be defined when using this role:

| Variable | Description | Example |
|----------|-------------|---------|
| `sl_dev_class_name` | Name of the device class for LVMS | `nvme` |
| `sl_dev_selector_paths` | List of disk path patterns for device selection | `["/dev/nvme0n1"]` |

### Optional Variables

These variables have default values and can be overridden:

| Variable | Default | Description |
|----------|---------|-------------|
| `sl_lvm_cluster_name` | `lvmcluster` | Name of the LVMCluster resource |
| `sl_lvm_namespace` | `openshift-storage` | Namespace where LVMS resources are created |
| `sl_fstype` | `xfs` | Filesystem type for logical volumes (xfs or ext4) |
| `sl_node_selector` | worker | Role of the node where LVMS operator will lookup disks |
| `sl_storage_class` | `None` | Name of the StorageClass to create |
| `sl_force_wipe_devices` | `false` | Whether to force wipe devices and destroy all data when creating LVMCluster |
| `sl_wait_retries` | `60` | Number of retries when waiting for resources |
| `sl_wait_delay` | `5` | Delay in seconds between retry attempts |

### Action Control Variable

| Variable | Description | Values |
|----------|-------------|--------|
| `sl_action` | Controls whether to setup or cleanup LVMS | `setup` (default), `teardown` |

## Dependencies

None.

## Example Playbooks

### Inventory

```yaml
---
all:
  vars:
    nodes:
      vars:
        ansible_ssh_extra_args: -o ConnectTimeout=360 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ~/.ssh/id_ed25519
        ansible_user: core
      children:
        masters:
          vars:
            role: master
          hosts:
            sno1.cluster1.example.lab:
              ansible_host: 172.16.0.100
...
```

### Setup LVMS

```yaml
---
- name: Setup LVMS on OpenShift cluster
  hosts: localhost
  gather_facts: false
  vars:
    sl_dev_class_name: "nvme"
    sl_dev_selector_paths: ["/dev/nvme0n1"]
  roles:
    - setup_lvms
```

### Setup LVMS with custom configuration

```yaml
---
- name: Setup LVMS with custom settings
  hosts: localhost
  gather_facts: false
  vars:
    sl_dev_class_name: "ssd"
    sl_dev_selector_paths: ["/dev/sdb"]
    sl_lvm_cluster_name: "my-lvm-cluster"
    sl_storage_class: "fast-storage"
    sl_fstype: "ext4"
    sl_wait_retries: 90
    sl_wait_delay: 10
    sl_node_selector: control-plane
  roles:
    - setup_lvms
```

### Teardown LVMS

```yaml
---
- name: Cleanup LVMS resources
  hosts: localhost
  gather_facts: false
  vars:
    sl_dev_class_name: "nvme"
    sl_dev_selector_paths: ["/dev/nvme0n1"]
    sl_action: "teardown"
  roles:
    - setup_lvms
```

## What This Role Does

### Setup Mode (default)

1. Creates an LVMCluster custom resource with the specified device class and selector
2. Waits for the LVMCluster to reach "Ready" state (with configurable retries)
3. Waits for the LVMVolumeGroup to be created
4. Creates a StorageClass that uses the LVMS provisioner

### Teardown Mode (`sl_action: teardown`)

1. Deletes the custom StorageClass
2. Deletes the default LVMS StorageClass
3. Deletes the LVMCluster resource
4. Deletes the LVMVolumeGroup

## License

Apache-2.0

## Author Information

Created for OpenShift LVMS operator management.
