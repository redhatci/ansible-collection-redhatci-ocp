# conserver

This role installs and configures [conserver](https://www.conserver.com/) to provide
serial console access to cluster nodes. It supports four console types:

- **IPMI Serial-over-LAN (SOL)** — classic IPMI SOL via ipmitool
- **Libvirt socket** — virtual machine consoles via socat/UNIX socket
- **Dell iDRAC SSH** — Dell iDRAC serial console via SSH (`console com2`)
- **HP iLO SSH** — HP iLO virtual serial port via SSH (`vsp`)

## Requirements

- `conserver`, `conserver-client`, `ipmitool`, `socat`, and `sshpass` packages
  (installed automatically by the role).
- For Dell iDRAC SSH and HP iLO SSH console types, SSH access to the BMC must
  be enabled and the `sshpass` package must be available on the conserver host.

## Role Variables

### Role-level variables (set per invocation)

| Variable      | Type         | Required | Description                                                                                    |
|---------------|--------------|----------|------------------------------------------------------------------------------------------------|
| `cluster`     | string       | yes      | Cluster name. Used to namespace log directories and conserver config file names.               |
| `cluster_nodes` | list(str)  | yes      | List of inventory hostnames in the cluster to configure consoles for.                          |

### Host variables (set per node in inventory)

| Variable                          | Type    | Required | Default  | Description                                                                                              |
|-----------------------------------|---------|----------|----------|----------------------------------------------------------------------------------------------------------|
| `console_type`                    | string  | no       | `ipmi`   | Console type: `ipmi`, `dell_idrac_ssh`, or `hp_ilo_ssh`. If unset and `socket_console` is true, libvirt socket is used. |
| `socket_console`                  | boolean | no       | `false`  | Set to `true` to use a libvirt socket console (overrides `console_type`).                                |
| `bmc_address` / `ipmi_address`    | string  | yes*     | —        | BMC/IPMI hostname or IP address. `bmc_address` takes precedence over `ipmi_address`.                     |
| `bmc_user` / `ipmi_user`          | string  | yes*     | —        | BMC/IPMI username. `bmc_user` takes precedence over `ipmi_user`.                                         |
| `bmc_password` / `ipmi_password`  | string  | yes*     | —        | BMC/IPMI password. `bmc_password` takes precedence over `ipmi_password`.                                 |
| `ipmi_port`                       | integer | no       | `623`    | IPMI UDP port (IPMI SOL only).                                                                           |
| `name`                            | string  | yes      | —        | Short hostname used as console name in conserver (e.g. `node1`).                                         |

*Required for IPMI SOL, Dell iDRAC SSH, and HP iLO SSH console types.

### Accumulated lists (managed internally)

| Variable                       | Type      | Default | Description                                                                   |
|--------------------------------|-----------|---------|-------------------------------------------------------------------------------|
| `conserver_sol_hosts`          | list(str) | `[]`    | Nodes auto-detected as supporting IPMI SOL. Populated during role execution.  |
| `conserver_socket_hosts`       | list(str) | `[]`    | Nodes configured for libvirt socket console. Populated during role execution. |
| `conserver_dell_idrac_ssh_hosts` | list(str) | `[]` | Nodes configured for Dell iDRAC SSH console. Populated during role execution. |
| `conserver_hp_ilo_ssh_hosts`   | list(str) | `[]`    | Nodes configured for HP iLO SSH console. Populated during role execution.     |

## Example Inventory

```yaml
all:
  hosts:
    # IPMI SOL node (classic)
    node-ipmi-1:
      name: node-ipmi-1
      bmc_address: 192.168.1.10
      bmc_user: admin
      bmc_password: secret

    # Libvirt socket console (virtual machine)
    node-libvirt-1:
      name: node-libvirt-1
      socket_console: true

    # Dell iDRAC SSH console
    node-idrac-1:
      name: node-idrac-1
      console_type: dell_idrac_ssh
      bmc_address: 192.168.1.20
      bmc_user: root
      bmc_password: calvin

    # HP iLO SSH console
    node-ilo-1:
      name: node-ilo-1
      console_type: hp_ilo_ssh
      bmc_address: 192.168.1.30
      bmc_user: Administrator
      bmc_password: secret

  children:
    mycluster:
      hosts:
        node-ipmi-1:
        node-libvirt-1:
        node-idrac-1:
        node-ilo-1:
```

## Example Playbook

```yaml
---
- name: Configure conserver for a cluster
  hosts: conserver_host
  gather_facts: false
  tasks:
    - name: Configure conserver
      ansible.builtin.include_role:
        name: redhatci.ocp.conserver
      vars:
        cluster: mycluster
        cluster_nodes: "{{ groups['mycluster'] }}"
```

For multi-cluster setups, use the `playbooks/conserver-setup.yml` playbook
which loops over `conserver_clusters` automatically.

## License

Apache-2.0
