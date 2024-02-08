# kvirt_vm role

This role allows the deployment of Kubevirt virtual machines. In order to execute the role a running OpenShift cluster and its credentials are required. i.e. through the KUBECONFIG environment variable.

The role is aimed for deployment of virtual nodes for OCP deployments, so only the root disk is created.

```shell
export KUBECONFIG=<path_kubeconfig>
```

Main tasks:
- Validate the storage class
- Check the required operators (CNV)
- Create the VMs and set it to the desired state

This role has been tested only in x86_64 architectures.

# Role variables
| Variable                      | Required  | Type    | Default   | Description
| ----------------------------- | --------- | ------- | --------- | -----------
| vms_config_file               | Yes       | String  | Undefined | The configuration file with the VM's settings
| vms_settings                  | Yes       | List    | Undefined | A list with the settings for each VM

## VM configs
| Variable                      | Default                       | Required    | Description
| -----------------------------------------------    ---------- | ----------- | ---------------------------------
| name                          |                               | yes         | VM name
| force                         | false                         | no          | Destroy the VM if already
| namespace                     | default                       | no          | VM namespace
| storage_class                 | <default>                     | no          | Root disk storage class
| memory                        | 8Gi                           | no          | VM memory
| disk_mode                     | ReadWriteOnce                 | no          | VM disk volume mode
| disk_size                     | 60Gi                          | no          | Root disk size
| os                            | rhcos                         | no          | VM Operating system annotation
| cpu_cores                     | 8                             | no          | VM CPU cores
| cpu_sockets                   | 1                             | no          | VM CPU sockets
| cpu_threads                   | 1                             | no          | VM CPU threads
| network_interface_multiqueue  | true                          | no          | Enable NIC multiqueue
| running                       | false                         | no          | Set the initial VM power state
| node_selector                 |                               | no          | Configure nodes selector
| interfaces                    | virtio/masquerade             | no          | Network interface definitions
| networks                      | Pod network                   | no          | VM network definitions

## Usage examples

See below for some examples of how to use the kvirt_vm role to create a VM.

Deploy a VM with custom configs

```yaml
- name: "Create a kvirt VM"
  vars:
   vms_config_file: /path/to/vms-config-file.yaml
  ansible.builtin.include_role:
    name: redhatci.ocp.kvirt_vm
```

Tree VMs with default settings
```yaml
---
vm_configs:
  - name: master-0
  - name: master-1
  - name: master-2
```

Generic VM definition
```yaml
---
vms_configs:
  - name: test
    force: true
    namespace: myns
    memory: 8Gi
    disk_mode: ReadWriteOnce
    disk_size: 60Gi
    os: rhcos
    cpu_cores: 8
    cpu_sockets: 1
    cpu_threads: 1
    network_interface_multiqueue: true
    running: false
    node_selector:
      kubernetes.io/hostname: master-1
    interfaces:
      - masquerade: {}
        model: virtio
        name: default
    networks:
      - name: default
        pod: {}
      ansible.builtin.include_role:
        name: redhatci.ocp.kvirt_vm
```

VM config file with SRIOV settings
```yaml
---
vm_configs:
  - name: master-1
    interfaces:
      - macAddress: "54:54:00:00:21:20"
        name: mellanox_port0
        sriov: {}
      - macAddress: "54:54:00:00:21:21"
        name: mellanox_port1
        sriov: {}
    networks:
      - multus:
          networkName: mellanox-net0
        name: mellanox_port0
      - multus:
          networkName: mellanox-net1
        name: mellanox_port1
```
