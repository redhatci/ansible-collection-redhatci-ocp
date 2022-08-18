# OLM-operator role

Role to deploy an OLM-based operator.

## Parameters

Name                        | Required  | Default                | Description
--------------------------- |-----------|------------------------|--------------------------------------
operator                    | Yes       | undefined              | Name of the operator to install
namespace                   | Yes       | undefined              | Namespace where the operator will be installed
channel                     | No        | None                   | The defaultChannel of the operator is used if no channel is defined
source                      | No        | redhat-operators       | CatalogSource where to pull operator from
source_ns                   | No        | openshift-marketplace  | Namespace where the CatalogSource is (default: )
operator_group_spec         | No        | default: {}            | OperatorGroupSpec is the spec for an OperatorGroup resource. e.g. make operator available in all namespaces)
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
