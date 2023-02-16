## PCI passthrough example configuration

If you would like to add the following PCI passthrough to the worker node:

```xml
<interface type='hostdev' managed='yes'>
   <mac address='52:54:00:00:02:04'/>
   <driver name='vfio'/>
   <source>
    <address type='pci' domain='0x0000' bus='0x86' slot='0x00' function='0x2'/>
   </source>
 </interface>
```

Please add the following variables to the libvirt cluster configuration:

```yaml
- name: dciokd-worker-0
  pci_passthrough:
    vf_mac_address: "52:54:00:00:02:04"
    domain: "0x0000"
    bus: "0x86"
    slot: "0x00"
    function: "0x2"
```