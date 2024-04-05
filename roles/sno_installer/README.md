# SNO-Installer role

This role contains playbooks to deploy OCP SNO in a very opinionated fashion. This might not correspond to the official or recommended way to deploy SNO. For SNO on libvirt it uses a live CD image to bootstrap a VM, and for baremetal it uses dnsmasq as TFTP/DNS/DHCP server and bootstrap a physical node. 

NOTE: Disconnected support only available on Baremetal SNO, virtual SNO still requires connected environment

## Minimum Required variables

For any type of SNO installation, these variables are always required

- pull secret # pull secret content
- domain # FQDN to use
- cluster # name of the cluster
- dir # directory to store deployment files
- extcidrnet # CIDR of the network to use
- install_type # DCI use only, options: ipi (default), sno
- pull_image # The "Pull From" `ocp_release` image to use from the release.txt file. In DCI this is provided in the OCP component.

## SNO Virtual

Steps and playbooks to help you setup your environment are documented [here](https://github.com/redhat-cip/dci-openshift-agent/tree/master/samples/sno_on_libvirt#readme)
## SNO Baremetal

## Provisioner node setup
- Install latest RHEL 8 release
- Subscribe the node to Base, Appstream, and EPEL repositories
- Create kni user and set sudo privileges without password
- Generate a ssh key for the kni user

### Required variables for SNO Baremetal

The variables below are required in the inventory

sno_install_type == baremetal
sno_extnet_ip # IP address to use on the SNO node from "extcidrnet"
- installation_disk  # Disk path (default /dev/sda)
- ipmi_address  # IP address of the BMC interface
- ipmi_user  # User with administrator privileges
- ipmi_password  # Password of the BMC user
- ipmi_port  # Port of the BMC console
- baremetal_mac  # MAC address of the Baremetal NIC 
- extcidrrouter  # define the gateway to use
- extcidrdns  # IP address of the DNS server


### DNS Entries Required

The following DNS entries will be configured in the dnsmasq service, but if using a corporate DNS then add API, Apps and SNO records there.

- api.{{ cluster }}.{{ domain }}  =>  {{ sno_extnet_ip }}  # IP of the SNO node
- apps.{{ cluster }}.{{ domain }}  =>  {{ sno_extnet_ip }}  # IP of the SNO node
- sno.{{ cluster }}.{{ domain }}  =>  {{ sno_extnet_ip }} # DNS Name of the SNO node

### Disable cache

Cache can be disabled with the variable cache_enabled=false, but the following variables with their values need to be defined with the URLs where the files can be downloaded. Example:

- coreos_pxe_rootfs_url=http://<web-server>/rhcos-48.84.202109241901-0-live-rootfs.x86_64.img
- coreos_sno_ignition_url=http://<web-server>:8080/4.8.15/sno.ign

### TFTP

To specify a server for hosting the dnsmasq service, include a tftp_host group in the inventory. If not defined, the provisioner node will be chosen.
See example in roles/sno_node_prep/tests/inventory-baremetal.

NOTE: if using a corporate DHCP and decide to use the SNO dnsmasq TFTP:
 - blacklist MAC of SNO Baremetal interface
 - make sure there is no service listening on port 53/udp in TFTP host that could interfere with dnsmasq service of the SNO baremetal deployment.

Also, if you setup dnsmasq_enabled = false (default is true) no dnsmasq service will be configure, and you can setup manually and choose the TFTP/DHCP/DNS services of your preference.

Finally if you do not want to leave the SNO deployment to download the kernel and initramfs images, you can previously downloaded them and and pass the variables of kernel and initramfs images with the path of the file in the tftp server. Example:

- coreos_pxe_kernel_path=/images/rhcos-48.84.202109241901-0-live-kernel-x86_64
- coreos_pxe_initramfs_path=/images/rhcos-48.84.202109241901-0-live-initramfs.x86_64.img

### Registry

To specify a server hosting the registry include registry_host group in the inventory. Only required in disconnected mode. SNO roles do not configure a registry service, only make use of a provisioned registry. 
See registry variables in the inventory example in roles/sno_node_prep/tests/inventory-baremetal


### Prepare the jumpbox CI and start a deployment

Note: This applies to DCI deployments only

- Same commands and DCI tools are used. See main DCI documentation [To prepare the jumpbox](https://github.com/redhat-cip/dci-openshift-agent/blob/master/README.md#installation-of-dci-jumpbox)
- Examples of SNO inventories can be found in:
  * [SNO Virtual](https://github.com/redhat-cip/dci-openshift-agent/blob/master/samples/sno_on_libvirt/examples/hosts-libvirt)
  * [SNO Baremetal](https://github.com/redhat-cip/dci-openshift-agent/blob/master/samples/sno_on_libvirt/examples/hosts-baremetal)

- Review the doc to [Start the DCI agent](https://github.com/redhat-cip/dci-openshift-agent/blob/master/README.md#starting-the-dci-ocp-agent)

