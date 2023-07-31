# Automate creation, update and attach of the Helm Chart Certification Project

This new role `create-helmchart` leverages some existing tasks from the create-certification-project role, promoting reusability and avoiding duplication of effort. Additionally, it introduces new tasks, such as check_if_helmchart_project_exists_same_org and update_helmchart_project, to accomplish specific requirements related to Helm Chart certification.

The associated templates, like create_project_helmchart.json.j2, update_project_helmchart_setting.json.j2 and attach_product_helmchart_listing.json.j2, are now stored within the create-certification-project role instead of being duplicated in the new role create-helmchart. This design ensures efficiency, maintainability, and consistency across the roles.


## Global Variables
As the new role `create-helmchart` reuses some existing tasks such as check_for_existing_projects, create_project and attach_product_listing. Please refer to the description in the `create-certification-project` role for information on the shared global variables.


## Variables to define under cert_settings for Helm Chart
Name                     | Default                                                                    | Description
-------------------      | ------------                                                               | -------------
distribution_method      | None                                                                       | Define when creating new Helm Chart and recommended to define the value as `undistributed` (Web catalog only) and for second value `external` (charts.openshift.io)
github_usernames         | None                                                                       | Define the Github user
long_description         | None                                                                       | Same as describe in other project, it means to describe what general information about these CNFs if there are more than one chart
distribution_instructions| None                                                                       | Define when creating new Helm Chart and provide the information how the user can get this Helm Chart

Note: Some variables are not mentioned since they are same as explained in `create-certification-project` role.


## Variables to define for each helmchart_to_certify

Name                     | Default                                                                    | Description
-------------------      | ------------                                                               | -------------
attach_product_listing   | false                                                                      | If set to true, it would attach product-listing to Helm Chart certification project.
create_helmchart_project | false                                                                      | If set to true, it would create a new Helm Chart certification project.
chart_name               | None                                                                       | If defined, it would create Helm Chart certification project, chart_name will be used as project and chart name
repository               | None                                                                       | If defined, it will be used for chart_name, the value for this `repository` variable can be dummy but please give more meaningful as chart_name
short_description        | None                                                                       | Define when create new Helm Chart and values of this variable is to describe specific detail about this chart


## Variables to define for project settings under `cert_listings` main variable

Name                          | Default                              | Description
----------------------------- | ------------------------------------ | -------------
pyxis_product_list_identifier | None                                 | Product-listing ID, it has to be created before. [See doc](https://redhat-connect.gitbook.io/red-hat-partner-connect-general-guide/managing-your-account/product-listing)
published                     | false                                | Boolean to enable publishing list of products
type                          | "container stack"                    | String. Type of product list


## Example Configuration of Helm Chart certification project creation
```yaml
---
dci_topic: OCP-4.11
dci_name: Automatic to create,update and attach certification Project for Helm Chart with DCI
dci_configuration: Use DCI to Automate Helm Chart Project Creation
check_for_existing_projects: true
ignore_project_creation_errors: true
dci_config_dirs: [/etc/dci-openshift-agent]
organization_id: 12345678
do_must_gather: false
page_size: 300
helmchart_to_certify:
  - repository: "https://github.com/xxxx/demochart1"
    short_description: "This is a short description demochart1"
    chart_name: "demochart1"
    create_helmchart_project: true
    attach_product_listing: true
  - repository: "https://github.com/xxxx/demochart2"
    short_description: "This is a short description demochart2"
    chart_name: "demochart2"
    create_helmchart_project: true
    attach_product_listing: true

cert_settings:
   email_address: "mail@example.com"
   distribution_method: "undistributed" #undistributed==>Web catalog only, external==> charts.openshift.io
   github_usernames: "xusername"
   application_categories: "Networking"
   long_description: "This is a long description about this sample chart"
   application_categories: "Networking"
   distribution_instructions: "Instruction how to get this helm-chart"

cert_listings:
  published: false
  type: "container stack"
  pyxis_product_list_identifier: "yyyyyyyyyyyyyyy"  # product list id for helmchart projects

pyxis_apikey_path: "/var/lib/dci-openshift-app-agent/demo-pyxis-apikey.txt"
dci_gits_to_components: []
...
```