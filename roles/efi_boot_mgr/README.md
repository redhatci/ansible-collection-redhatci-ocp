# EFI Boot Manager

Remove the non-active UEFI boot entries from OCP nodes.

> IMPORTANT: This role removes permantently UEFI boot entries, use it with care.

## Requirements

A valid *KUBECONFIG* env variable pointing to a kubeconfig file.

## Variables

| Variable      | Default             | Required  | Description                                           |
| ------------- | ------------------- | --------- | ----------------------------------------------------- |
| ebm_nodes     | \<undefined\>       | Yes       | A list of OCP node names to manage their Boot order.  |
| ebm_oc_path   | /usr/local/bin/oc   | No        | Path to oc client.                                    |

## Example Playbook

- Remove the non-active UEFI Boot entries in the nodes

```YAML
- name: Clean up non-active UEFI boot entries
  ansible.builtin.include_role:
    name: redhatci.ocp.efi_boot_mgr
  vars:
    ebm_nodes:
      - worker-0
      - worker-1
      - worker-2
    ebm_oc_path: /path/to/my/oc
```
