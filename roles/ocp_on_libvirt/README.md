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