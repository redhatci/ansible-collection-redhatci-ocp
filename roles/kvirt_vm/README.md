# kvirt_vm role

This role allows the deployment of a Kubevirt virtual machine. In order to execute the role a running OpenShift cluster and its credentials are required. i.e. through the KUBECONFIG environment variable.

The role is aimed for deployment if virtual nodes for OCP deployments, so only the root disk is created.

```shell
export KUBECONFIG=<path_kubeconfig>
```

Main tasks:
- Validate the storage class
- Check the required operators (CNV)
- Create the VM and set it to the desired state

This role only been tested in x86_64 architectures.

## Variables

| Variable                               | Default                       | Required    | Description                                   |
| -------------------------------------- | ----------------------------- | ----------- | ----------------------------------------------|
| kvirt_vm_name                          |                               | yes         | VM name                                       |
| kvirt_vm_force                         | false                         | no          | Destroy the VM if already exists              |                              
| kvirt_vm_namespace                     | default                       | no          | VM namespace                                  |
| kvirt_vm_storage_class                 | <default>                     | no          | Root disk storage class                       |
| kvirt_vm_memory                        | 8Gi                           | no          | VM memory                                     |
| kvirt_vm_disk_mode                     | ReadWriteOnce                 | no          | VM disk volume mode                           |
| kvirt_vm_disk_size                     | 60Gi                          | no          | Root disk size                                |         
| kvirt_vm_os                            | rhcos                         | no          | VM Operating system annotation                |
| kvirt_vm_cpu_cores                     | 8                             | no          | VM CPU cores                                  |
| kvirt_vm_cpu_sockets                   | 1                             | no          | VM CPU sockets                                |
| kvirt_vm_cpu_threads                   | 1                             | no          | VM CPU threads                                | 
| kvirt_vm_network_interface_multiqueue  | true                          | no          | Enable NIC multiqueue                         |
| kvirt_vm_running                       | false                         | no          | Set the initial VM power state                |  
| kvirt_vm_node_selector                 |                               | no          | Configure nodes selector                      | 
| kvirt_vm_interfaces                    | virtio/masquerade             | no          | Network interface definitions                 |
| kvirt_vm_networks                      | Pod network                   | no          | VM network definitions                        |

## Usage examples

See below for some examples of how to use the kvirt_vm role to create a VM.

Deploy a VM with custom configs
```yaml
- name: "Create a kvirt VM"
  vars:
    kvirt_vm_name: test
    kvirt_vm_force: true
    kvirt_vm_namespace: myns
    kvirt_vm_memory: 8Gi
    kvirt_vm_disk_mode: ReadWriteOnce
    kvirt_vm_disk_size: 60Gi
    kvirt_vm_os: rhcos
    kvirt_vm_cpu_cores: 8
    kvirt_vm_cpu_sockets: 1
    kvirt_vm_cpu_threads: 1
    kvirt_vm_network_interface_multiqueue: true
    kvirt_vm_running: false
    kvirt_vm_node_selector:
      kubernetes.io/hostname: master-1
    kvirt_vm_interfaces:
      - masquerade: {}
        model: virtio
        name: default
    kvirt_vm_networks:
      - name: default
        pod: {}
  ansible.builtin.include_role:
    name: redhatci.ocp.kvirt_vm
```

Deploy a VM with default settings
```yaml
- name: "Create a kvirt VM"
  vars:
    kvirt_vm_name: test
  ansible.builtin.include_role:
    name: redhatci.ocp.kvirt_vm
```

Deploy a VM with SRIOV support
```yaml
- name: "Create a kvirt VM"
  vars:
    kvirt_vm_name: test
    kvirt_vm_interfaces:
      - name: mellanox_port0
        sriov: {}
        macAddress: "52:54:00:00:20:20"
      - name: mellanox_port1
        sriov: {}
        macAddress: "52:54:00:00:20:21"
    kvirt_vm_networks:
      - multus:
          networkName: mellanox-net0
        name: mellanox_port0
      - multus:
          networkName: mellanox-net1
        name: mellanox_port1
  ansible.builtin.include_role:
    name: redhatci.ocp.kvirt_vm
```

# Troubleshooting

# References
