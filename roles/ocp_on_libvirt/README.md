# OCP_on_libvirt role

Role to setup a libvirt cluster ready to get provisioned with an OpenShift Container Platform release.

## Parameters

Name  | Required  | Default  | Description
------|-----------|----------|-------------
enable_conserver | No | true | Conserver is used to write the console output to a file for later monitoring. Disabling it may be required to monitor the VMs console during ongoing jobs.
enable_redfish | No | false | By default, VMs are created with a Virtual Baseboard Management Controller (vBMC) that can be operated using the IPMI protocol. This parameter enables support for the Redfish protocol based on the sushy_tool Redfish Emulator.
enable_virtualmedia | Only with enable_redfish=true | false | The Redfish protocol uses PXE as the default protocol to provide the hosts with the boot image. Currently we don't support the Redfish/PXE combination so, if you intend to use redfish in your setup, you must also enable virtualmedia.
vbmc_user | Yes | - | User name to authenticate with the Redfish API.
vbmc_pass | Yes | - | User password to authenticate with the Redfish API.
externalMACAddress | Yes | - | MAC address to be assigned to the bootstrap VM, required for DHCP managed static addressing.
bootstrapProvisioningIP | Yes | - | The IP address on the bootstrap VM where the provisioning services run while the installer is deploying the control plane (master) nodes
rhsm_username | Yes | - | User name to log into the [Red Hat Access Portal](https://access.redhat.com). We strongly recommend to have the user name encrypted in an ansible-vault string.
rhsm_password | Yes | - | User password to log into the [Red Hat Access Portal](https://access.redhat.com). We strongly recommend to have the user name encrypted in an ansible-vault string.
redfish_port | No | 8082 | Port the Redfish service is listening on.
cert_country | No | US | Settings for the TLS certificate in the sushy tools Redfish emulator.
cert_state | No | MA | see *cert_country*
cert_locality | No | Westford | see *cert_country*
cert_organization | No | DCI | see *cert_country*
cert_organizational_unit | No | Lab | see *cert_country*


## PCI passthrough example configuration

If you would like to add the following PCI passthrough to the worker node:

```xml
<hostdev mode='subsystem' type='pci' managed='yes'>
  <driver name='vfio'/>
    <source>
      <address domain='0x0000' bus='0x86' slot='0x00' function='0x0'/>
    </source>
</hostdev>
```

Please add the following variables to the libvirt cluster configuration:

```yaml
- name: dciokd-worker-0
  pci_passthrough:
    domain: "0x0000"
    bus: "0x86"
    slot: "0x00"
    function: "0x0"
```

## How to create a libvirt cluster based on Virtualmedia over Redfish

### Example of inventory file

```
all:
  children:
    vm_host:
      hosts:
        libvirthost:
          vbmc_user: MY_USER
          vbmc_password: MY_PASSWORD
    nodes:
      hosts:
        libvirthost
  vars:
    bootstrapProvisioningIP: 192.168.168.168
    externalMACAddress: 01:23:45:67:89:ab
    rhsm_username: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      ### REDACTED ###
    rhsm_password: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      ### REDACTED ### 
```