# generate_agent_iso

Creates the boot ISO using openshift_installer's agent sub-command

## Role Variables

Name                           | Type   | Required | Default                                          | Description
------------------------------ | ------ | -------- | ------------------------------------------------ | ------------
gai_cluster_name               | string | yes      | -                                                | Cluster name, typically defined in the inventory file.
gai_repo_root_path             | string | yes      | -                                                | Root path to place all files and folders required to build the agent ISO.
gai_pull_secret                | string | yes      | -                                                | Pull secret to download images required to build the agent ISO.
gai_agent_based_installer_path | string | yes      | -                                                | Path to find `openshift-install` binary
gai_discovery_iso_name         | string | yes      | -                                                | Relateive path to discovery ISO name, typically defined in ABI inventories.
gai_path_var                   | string | no       | "/sbin:/usr/sbin:/usr/local/bin/"                | String to append to `PATH` environment variable when creating the agent ISO.
gai_generated_dir              | string | no       | "{{ gai_repo_root_path }}/generated"             | Directory to place pull secret, using it afterwards as value for `XDG_RUNTIME_DIR` environment variable when creating the agent ISO.
gai_manifests_dir              | string | no       | "{{ gai_generated_dir }}/{{ gai_cluster_name }}" | Directory to save the manifests that are lately used to save the generated ISO.
gai_iso_download_dest_path     | string | no       | "/opt/http_store/data"                           | Root directory to eventually save the generated agent ISO.
gai_arch                       | string | no       | "x86_64"                                         | Cluster architecture.

## Example

You can call this role in the following way, as an example of usage:

```yaml
- name: Generate agent ISO
  vars:
    gai_cluster_name: "my-cluster"
    gai_repo_root_path: "/path/to/root_path"
    gai_pull_secret: "/path/to/pull_secret"
    gai_agent_based_installer_path: "/path/to/openshift-install"
    gai_discovery_iso_name: "relative/path/to/discovery.iso"
  ansible.builtin.include_role:
    name: redhatci.ocp.generate_agent_iso
```
