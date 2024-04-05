# Automate creation, update and attach of the Helm Chart Certification Project

This new role `create_helmchart` leverages some existing tasks from the create_certification_project role, promoting reusability and avoiding duplication of effort. Additionally, it introduces new tasks, such as check_if_helmchart_project_exists_same_org and update_helmchart_project, to accomplish specific requirements related to Helm Chart certification.

The associated templates, like create_project_helmchart.json.j2, update_project_helmchart_setting.json.j2 and attach_product_helmchart_listing.json.j2, are now stored within the create_certification_project role instead of being duplicated in the new role create_helmchart. This design ensures efficiency, maintainability, and consistency across the roles.

The current backend behavior for attaching a product listing to newly created cert projects requires that the <old_certs_list> and <new_cert_list> be included. This is because the product listing ID may have been used in both the old and new projects. To address this, we implemented an enhancement to query all old cert projects based on the product listing ID that was used in both lists. We then merged the results into a single array and attached the product listing ID to all of the cert projects.

## Global Variables
As the new role `create_helmchart` reuses some existing tasks such as check_for_existing_projects, create_project and attach_product_listings. Please refer to the description in the `create_certification_project` role for information on the shared global variables.


## Variables to define under cert_settings for Helm Chart
Name                     | Default                                                                    | Description
-------------------      | ------------                                                               | -------------
distribution_method      | None                                                                       | Define when creating new Helm Chart and recommended to define the value as `undistributed` (Web catalog only) and for second value `external` (charts.openshift.io)
github_usernames         | None                                                                       | Define the GitHub user
long_description         | None                                                                       | Same as describe in other project, it means to describe what general information about these CNFs if there are more than one chart
distribution_instructions| None                                                                       | Define when creating new Helm Chart and provide the information how the user can get this Helm Chart

Note: Some variables are not mentioned since they are same as explained in `create_certification_project` role.


## Variables to define for each helmchart_to_certify

Name                     | Default                                                                    | Description
-------------------      | ------------                                                               | -------------
chart_name               | None                                                                       | If defined, it would create Helm Chart certification project, chart_name will be used as project and chart name
repository               | None                                                                       | If defined, it will be used for chart_name, the value for this `repository` variable can be dummy but please give more meaningful as chart_name
short_description        | None                                                                       | Define when create new Helm Chart and values of this variable is to describe specific detail about this chart
pyxis_product_lists       | None                                                                      | Optional. A list of Product Listings; all of them must be created beforehand [See doc](https://redhat-connect.gitbook.io/red-hat-partner-connect-general-guide/managing-your-account/product-listing). It could contain one or many PLs. If set, it will attach all PLs to both old and new certification projects.


## Example Configuration of Helm Chart certification project creation
```yaml
---
# Generic DCI config
dci_topic: OCP-4.15
dci_name: Automatic to create,update and attach certification Project for Helm Chart with DCI
dci_configuration: Use DCI to Automate Helm Chart Project Creation
dci_config_dirs: [/etc/dci-openshift-agent]
dci_gits_to_components: []

# Certification-related config
pyxis_apikey_path: "/var/lib/dci-openshift-app-agent/demo-pyxis-apikey.txt"
organization_id: 12345678

helmchart_to_certify:
  # Mandatory variables
  - repository: "https://github.com/xxxx/demochart1"
    chart_name: "demochart1"
    short_description: "This is a short description demochart1"
    # Optional, define list of Product Listings
    # if you want to attach PLs to your cert project
    pyxis_product_lists:
      - "xxxxxxxxxxxxxxxxxxxxxxxx"
      - "yyyyyyyyyyyyyyyyyyyyyyyy"
  - repository: "https://github.com/xxxx/demochart2"
    chart_name: "demochart2"
    short_description: "This is a short 50+ characters description demochart2"

cert_settings:
  email_address: "mail@example.com"
  distribution_method: "undistributed" #undistributed==>Web catalog only, external==> charts.openshift.io
  github_usernames: "xusername"
  application_categories: "Networking"
  long_description: "This is a long 100+ characters description about this sample chart"
  application_categories: "Networking"
  distribution_instructions: "Instruction how to get this helm-chart"
...
```
