# OPCAP tool role

OPCAP is a tool to test the installation of the Openshift operators.
Here is the official [Github repository](https://github.com/opdev/opcap) of the tool for more details.

This role clones the official repository, builds the tool and launches checks on a catalog operator.
It generates a JSON file with the results of the checks, and it also displays all the packages available in the catalog
in the Ansible playbook.
Binary is copied in the output_dir at the end of the test in case of debugging.

## Usage

| Name                           | Required | Default                          | Description                                                                                                                                 |
|--------------------------------|----------|----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| opcap_target_catalog_source    | true     | None                             | Name of the catalogSource that will be checked                                                                                              |
| opcap_catalog_source_namespace | true     | None                             | Namespace where is deployed the catalogSource tested                                                                                        |
| opcap_output_dir               | true     | None                             | Directory where the results of the checks are copied                                                                                        |
| opcap_packages                 | false    | None                             |  List of package(s) which limits audits and/or other flag(s) output, CSV format
| opcap_version                  | false    | 0.2.1                            | Version that will be displayed when the binary is running                                                                                   |
| opcap_repo                     | false    | https://github.com/opdev/opcap   | Repository used to clone and build the tool                                                                                                 |
| opcap_audit_plan               | false    | "OperatorInstall,OperandInstall" | In order to test operands, the audit plan can be modified. Possible values: "OperatorInstall,OperandInstall,OperandCleanUp,OperatorCleanUp" |

### Example

KUBECONFIG must be defined as a ENV variable in order to have opcap bin working properly:

    - name: Run opcap checks on my-catalog
      ansible.builtin.include_role:
        name: redhatci.ocp.opcap_tool
        apply:
          environment:
            KUBECONFIG: "{{ kubeconfig_path }}"
      vars:
        opcap_target_catalog_source: "my-catalog"
        opcap_catalog_source_namespace: "openshift-marketplace"
        opcap_output_dir: "{{ job_logs.path }}"
        opcap_package: "my-package1,my-package2"
