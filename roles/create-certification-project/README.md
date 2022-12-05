# Automate creation of the certification projects

This role automatically creates a container certification project if option `create_container_project: true` is provided, and operator certification project if `create_operator_project: true`.

## Global Variables

Name                     | Default                                                                    | Description
-------------------      | ------------                                                               | -------------
connect_url              | https://connect.redhat.com/projects                                        | Mandatory; usually there is no need in redefining it. Certification UI link, you may need to change it to target UAT environment for the testing.
create_project_url       | https://catalog.redhat.com/api/containers/v1/projects/certification        | Mandatory; usually there is no need in redefining it.Pyxis API to create certification project, you may need to change it to target UAT environment for the testing.
github_token_path        | undefined                                                                  | Mandatory when using `create_operator_project`. Path to GitHub token to be used for the operator certification project.


## Variables to define for each operator / container

Name                     | Default                                                                    | Description
-------------------      | ------------                                                               | -------------
create_container_project | false                                                                      | If set to true, it would create a new container certification project.
create_operator_project  | false                                                                      | If set to true, it would create a new operator certification project.


## Variables to define for project settings under `cert_settings` main variable (Optional)

Below an example of variables used for container image certification project, more variables are available depending is created for operator or helmchart certifications. All sub-variables are optional.
For more details see full [API schema](https://catalog.redhat.com/api/containers/v1/ui/#/Certification%20projects/pyxis.rest.legacy.cert_projects.patch_certification_project)

Name                       | Default                              | Description
-------------------        | ------------------------------------ | -------------
auto_publish               | false                                | false or true: boolean to enable auto publish
build_categories           | "Standalone image"                   | Image type, choose between "Standalone image", "Operator image" or "Component image".
registry_override_instruct | "Add override instructions"          | (String) Additional instructions to get image.
email_address              | None                                 | Maintainer email addresses separated by a comma.
application_categories     | "Networking"                         | (String) Up to three categories related to the function of the image/operator. Examples: "Networking", "Storage", "Security".
os_content_type            | "Red Hat Universal Base Image (UBI)" | Base OS running in the image. Either "Red Hat Enterprise Linux" for RHEL or "Red Hat Universal Base Image (UBI)" for UBI.
privileged                 | true                                 | false or true: false when the container is isolated from the host, and true when the container requires special Host level privileges.
release_category           | "Generally Available"                | Whether the resource to certify is either GA or Beta, choose between: "Generally Available" or "Beta".
repository_description     | "Add a description of project here"  | This will be displayed on the container catalog repository overview page.
organization_id            | None                                 | This is required if you use cert_settings, [Company ID](https://redhat-connect.gitbook.io/partner-guide-for-red-hat-openshift-and-container/appendix/connect-portal-api/project-creation#company-id)


## Variables to define for project settings under `cert_listings` main variable (Optional)

Name                          | Default                              | Description
----------------------------- | ------------------------------------ | -------------
pyxis_product_list_identifier | None                                 | Product-listing ID, it has to be created before [See doc](https://redhat-connect.gitbook.io/red-hat-partner-connect-general-guide/managing-your-account/product-listing)
published                     | false                                | Boolean to enable publishing list of products
type                          | "container stack"                    | String. Type of product list


## Example of configuration file

```yaml
$ cat /etc/dci-openshift-app-agent/settings.yml
---
# job name and tags to be displayed in DCI UI
dci_name: "Testpmd-Operator-Preflight"
dci_tags: ["debug", "testpmd-operator", "testpmd-container"]
dci_topic: "OCP-4.7"
# DCI component for every OCP version
# could be checked here: https://www.distributed-ci.io/topics
dci_component: ['8cef32d9-bb90-465f-9b42-8b058878780a']

# Optional, please provide these credentials
# if your registry is private.
partner_creds: "/opt/pull-secrets/partner_config.json"

# List of operators to certify,
# you could provide many operators at once.
preflight_operators_to_certify:
  - bundle_image: "quay.io/rh-nfv-int/bla-bla-bundle:v0.2.1"
    # Mandatory for the connected environments.
    index_image: "quay.io/rh-nfv-int/bla-bla-catalog:v0.2.1"
    # Optional; provide it when you need to create
    # a new "Container Image project" and submit test results in it.
    create_container_project: true
    # Optional; provide it when you need to create
    # a new "Operator Bundle Image" and submit test results in it.
    create_operator_project: true
    # Optional; use it to automatically open cert PR
    # at the certified-operators repository
    create_pr: true

# List of container images to certify,
# you could provide multiple images to certify at once.
preflight_containers_to_certify:
  - container_image: "quay.io/my-container/bla-bla-image:v0.0.1"
    create_container_project: true
    # Optional; use it to pass an image description to the created project
    short_description: "Add description here"

# Project certification setting (Optional)
# This allows to fill the rest of the project settings after project creation
# Any project for containers images or operators certifications can use them
cert_settings:
   build_categories: "Standalone image"
   registry_override_instruct: "This are instructions of how to override settings"
   email_address: "email@example.com"
   application_categories: "Networking"
   os_content_type: "Red Hat Universal Base Image (UBI)"
   privileged: false
   release_category: "Generally Available"
   repository_description: "This is a test repo"
   organization_id: 12345678

# Project certification list setting (Optional)
cert_listings:
  published: false
  type: "container stack"
  pyxis_product_list_identifier: "yyyyyyyyyyyyyyyyy"

# Optional; provide it when you need to submit test results.
# This token is shared between all your projects.
# To generate it: connect.redhat.com -> Product certification ->
# Container API Keys -> Generate new key
pyxis_apikey_path: "/opt/cache/pyxis-apikey.txt"

# Optional; provide this token when using create_pr option
github_token_path: "/opt/cache/dcicertbot-token.txt"
```

## GitHub token

Please note that `github_token_path` is required when using `create_operator_project` project. It is used to setup proper permissions in the certification project.

Here are the required token permissions.

![pic](files/github_token.png)
