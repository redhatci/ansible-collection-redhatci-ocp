Ansible role: create_rhde_builder
=================================

This role bootstraps a VM used as a [Red Hat Device Edge](https://www.redhat.com/en/technologies/device-edge) image builder

The VM will be based on an official RHEL qcow2 image which will be downloaded using a RHSM offline token. Get it [here][rhsm_offline_token]

Accessing the builder system
----------------------------

The resulting VM will be added to the inventory as: `{{ rhde_image_name }}` (defaults to `rhde-builder-<rhel version>` / `rhde-builder-9.3`).
It will be part of the inventory group `rhde_builder`.

The user's public ssh key (`${HOME}/.ssh/id_rsa.pub` override with `rhde_builder_ssh_pubkey` param) will be installed
into the newly created system for `root` and `cloud-user`. The user's private ssh key (`${HOME}/.ssh/id_rsa` override with `rhde_builder_ssh_privkey`)
will be used to access the newly created system.

Parameters
----------

Mandatory parameters for this role are:
- `rhde_builder_rhsm_api_offline_token`: a RHSM offline token. Get it [here][rhsm_offline_token]
- `rhde_builder_rhsm_org_id`: the RHSM org id to register the RHEL system
- `rhde_builder_rhsm_activation_key`: the RHSM activation key to register the RHEL system

All other intersting parameters are defined in [defaults/main.yml](defaults/main.yml) and described in [meta/argument_specs.yml](meta/argument_specs.yml)

[rhsm_offline_token]: https://access.redhat.com/management/api

Example usage
-------------
Create the system
``` ansible playbook
---
- name:
  hosts: localhost
  tasks:
    - include_role:
        name: create_rhde_builder
      vars:
        # set them into your inventory
        rhde_builder_rhsm_api_offline_token: <rhsm_offline_token>
        rhde_builder_rhsm_org_id: <rhsm_org_id>
        rhde_builder_rhsm_activation_key: <rhsm_activation_key>
...
```

Cleanup everything
```
---
- name:
  hosts: localhost
  tasks:
    - include_role:
        name: create_rhde_builder
        tasks_from: cleanup_rhde_builder.yml
      vars:
        rhde_builder_cleanup_remove_base_rhel_image: true
...
```
