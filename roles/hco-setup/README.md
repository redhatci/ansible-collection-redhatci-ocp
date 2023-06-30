# hco-setup role

A role that deploys and configures the `hco-operator` through the `kubevirt-hyperconverged` CRs.
This role also deploys a test VM to ensure its functionality.

## Variables

| Variable                | Default                                             | Required | Description                                     |
| ----------------------- | --------------------------------------------------- | -------- | ----------------------------------------------- |
| hs_deploy               | true                                                | No       | Deploy the hco-operator                         |
| hs_test_vm              | false                                               | No       | Perform a VM test to validate the operator      |
| hs_ns                   | openshift-cnv                                       | No       | Namespace where to install the operator         |
| hs_vm_file              | vm.yaml.j2                                          | No       | A template used for the creation of the test VM |
| hs_test_vm_image        | quay.io/kubevirt/cirros-container-disk-demo:v0.59.2 | No       | The image used in the test VM                   |
| hs_retries              | 60                                                  | No       | The number of retries to validate a VM is ready |
| hs_kubevirt_api_version | v1                                                  | No       | The API version for kubevirt CRs                |
| hs_pullsecret_file      | None                                                | Yes*     | The pull-secret file to the local registry      |
| hs_registry             | None                                                | Yes*     | The local registry to mirror the VM             |

*Required for disconnected environments

## Role requirements

This operator requires the CNV operator `kubevirt-hyperconverged` already installed in the cluster.

## Examples

As a role:

```yaml
- hosts: localhost
  roles:
     - role: hco-setup
```

As a task:

```yaml
- name: "Deploy hco-operator and test it"
  include_role:
    name: hco-setup
  vars:
    hs_test_vm: true
    hs_test_vm_image: quay.io/kubevirt/fedora-with-test-tooling-container-disk:v0.59.2
    hs_pullsecret_file: /path/to/pull-secret.json
    hs_registry: my.registry.example.com
```

# References

* [OpenShift Virtualization installation, usage, and release notes](https://access.redhat.com/documentation/en-us/openshift_container_platform/4.13/html-single/virtualization/index)
* [dci-openshfit-agent](https://github.com/redhat-cip/dci-openshift-agent/): An agent that allows the deployment of OCP clusters, it is integrated with DCI (Red Hat Distributed CI).
