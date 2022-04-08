# Preflight cert suite Role

Preflight is a commandline interface for validating if OpenShift operator bundles and containers meet minimum requirements for Red Hat OpenShift Certification.

This role implements the preflight test suite as part of DCI Application Agent.

## Variables

Name                               | Default                                              | Description
---------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
do\_preflight\_tests               | false                                                | Trigger to activate the preflight tests
preflight\_version                 | quay.io/opdev/preflight:1.0.8                        | [Version of Preflight Cert Suite to run](https://quay.io/repository/opdev/preflight?tab=tags)
preflight\_operators\_to\_certify  | undefined                                            | List of operators to be checked for certification with Preflight Cert Suite. This variable is mandatory to run Preflight cert suite. Please check [example_preflight_config.yaml](#example-of-config-file-to-define-a-list-of-operators-to-certify) for the example.
operator\_sdk\_tool\_path          | undefined                                            | Path to operator-sdk binary, optional. Please check [example_preflight_config.yaml](#example-of-config-file-to-define-a-list-of-operators-to-certify) for the example.
preflight\_namespace               | preflight-testing                                    | Namespace to use for preflight tests
submit\_preflight\_to\_pyxis       | false                                                | Should be set to true to submit Preflight results to Pyxis. Please do not forget to provide Pyxis credentials: pyxis\_apikey\_path with Pyxis token (shared for all projects within one client) and pyxis\_identifier (each operator should have its own certification project with the unique identifier).
pyxis\_apikey\_path                | undefined                                            | This is a path to file that contains partner's token. Parner should generate this token in connect.redhat.com. The token is shared for all projects within one partner.
pyxis\_identifier                  | undefined                                            | Each operator should have its own certification project with the unique identifier. If the partner has to certify two operators, he has to create two certification projects. Once a new cert project is created, the identifier could be extracted from the project url: https://connect.redhat.com/projects/pyxis_identifier/overview
preflight\_custom\_ca              | undefined                                            | Path of custom ca.crt. Used to test operator stored in a self signed registry


## Example of config file to define a list of operators to certify

```yaml
---
# preflight-config.yaml

do_preflight_tests: true

# optional
# operator_sdk_tool_path: "/usr/local/bin/operator-sdk-flag"

# Uncomment the next two lines if you need to use the latest Preflight pre-release:
# preflight_binary: https://github.com/redhat-openshift-ecosystem/openshift-preflight/releases/download/1.1.0-beta4/preflight-linux-amd64
# preflight_image: quay.io/opdev/preflight:1.1.0-beta4

# all certification projects for one partner
# share one access token
pyxis_apikey_path: APIKEY_PATH

preflight_operators_to_certify:
  - bundle_image: "quay.io/rh-nfv-int/testpmd-operator-bundle:v0.2.9"
    pyxis_identifier: PROJECTID
  - bundle_image: "quay.io/opdev/simple-demo-operator-bundle:v0.0.5"
    pyxis_identifier: PROJECTID
...
```

**Mandatory**
- `preflight_operators_to_certify` should be provided to run preflight or operator-sdk tests.
- `pyxis_apikey_path` and `pyxis_identifier` can be found on connect.redhat.com


**Optional**

- `preflight_image: quay.io/opdev/preflight:1.1.0-beta4` should be provided if you intend to test againts the latest Preflight pre-release, it's used for `check operator` tests
- `preflight_binary: https://github.com/redhat-openshift-ecosystem/openshift-preflight/releases/download/1.1.0-beta4/preflight-linux-amd64` should be provided if you intend to test againts the latest Preflight pre-release, it's used for `check container` tests
`operator_sdk_tool_path` should be provided to run operator-sdk scorecard tests.
- `pyxis_apikey_path` and `pyxis_identifier` can be found on connect.redhat.com, they are optional for current Preflight GA 1.0.8, and will be mandatory starting from Preflight release 1.1.0

**Invocation**
Here is the invocation:

```console
dci-openshift-app-agent-ctl -s -- -v \
-e kubeconfig_path=path/to/kubeconfig \
-e @preflight_config.yaml
```
