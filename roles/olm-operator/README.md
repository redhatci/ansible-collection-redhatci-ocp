# OLM-operator role

Role to deploy an OLM-based operator.

## Parameters

Name                        | Required  | Default                | Description
--------------------------- |-----------|------------------------|--------------------------------------
operator                    | Yes       | undefined              | Name of the operator to install
namespace                   | Yes       | undefined              | Namespace where the operator will be installed
source                      | No        | redhat-operators       | CatalogSource where to pull operator from
source\_ns                   | No        | openshift-marketplace  | Namespace where the CatalogSource is (default: )
operator\_group\_spec         | No        | default: {}            | OperatorGroupSpec is the spec for an OperatorGroup resource. i.e make operator available in all namespaces)
install\_approval            | No        | Manual                 | Operator install plan approval mode, either Automatic or Manual (default)

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
