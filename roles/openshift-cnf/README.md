# Automate creation of the Openshift-cnf project for vendor validated

This role will automatically generate an Openshift-cnf certification project when the option `create_cnf_project` is set to `true`. The new role reuses some tasks from the `create-certification-project` role, and the associated templates are stored within this role. Currently, there are no mandatory parameters that need to be updated in the new role.

Please note that the role `openshift-cnf` is currently a basic automation setup. It will undergo further updates once additional options are available by the backend REST API, such as automatic start/continue parameters for starting `Certify the functionality of your CNF on Red Hat OpenShift` step inside the project.

## Global Variables
As the new role openshift-cnf reuses some existing tasks, please refer to the description in the `create-certification-project` role for information on the shared global variables.


## Variables to define for each cnf_to_certify

Name                     | Default                                                                    | Description
-------------------      | ------------                                                               | -------------
attach_product_listing   | false                                                                      | If set to true, it would attach product-listing to Openshift-cnf certification project.
create_cnf_project       | false                                                                      | If set to true, it would create a new Openshift-cnf certification project.
cnf_name                 | None                                                                       | If defined, it would create Openshift-cnf certification project for vendor validated, cnf_name format: `CNF25.8 + OCP4.12`


## Variables to define for project settings under `cert_listings` main variable

Name                          | Default                              | Description
----------------------------- | ------------------------------------ | -------------
pyxis_product_list_identifier | None                                 | Product-listing ID, it has to be created before. [See doc](https://redhat-connect.gitbook.io/red-hat-partner-connect-general-guide/managing-your-account/product-listing)
published                     | false                                | Boolean to enable publishing list of products
type                          | "container stack"                    | String. Type of product list
email_address                 | "mail@example.com"                   | String. Email address is needed for creating openshift-cnf project



## Example Configuration of Openshift-cnf certification project creation
```yaml
---
dci_topic: OCP-4.11
dci_name: Testing Openshift-cnf auto creation and attach
dci_configuration: Using DCI create cnf project and attach product-list
check_for_existing_projects: true
ignore_project_creation_errors: true
dci_config_dirs: [/etc/dci-openshift-agent]
partner_creds: "/var/lib/dci-openshift-app-agent/auth.json"
organization_id: 12345678
#cnf_name is a free-text but format: CNF-version + OCP-version e.g "CNF23.5 OCP4.12.9"
cnf_to_certify:
  - cnf_name: "test-smf23.5 OCP4.11.5"
    create_cnf_project: true
    attach_product_listing: true

  - cnf_name: "test-upf23.5 OCP4.11.5"
    create_cnf_project: true
    attach_product_listing: true

cert_listings:
  #email_address is mandatory when creating openshift-cnf for vendor validation but does not hurt to define it
  email_address: "email@example.com"
  published: false
  type: "container stack"
  pyxis_product_list_identifier: "yyyyyyyyyyyyyyyyy" #7GC UDM

pyxis_apikey_path: "/var/lib/dci-openshift-app-agent/pyxis-apikey.txt"
dci_gits_to_components: []
...
```