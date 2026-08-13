# RedHat CI OCP collection Playbooks
This folder contains the playbooks that support the Ansible roles of the collection.

## Playbook list
| Role                                                                                                                                 | Name                       | Description
|--------------------------------------------------------------------------------------------------------------------------------------|----------------------------|------------------------------------------------------------------------------------------------------
| [redhatci.ocp.multibench_run](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/multibench_run/README.md)  |  multibench_setup_host.yml | This playbook installs the crucible binaries needed for the proper execution of the Multi-bench role.
| [redhatci.ocp.conserver](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/conserver/README.md)            |  conserver-setup.yml       | This playbook configures conserver for one or more clusters, supporting IPMI SOL, libvirt socket, Dell iDRAC SSH, and HP iLO SSH console types.

## Multi-bench playbook
### Variables

| Variable                  | Default                        | Type    | Required | Description                                                                          |
|---------------------------|--------------------------------|---------|----------|--------------------------------------------------------------------------------------|
| multibench_quay_token     | null                           | string  | true     | Path to the file which contains the credentials for accessing the container registry |
| multibench_disconnected   | false                          | boolean | false    | Set it to 'true' if the multibench host does not have access to the Internet         |
| multibench_local_registry | quay.io/crucible/client-server | String  | false    | Registry that will be used to pull the crucible images                               |
| multibench_git_name       | Smith                          | String  | false    | Name displayed in on git                                                             |
| multibench_git_email      | ansible@whatever.com           | String  | false    | email displayed in on git                                                            |

### Requirements
The playbook will be run on the host `multibench`, make sure it is correctly defined in your inventory, here is an example:
```yaml
  children:
    multibench:
      hosts:
        my-host.my-lab:
          ansible_user: root
```
Also, the installation needs to be run as root, verify that the ansible_user is correctly set.

## Conserver setup playbook
### Variables

| Variable              | Default     | Type         | Required | Description                                                     |
|-----------------------|-------------|--------------|----------|-----------------------------------------------------------------|
| conserver_jumphost    | `localhost`  | string      | false    | Inventory hostname of the host running conserver                |
| conserver_clusters    | —           | list(string) | true     | List of cluster group names to configure consoles for           |

### Requirements
Each cluster group must exist in your inventory, with nodes having the appropriate
`console_type` and BMC credential host variables set. See the
[conserver role README](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/conserver/README.md)
for details.

Example:
```yaml
  children:
    cluster1:
      hosts:
        node1.cluster1.example.com:
          name: node1
          console_type: dell_idrac_ssh
          bmc_address: 192.168.1.10
          bmc_user: root
          bmc_password: calvin
```
