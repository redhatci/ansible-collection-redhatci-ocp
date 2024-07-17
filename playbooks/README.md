# RedHat CI OCP collection Playbooks

This directory contains playbooks for common use cases of the OpenShift Container Platform (OCP) collection's roles. These are aim to be use as references cases where the [DCI Openshift Agent](https://github.com/redhat-cip/dci-openshift-agent) may no be available.

# Requirements

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
