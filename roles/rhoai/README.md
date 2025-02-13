# rhoai

A role to install the Red Hat OpenShift AI operators

## Requirements

This role makes extensive use of the Kubernetes collection, but there are no
other extra requirements

## Role Variables

| Variable                  | Default               | Description   |
|---------------------------|-----------------------|---------------|
| rhoai_action              | install               | Execute the action on role inclusion |
| rhoai_operator_map        | {}                    | Operator/image overrides, read more in-depth description below |
| rhoai_source_catalog      | redhat-operators      | Name of the source catalog providing the subscription, default is the stock catalog |
| rhoai_source_namespace    | openshift-marketplace | Namespace where the source catalog is, default is the stock namespace |
| rhoai_create_dsc          | true                  | Create a DataScienceCluster CRD on `install` action |
| rhoai_dsc_name            | default-dsc           | Name of the DataScienceCluster CRD object to create |
| rhoai_wait_for_dsc        | true                  | Wait for the DSC deployment to finish |

### DataScienceCluster defaults

The DSC cluster default components state is as below.

| Variable                  | Component                 | Status               |
|---------------------------|---------------------------|----------------------|
| rhoai_codeflare           | codeflare                 | Removed              |
| rhoai_kserve              | kserve                    | Managed              |
| rhoai_ray                 | ray                       | Removed              |
| rhoai_kueue               | kueue                     | Removed              |
| rhoai_workbenches         | workbenches               | Managed              |
| rhoai_dashboard           | dashboard                 | Managed              |
| rhoai_modelmeshserving    | modelmeshserving          | Managed              |
| rhoai_datasciencepipeline | datasciencepipelines      | Managed              |

### rhoai_operator_map

The default operator map looks something like this:

```yaml
servicemesh:
  package: servicemeshoperator
  channel: stable
namespace: openshift-operators
serverless:
  package: serverless-operator
  channel: stable-1.32
  namespace: openshift-serverless
rhods:
  package: rhods-operator
  channel: stable-2.8
  namespace: redhat-ods-operator
```

Defined as follows:

* `package` is the packaged operator to install
* `channel` is what channel to pull the package from
* `namespace` is where (what namespace) the operator will be installed

If you want to override any of the keys in the map (e.g. a newer channel for
the ODS operator) you can set the variable like this:

```yaml
rhoai_operator_map:
  rhods:
    channel: stable-2.9
```

## Example Playbook

You can include the role like this:

```yaml
- name: Install DSC in the cluster
  ansible.builtin.include_role:
    name: redhatci.ocp.rhoai
    # In case your kubeconfig is not in the standard location
    # apply:
    #   environment:
    #     KUBECONFIG: /path/to/kubeconfig
    vars:
     rhoai_operator_map:
       rhods:
         channel: stable-2.9  # we want a newer version
     rhoai_dsc_name: my-dsc
     rhoai_kserve: Managed
     rhoai_ray: Removed
     rhoai_kueue: Removed
     # rhoai_source_catalog: offline-operators  # our own copy of the redhat catalogs
     # rhoai_source_namespace: redhat-offline  # previously mirrored to this location
```

## License

Apache License, Version 2.0
