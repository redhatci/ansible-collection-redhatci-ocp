# Preflight cert suite Role

Preflight is a command-line interface for validating if OpenShift operator bundles and containers meet minimum requirements for Red Hat OpenShift Certification.

This role implements the preflight test suite as part of DCI Application Agent.

## Global Variables

Name                               | Default                                              | Description
---------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
preflight_operators_to_certify  | undefined                                            | Mandatory for end-to-end operator certification. List of operators to be checked for certification with Preflight Cert Suite. Please check [example_preflight_config.yaml](#operator-end-to-end-certification) for the example.
preflight_containers_to_certify  | undefined                                            | Mandatory for standalone container certification. List of containers to be checked for certification with Preflight Cert Suite. Please check [example_preflight_config.yaml](#certification-of-standalone-containers) for the example.
preflight_image                   | quay.io/opdev/preflight:1.9.6                                 | Optional. [Version of Preflight Cert Suite to run check operator cert suite](https://quay.io/repository/opdev/preflight?tab=tags)
preflight_namespace               | preflight-testing                                    | Optional. Namespace to use for preflight tests
preflight_sa                      | default                                             | Optional. Service account to use for preflight tests
pyxis_apikey_path                | undefined                                            | Optional. This is a path to file that contains partner's token. Partner should generate this token in connect.redhat.com. The token is shared for all projects within one partner.
preflight_custom_ca              | undefined                                            | Optional. Path of custom ca.crt. Used to test operator stored in a self signed registry
preflight_source_dir             | undefined                                            | Optional. If this variable is defined, the Preflight role would use this folder to generate preflight image and binary and then use them during Preflight tests execution. That would overwrite predefined preflight_image if any.
preflight_test_certified_image  | false                                                | Optional. Run preflight tests on already certified images.
catalog_url                       | https://catalog.redhat.com/api/containers/v1         | Optional. This is a Pyxis API that used during the check if the image is certified.
preflight_run_health_check      | true                                                 | Optional. Run health check on every container and generate oval reports both in xml and HTML formats.
preflight_dci_all_components_are_ga | true                                             | Optional. Only submit test results when all components in the list `dci_ga_components_for_certification` are GA.
max_images_per_batch | 1                                             | Optional. This variable allows the user to adjust the number of images processed per batch for running preflight in parallel. By default, it is set to `1`.


## Variables to define for each operator in preflight_operators_to_certify

Name                               | Default                                              | Description
---------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
bundle_image                       | undefined                                            | Mandatory. In the connected environment, the image could be provided by tag. In the disconnected, you have to provide the image by digest.
index_image                        | undefined                                            | Optional for connected environments and mandatory for disconnected.
pyxis_container_identifier         | undefined                                            | Optional. Use this option if you'd like manually create container project and use it for the submission of the test results. To get this identifier, please create a project of type "Container Image project" at connect.redhat.com. It will be used to submit Preflight `check container` results to Pyxis and connect.redhat.com. This identifier is unique for every container. If you have to certify multiple containers, please create multiple projects. Please do not forget to provide Pyxis token `pyxis_apikey_path` shared for all projects within one partner.
pyxis_operator_identifier          | undefined                                            | Optional. Use this option if you'd like manually create container project and use it for the submission of the test results. To get this identifier, please create a project of type "Operator Bundle Image project" at connect.redhat.com. It will be used to submit Preflight `check operator` results to Pyxis and connect.redhat.com. This identifier is unique for every container. If you have to certify multiple operators, please create multiple projects. Please do not forget to provide Pyxis token `pyxis_apikey_path` shared for all projects within one partner.
create_container_project           | undefined        | Optional. If you use this parameter, DCI would automatically create "Container Image project" for you using `pyxis_apikey_path`. `create_container_project` and `pyxis_container_identifier` are incompatible options, you have to choose one of them.
create_operator_project            | undefined        | Optional. If you use this parameter, DCI would automatically create "Operator Bundle Image project" for you using `pyxis_apikey_path`. `create_operator_project` and `pyxis_operator_identifier` are incompatible options, you have to choose one of them.
create_pr                          | false                                                | Optional. Use this option if you'd like to create a certification PR at [certified-operators](https://github.com/redhat-openshift-ecosystem/certified-operators/pulls). Creation of such a PR is a part of operator certification process and required to publish the operator in the catalog. Please do not forget to provide `github_token_path` when using this option.
merge_pr                           | false                                                | Optional. Use this option if you'd like to merge a certification PR at [certified-operators](https://github.com/redhat-openshift-ecosystem/certified-operators/pulls).
pyxis_product_lists           | None                                 | A list of Product Listings; all of them must be created beforehand [See doc](https://redhat-connect.gitbook.io/red-hat-partner-connect-general-guide/managing-your-account/product-listing). It could contain one or many PLs. If set, it will attach all PLs to both old and new certification projects.


## Two modes of certification

There are two modes of certification:

  - Standalone containers. Please use the variable `preflight_containers_to_certify` if your operator is not yet ready but you'd like to certify the containers.

  - End-to-end operator certification. Please use the variable `preflight_operators_to_certify` if you'd like to certify all container images to which you bundle image is referring and the operator itself.

The idea is use one of them.

## Certification of standalone containers

- Export kubeconfig:

    ```bash
    export KUBECONFIG=/var/lib/dci-openshift-app-agent/kubeconfig
    ```

- Create file settings.yml in /etc/dci-openshift-app-agent/settings.yml and provide all the information about your certification projects. Let’s consider two standard scenarios here.

  a. If you have a connected environment with the private external registry. In the example below, we use the existing certification project for testpmd-operator container and create a new one for bla-bla-operator.

    ```yaml
    $ cat /etc/dci-openshift-app-agent/settings.yml
    ---
    # Job name and tags to be displayed in DCI UI
    dci_name: "Testpmd-Container-Preflight"
    dci_tags: ["debug", "testpmd-container"]
    dci_topic: "OCP-4.7"
    # DCI component for every OCP version
    # could be checked here: https://www.distributed-ci.io/topics
    dci_component: ['8cef32d9-bb90-465f-9b42-8b058878780a']

    # Optional, please provide these credentials
    # if your registry is private.
    partner_creds: "/opt/pull-secrets/partner_config.json"

    # List of images to certify,
    # you could provide many containers at once.
    preflight_containers_to_certify:
      - container_image: "quay.io/rh-nfv-int/testpmd-operator:v0.2.9"
        # Optional; provide it when you need to use
        # the existing project to submit test results.
        # It's an id of your Container Image Project
        # https://connect.redhat.com/projects/my_nice_container_id
        pyxis_container_identifier: "my_nice_container_id"
      - container_image: "quay.io/rh-nfv-int/bla-bla-operator:v0.2.9"
        # Optional; provide it when you need to create
        # a new "Container Image project" and submit test results in it.
        create_container_project: true
        pyxis_product_lists:
          - "65dc9e05f1f7e59bac573122"
          - "65dc9dbb11956b89f14194e0"

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
    # Job name and tags to be displayed in DCI UI
    dci_name: "Testpmd-Container-Preflight"
    dci_tags: ["debug", "testpmd-container"]
    dci_topic: "OCP-4.7"
    # DCI component for every OCP version
    # could be checked here: https://www.distributed-ci.io/topics
    dci_component: ['8cef32d9-bb90-465f-9b42-8b058878780a']

    # Mandatory for disconnected environment,
    # this registry is used for mirrored images
    # and to store an index (catalog) image.
    dci_local_registry: registry.local.lab:4443

    # Credentials for your private registries.
    # You could have several private registries:
    # local and another external, to store the operator.
    # In this case, please provide all credentials here.
    partner_creds: "/opt/pull-secrets/partner_config.json"

    # Optional, provide it if your registry is self-signed.
    preflight_custom_ca: "/var/lib/dci-openshift-agent/registry/certs/cert.ca"

    # List of images to certify,
    # you could provide many containers at once.
    preflight_containers_to_certify:
        # In disconnected environments provide a digest (SHA), not a tag.
      - container_image: "quay.io/rh-nfv-int/testpmd-operator@sha256:339096a68f09eb42aa9bb8d72bf1d958fe14a15c93fb850e27ce18208fed23ed"
        # Optional; provide it when you need to create
        # a new "Container Image project" and submit test results in it.
        create_container_project: true

    # Optional; provide it when you need to submit test results.
    # This token is shared between all your projects.
    # To generate it: connect.redhat.com -> Product certification ->
    # Container API Keys -> Generate new key
    pyxis_apikey_path: "/opt/cache/pyxis-apikey.txt"
    ```

- Run dci-openshift-app-agent:

    ```bash
    dci-openshift-app-agent-ctl -s -- -v
    ```


## Operator end-to-end certification

- Export kubeconfig:

    ```bash
    export KUBECONFIG=/var/lib/dci-openshift-app-agent/kubeconfig
    ```

- Create file settings.yml in /etc/dci-openshift-app-agent/settings.yml and provide all the information about your certification projects. Let’s consider two standard scenarios here.

  a. If you have a connected environment with the private external registry. In the example below, we use existing certification projects for testpmd-operator and create new ones for bla-bla-operator.

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
      - bundle_image: "quay.io/rh-nfv-int/testpmd-operator-bundle:v0.2.9"
        # Mandatory for the connected environments.
        index_image: "quay.io/rh-nfv-int/nfv-example-cnf-catalog:v0.2.9"
        # Optional; provide it when you need to use
        # the existing project to submit test results.
        # It's an id of your Container Image Project
        # https://connect.redhat.com/projects/my_nice_container_id
        pyxis_container_identifier: "my_nice_container_id"
        # Optional; provide it when you need to use
        # the existing project to submit test results.
        # It's an id of your Operator Bundle Image
        # https://connect.redhat.com/projects/my_nice_container_id
        pyxis_operator_identifier: "my_nice_operator_id"
        # Optional; use it to automatically open cert PR
        # at the certified-operators repository
        create_pr: true
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
        # Optional; use it to automatically merge cert PR
        # at the certified-operators repository
        merge_pr: true

    # Optional; provide it when you need to submit test results.
    # This token is shared between all your projects.
    # To generate it: connect.redhat.com -> Product certification ->
    # Container API Keys -> Generate new key
    pyxis_apikey_path: "/opt/cache/pyxis-apikey.txt"

    # Optional; provide this token when using create_pr option
    github_token_path: "/opt/cache/dcicertbot-token.txt"
    ```

  b. There is a disconnected environment with the self-signed local registry and operator images in the external private registry. In the case of a disconnected environment, DCI would handle all the mirroring and regenerate a catalog image.

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

    # Mandatory for disconnected environment,
    # this registry is used for mirrored images
    # and to store an index (catalog) image.
    dci_local_registry: registry.local.lab:4443

    # Optional, provide it if your registry is self-signed.
    preflight_custom_ca: "/var/lib/dci-openshift-agent/registry/certs/cert.ca"

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
        # Optional; provide it when you need to create
        # a new "Container Image project" and submit test results in it.
        create_container_project: true
        # Optional; provide it when you need to create
        # a new "Operator Bundle Image" and submit test results in it.
        create_operator_project: true
        # Optional; use it to automatically open cert PR
        # at the certified-operators repository
        create_pr: true
        # Optional; use it to automatically merge cert PR
        # at the certified-operators repository
        merge_pr: true

    # Optional; provide it when you need to submit test results.
    # This token is shared between all your projects.
    # To generate it: connect.redhat.com -> Product certification ->
    # Container API Keys -> Generate new key
    pyxis_apikey_path: "/opt/cache/pyxis-apikey.txt"

    # Optional; provide this token when using create_pr option
    github_token_path: "/opt/cache/dcicertbot-token.txt"
    ```

- Run dci-openshift-app-agent:

    ```bash
    dci-openshift-app-agent-ctl -s -- -v
    ```

## Preflight CI

If the variable `preflight_source_dir` is defined, the Preflight role would use this folder to generate preflight image and binary and then use them during Preflight tests execution. That would overwrite predefined preflight_image and if any.

Currently, Preflight CI stores the generated preflight image into a `dci_local_registry` and hence would only work in disconnected environments with a registry attached. The plan is to remove this limitation in the next releases.
