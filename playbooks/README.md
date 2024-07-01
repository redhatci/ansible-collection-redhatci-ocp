# RedHat CI OCP collection Playbooks

This directory contains playbooks for common use cases of the OpenShift Container Platform (OCP) collection's roles. These are aim to be use as references cases where the [DCI Openshift Agent](https://github.com/redhat-cip/dci-openshift-agent) may no be available.

# Requirements

The Ansible collection must be installed either using an RPM package or via Ansible Galaxy. It is required that the ansible.cfg file has an entry pointing to the OpenShift Container Platform (OCP) roles location. For example:

Installation using galaxy
```ShellSession
$ ansible-galaxy collection install redhatci.ocp
```

Example of playbook's `ansible.cfg` file.
```ShellSession
$ cat ansible.cfg
[defaults]
<trimmed>
collections_path    = /home/<user>/.ansible/collections/ansible_collections:/home/<user>/<my_dir>/git/ansible_collections
roles_path          = /usr/share/dci/roles/:/var/lib/dci-openshift-agent/assisted_deploy_repo/roles/
<trimmed>
```

Most of the playbooks interact with an OCP cluster via its `KUBECONFIG`, so please set the `KUBECONFIG` environment variable to point to a file containing a valid kubeconfig.

```ShellSession
$ export KUBECONFIG=/home/<user>/kubeconfig
$ ansible-playbook <playbook-file> <options>
```

Some roles may have dependencies script distributed as part or `dci-openshift-agent`, so it is recommended to have the RPM installed.

See the corresponding README and variables defined in de playbook for additional information.

## Playbook list

| Playbook                                                                  | Description
|-------------------------------------------------------------------------- | ---------------------------
| [Multibench Setup Host](multibench_setup_host/multibench_setup_host.yml)  |  Installs the crucible binaries needed for the execution of the Multi-bench role. See [Readme](multibench_setup_host/README.md)
| [Prune and Mirror Operators](prune_mirror.yml)                            |  Prunes and mirror operators to a local registry
| [Mirror OCP](mirror_ocp.yml)                                              |  Mirror and OCP release
| [Install Operators](install_operators.yml)                                |  Creates a catalog source and install and operator