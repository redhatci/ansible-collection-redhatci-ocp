Virtualbmc role
---------------

This roles installs python-virtualbmc package and configures it for VMs hosted
on the hypervisor. Should be run on the hypervisor host.

Usage examples
==============

1. Run default vbmc configuration::

    - name: Configure vbmc
      hosts: localhost
      any_errors_fatal: true
      tasks:
          - ansible.builtin.include_role:
                name: redhatci.ocp.vbmc
            vars:
                vbmc_nodes: "{{ groups.get('master', []) }}"
