# Ansible Role: Generate MicroShift ISO

This Ansible role automates the process of generating a MicroShift ISO image.

## Requirements

- Red Hat Subscription Manager (RHSM) for registering the host.
- OCP pull secret for MicroShift

## Role Variables

The role requires the following variables to be defined:

- `microshift_generate_iso_microshift_repo_url`: The location of the Microshift repo.
- `microshift_generate_iso_rhocp_repo_url`: The location of the GA RHOCP repo.
- `microshift_generate_iso_microshift_version`: The version of Microshift to use.

- `microshift_generate_iso_localhost_folder`: The directory on the localhost where the ISO will be saved. Default is `"/tmp"`.
- `microshift_generate_iso_microshift_iso_name`: Name of the iso in {{ microshift_generate_iso_localhost_folder }}. Default "/tmp".
- `microshift_generate_iso_fast_datapath_repo_url`: Fast data path repo url. Default is `"https://cdn.redhat.com/content/dist/layered/rhel{{ ansible_distribution_major_version }}/{{ ansible_architecture }}/fast-datapath/os"`
- `microshift_generate_iso_action`: Specifies the action to perform. Default is `"install"`.
- `microshift_generate_iso_folder`: The directory where MicroShift files will be stored. Default is `"/home/{{ ansible_user }}/microshift"`.
- `microshift_generate_iso_folder_blueprints_dir`: The directory within `microshift_generate_iso_folder` where blueprints will be stored. Default is `"{{ microshift_generate_iso_folder }}/blueprints"`.
- `microshift_generate_iso_ssh_key`: The SSH public key to use for accessing servers. Default is the content of `~/.ssh/id_rsa.pub`.

## Example Playbook

```yaml
- hosts: microshift_build_server
  roles:
    - role: microshift_generate_iso
