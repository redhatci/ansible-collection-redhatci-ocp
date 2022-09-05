# Automate creation of the certification projects

This role automatically creates a container certification project if option `create_container_project: true` is provided, and operator certification project if `create_operator_project: true`.

## Variables

Name                     | Default                                                                    | Description
-------------------      | ------------                                                               | -------------
create_container_project | false                                                                      | If set to true, it would create new container certification project
create_operator_project  | false                                                                      | If set to true, it would create new operator certification project
connect_url              | https://connect.redhat.com/projects                                        | Certification UI link
create_project_url       | https://catalog.redhat.com/api/containers/v1/projects/certification            | Pyxis API to create certification project
github_token_path        | undefined            | Path to GitHub token to be used for the operator certification project

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

# Optional; provide it when you need to submit test results.
# This token is shared between all your projects.
# To generate it: connect.redhat.com -> Product certification ->
# Container API Keys -> Generate new key
pyxis_apikey_path: "/opt/cache/pyxis-apikey.txt"

# Optional; provide this token when using create_pr option
github_token_path: "/opt/cache/dcicertbot-token.txt"
```

## GitHub token

Please note that github_token_path is required when using create_operator_project project. It is used to setup proper permissions in the certification project.

Here are the required token permissions.

![pic](files/github_token.png)
