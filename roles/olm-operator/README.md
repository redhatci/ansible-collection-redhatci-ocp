# OLM-operator role

Role to deploy an OLM-based operator.

## Parameters

Name                        | Required  | Default                | Description
--------------------------- |-----------|------------------------|--------------------------------------
operator                    | Yes       | undefined              | Name of the operator to install
namespace                   | Yes       | undefined              | Namespace where the operator will be installed
ns_labels                   | No        | {}                     | Dictionary of labels (name: value) to be assigned to the operator namespace
channel                     | No        | \<defaultChannel\>     | The default channel of the operator is calculated and used when undefined
source                      | No        | redhat-operators       | CatalogSource where to pull operator from
source_ns                   | No        | openshift-marketplace  | Namespace where the CatalogSource is (default: )
operator_group_name         | No        | {{ operator }}         | Name to be given to the operator group. If none is defined, the operator name will be used.
operator_group_spec         | No        | {}                     | OperatorGroupSpec is the spec for an OperatorGroup resource. e.g. make operator available in all namespaces)
install_approval            | No        | Manual                 | Operator install plan approval mode, either Automatic or Manual (default)

## Example of usage

```yaml
- name: "deploy-operators : Install OCS Operator"
  include_role:
    name: olm-operator
  vars:
    operator: ocs-operator
    source: "{{ opm_catalog_source_name }}"
    namespace: redhat-operators
    ns_labels:
      openshift.io/cluster-monitoring: "true"
    operator_group_spec:
      targetNamespaces:
        - openshift-storage
```
