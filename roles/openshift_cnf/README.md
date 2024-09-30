# Automate creation of the Openshift-cnf project for vendor validated

This role will automatically generate an Openshift-cnf certification project when the option `create_cnf_project` is set to `true`. The new role reuses some tasks from the `create_certification_project` role, and the associated templates are stored within this role. Currently, there are no mandatory parameters that need to be updated in the new role.

Please note that the role `openshift_cnf` is currently a basic automation setup. It will undergo further updates once additional options are available by the backend REST API, such as automatic start/continue parameters for starting `Certify the functionality of your CNF on Red Hat OpenShift` step inside the project.

The current backend behavior for attaching a product listing to newly created cert projects requires to include the <old_certs_list> and <new_cert_list>. This is because the product listing ID may have been used in both the old and new projects. To address this, we implemented an enhancement to query all old cert projects based on the product listing ID that was used in both lists. We then merge the results into a single array and attach the product listing ID to to all cert projects.

## Global Variables
As the new role openshift_cnf reuses some existing tasks, please refer to the description in the `create_certification_project` role for information on the shared global variables.


## Variables to define for each cnf_to_certify

Name                     | Default                                                                    | Description
------------------------ | -------------------------------------------------------------------------- | -------------
cnf_name                 | None                                                                       | If defined, it would create Openshift-cnf certification project for vendor validated, cnf_name format: `CNF25.8 + OCP4.12`
pyxis_product_lists      | None                                                                       | Optional. A list of Product Listings; all of them must be created beforehand [See doc](https://redhat-connect.gitbook.io/red-hat-partner-connect-general-guide/managing-your-account/product-listing). It could contain one or many PLs. If set, it will attach all PLs to both old and new certification projects.


## Variables to define for project settings under `cert_settings`

Name                          | Default                              | Description
----------------------------- | ------------------------------------ | -------------
email_address                 | "mail@example.com"                   | String. Email address is needed for creating openshift-cnf project


## Example Configuration of Openshift-cnf certification project creation
```yaml
---
# Generic DCI Pipeline config
- name: create-openshift-cnf
  stage: workload
  topic: OCP-4.16
  ansible_playbook: /usr/share/dci-openshift-app-agent/dci-openshift-app-agent.yml
  ansible_cfg: /var/lib/dci-openshift-app-agent/my-dci-pipeline-test/pipelines/ansible.cfg
  ansible_inventory: /var/lib/dci-openshift-app-agent/my-dci-pipeline-test/inventories/@QUEUE/@RESOURCE-workload.yml
  dci_credentials: /var/lib/dci-openshift-app-agent/.config/dci-pipeline/dci_credentials.yml
  #ansible_skip_tags:
  #  - post-run
  ansible_extravars:
    dci_cache_dir: /var/lib/dci-openshift-app-agent/dci-cache-dir
    dci_config_dir: /var/lib/dci-openshift-app-agent/my-dci-pipeline-test/ocp-workload
    dci_gits_to_components:
      - /var/lib/dci-openshift-app-agent/my-dci-pipeline-test
    dci_local_log_dir: /var/lib/dci-openshift-app-agent/upload-errors
    dci_tags: ["openshift-cnf", "cnf", "debug", "create"]
    dci_workarounds: []

    # custom settings
    check_for_existing_projects: true
    organization_id: 12345678
    page_size: 200

    # Reduce the job duration
    do_must_gather: false
    check_workload_api: false

    # Backend access
    pyxis_apikey_path: "/var/lib/dci-openshift-app-agent/demo-pyxis-apikey.txt"

    cnf_to_certify:
      # Mandatory variables
      - cnf_name: "test-smf23.5 OCP4.16.8"
        create_cnf_project: true
        # Optional, define list of Product Listings
        # if you want to attach PLs to your cert project
        pyxis_product_lists:
          - "xxxxxxxxxxxxxxxxxxxxxxxx"
      - cnf_name: "test-upf23.5 OCP4.16.8"
        create_cnf_project: true

    cert_settings:
      email_address: "email@example.com"

  use_previous_topic: true
  inputs:
    kubeconfig: kubeconfig_path
...
```