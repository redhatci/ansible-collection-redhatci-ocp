# Automate creation of the certification projects

This role automatically creates the missing certification projects if `create_cert_projects: true`.
If the project already exists and its identifier `pyxis_container_identifier` is provided, then the new project will not be created. For the moment, it's implemented only for the container certification.

## Variables

Name                     | Default                                                                    | Description
-------------------      | ------------                                                               | -------------
create\_cert\_projects   | false                                                                      | If set to true, it would create missing certification projects.
connect\_url             | https://connect.redhat.com/projects                                        | Certification UI link
create\_project\_url     | https://catalog.redhat.com/api/containers/v1/projects/certification        | Pyxis API to create certification project

## Example of configuration file

```yaml
# config example
$ cat /etc/dci-openshift-app-agent/settings.yml
---
# Job name and tags to be displayed in DCI UI
dci_name: "Containers-Preflight"
dci_tags: ["debug", "standalone-containers"]

# Optional, please provide these credentials
# if your registry is private.
partner_creds: "/opt/pull-secrets/partner_config.json"

# The missing cert projects will be automatically created
# for the containers with missing pyxis_container_identifier parameter.
# The new project will be created for noc-noc container and
# will not be created for bla-bla container.
create_cert_projects: true

# List of images to certify,
# you could provide many containers at once.
preflight_containers_to_certify:
  - container_image: "quay.io/rh-nfv-int/bla-bla:v0.2.9"
    # Optional; provide it when you need to submit test results.
    # It's an id of your Container Image Project
    # https://connect.redhat.com/projects/my_nice_container_id
    pyxis_container_identifier: "my_nice_container_id"
  - container_image: "quay.io/rh-nfv-int/noc-noc:v0.2.9"

# Optional; provide it when you need to submit test results.
# This token is shared between all your projects.
# To generate it: connect.redhat.com -> Product certification ->
# Container API Keys -> Generate new key
pyxis_apikey_path: "/opt/cache/pyxis-apikey.txt"
```
