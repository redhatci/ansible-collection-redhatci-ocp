# Preflight cert suite Role

Preflight is a commandline interface for validating if OpenShift operator bundles and containers meet minimum requirements for Red Hat OpenShift Certification.

This role implements the preflight test suite as part of DCI Application Agent.

## Global Variables

Name                               | Default                                              | Description
---------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
do\_preflight\_tests               | false                                                | Mandatory. Trigger to activate the preflight tests.
preflight\_operators\_to\_certify  | undefined                                            | Mandatory. List of operators to be checked for certification with Preflight Cert Suite. This variable is mandatory to run Preflight cert suite. Please check [example_preflight_config.yaml](#example-of-config-file-to-define-a-list-of-operators-to-certify) for the example.
preflight\_binary                  | https://github.com/redhat-openshift-ecosystem/openshift-preflight/releases/download/1.2.1/preflight-linux-amd64              | Optional. [Version of Preflight Cert Suite to run check container cert suite](https://quay.io/repository/opdev/preflight?tab=tags)
preflight\_image                   | quay.io/opdev/preflight:1.2.1                                  | Optional. [Version of Preflight Cert Suite to run check operator cert suite](https://quay.io/repository/opdev/preflight?tab=tags)
preflight\_namespace               | preflight-testing                                    | Optional. Namespace to use for preflight tests
pyxis\_apikey\_path                | undefined                                            | Optional. This is a path to file that contains partner's token. Parner should generate this token in connect.redhat.com. The token is shared for all projects within one partner.
preflight\_custom\_ca              | undefined                                            | Optional. Path of custom ca.crt. Used to test operator stored in a self signed registry
preflight\_source\_dir             | undefined                                            | Optional. If this variable is defined, the Preflight role would use this folder to generate preflight image and binary and then use them during Preflight tests execution. That would overwrite predefined preflight_image and preflight_binary (if any).
operator\_sdk\_tool\_path          | undefined                                            | Optional. Path to operator-sdk binary, optional. Please check [example_preflight_config.yaml](#example-of-config-file-to-define-a-list-of-operators-to-certify) for the example.

## Variables to define for each operator in preflight_operators_to_certify

Name                               | Default                                              | Description
---------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
bundle\_image                      | undefined                                            | Mandatory. In the connected environment, the image could be provided by tag. In the disconnected, you have to provide the image by digest.
index\_image                       | undefined                                            | Optional for connected environments and mandatory for disconnected.
pyxis\_container\_identifier       | undefined                                            | Optional. To get this identifier, please create a project of type "Container Image project" at connect.redhat.com. Set this project identifier to submit Preflight `check container` results to Pyxis and connect.redhat.com. This identifier is unique for each container. If you have to certify multiple containers please create multiple projects. Please do not forget to provide Pyxis credentials: pyxis\_apikey\_path with Pyxis token (shared for all projects within one client).
pyxis\_operator\_identifier        | undefined                                            | Optional. This variable should be defined for each operator. To get this identifier, please create a project of type "Operator Bundle Image project" at connect.redhat.com. Set this project identifier to submit Preflight `check operator` results to Pyxis and connect.redhat.com. This identifier is unique for each operator. If you have to certify multiple operators please create multiple projects. Please do not forget to provide Pyxis credentials: pyxis\_apikey\_path with Pyxis token (shared for all projects within one client).


## How to run preflight cert suite

- Export kubeconfig:

  ```sh
  export KUBECONFIG=/var/lib/dci-openshift-app-agent/kubeconfig
  ```

- Create file settings.yml in /etc/dci-openshift-app-agent/settings.yml and provide all the information about your certification projects. Let’s consider two standard scenarios here.

  a. If you have a connected environment with the private external registry.

  ```yaml
  $ cat /etc/dci-openshift-app-agent/settings.yml
  ---
  # Job name and tags to be displayed in DCI UI
  dci_name: "Testpmd-Operator-Preflight"
  dci_tags: ["debug", "testpmd-operator"]

  do_preflight_tests: true

  # Optional, please provide these credentials
  # if your registry is private.
  partner_creds: "/opt/pull-secrets/partner_config.json"

  # List of operators to certify,
  # you could provide many operators at once.
  preflight_operators_to_certify:
    - bundle_image: "quay.io/rh-nfv-int/testpmd-operator-bundle:v0.2.9"
      # Mandatory for the connected environments.
      index_image: "quay.io/rh-nfv-int/nfv-example-cnf-catalog:v0.2.9"
      # Optional; provide it when you need to submit test results.
      # It's an id of your Container Image Project
      # https://connect.redhat.com/projects/my_nice_container_id
      pyxis_container_identifier: "my_nice_container_id"

  # Optional; provide it when you need to submit test results.
  # This token is shared between all your projects.
  # To generate it: connect.redhat.com -> Product certification ->
  # Container API Keys -> Generate new key
  pyxis_apikey_path: "/opt/cache/pyxis-apikey.txt"
  ```

  b. There is a disconnected environment with the self-signed local registry and operator images in the external private registry. In the case of a disconnected environment, DCI would handle all the mirroring and regenerate a catalog image.

  ```yaml
  $ cat /etc/dci-openshift-app-agent/settings.yml
  ---
  # job name and tags to be displayed in DCI UI
  dci_name: "Testpmd-Operator-Preflight"
  dci_tags: ["debug", "testpmd-operator"]

  do_preflight_tests: true
  # Mandatory for disconnected environment,
  # this registry is used for mirrored images
  # and to store an index (catalog) image.
  provisionhost_registry: registry.local.lab:4443
  # Credentials for your private registries.
  # You could have several private registries:
  # local and another external, to store the operator.
  # In this case, please provide all credentials here.
  partner_creds: "/opt/pull-secrets/partner_config.json"

  # List of operators to certify,
  # you could provide many operators at once.
  preflight_operators_to_certify:
      # In disconnected environments provide a digest (SHA) and not a tag.
    - bundle_image: "quay.io/rh-nfv-int/testpmd-operator-bundle@sha256:5e28f883faacefa847104ebba1a1a22ee897b7576f0af6b8253c68b5c8f42815"
      # Optional, provide it when you need to submit test results.
      # It's an id of your Container Image Project
      # https://connect.redhat.com/projects/my_nice_container_id
      pyxis_container_identifier: "my_nice_container_id"

  # Optional; provide it when you need to submit test results.
  # This token is shared between all your projects.
  # To generate it: connect.redhat.com -> Product certification ->
  # Container API Keys -> Generate new key
  pyxis_apikey_path: "/opt/cache/pyxis-apikey.txt"
  # Optional, provide it if your registry is self-signed.
  preflight_custom_ca: "/var/lib/dci-openshift-agent/registry/certs/cert.ca"
  ```

- Run dci-openshift-app-agent:
  ```sh
  dci-openshift-app-agent-ctl -s -- -v
  ```


## Preflight CI

If the variable `preflight_source_dir` is defined, the Preflight role would use this folder to generate preflight image and binary and then use them during Preflight tests execution. That would overwrite predefined preflight_image and preflight_binary (if any).

Currently, Preflight CI stores the generated preflight image into a `provisionhost_registry` and hence would only work in disconnected environments with a registry attached. The plan is to remove this limitation in the next releases.
