# This role uses Pyxis API to submit preflight certification results

## Fully automated preflight operator certification flow

- DCI runs preflight tests and generates a file with test results for each operator
- This file results.json is parsed and submitted to Pyxis API

## Variables

Name                               | Default                                              | Description
---------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
preflight\_operators\_to\_check    | undefined                                            | List of operators to be checked with Preflight Cert Suite. This variable is mandatory to run Preflight cert suite. Please check [example_config.yaml](README.md#example-of-config-file-to-define-a-list-of-operators-to-certify) for the example.
submit\_preflight\_to\_pyxis       | false                                                | Should be set to true to submit Preflight results to Pyxis. Please do not forget to provide Pyxis credentials: pyxis\_apikey\_path with Pyxis token (shared for all projects within one client) and pyxis\_identifier (each operator should have its own certification project with the unique identifier).
pyxis\_apikey\_path                | undefined                                            | This is a path to file that contains partner's token. Parner should generate this token in connect.redhat.com. The token is shared for all projects within one partner.
pyxis\_identifier                  | undefined                                            | Each operator should have its own certification project with the unique identifier. If the partner has to certify two operators, he has to create two certification projects. Once a new cert project is created, the identifier could be extracted from the project url: https://connect.redhat.com/projects/pyxis_identifier/overview


## Example of config file to define a list of operators to certify

```yaml
---
# preflight-config.yaml
preflight_operators_to_check:
  - name: "simple-demo-operator"
    version: "v0.0.3"
    bundle_image: "quay.io/opdev/simple-demo-operator-bundle@sha256:eff7f86a54ef2a340dbf739ef955ab50397bef70f26147ed999e989cfc116b79"
    index_image: "quay.io/opdev/simple-demo-operator-catalog:v0.0.3"
    pyxis_identifier: "project-identifier-for-simple-demo-operator"
  - name: "testpmd-operator"
    version: "v0.2.9"
    bundle_image: "quay.io/rh-nfv-int/testpmd-operator-bundle@sha256:5e28f883faacefa847104ebba1a1a22ee897b7576f0af6b8253c68b5c8f42815"
    index_image: "quay.io/tkrishtop/index-testpmd-operator-bundle:v0.2.9"
    pyxis_identifier: "project-identifier-for-testpmd-operator"
# pyxis token
pyxis_apikey_path: "/path/to/partner/file/with/token"
```

**Mandatory** `preflight_operators_to_check` should be provided to run Preflight tests.
**Mandatory** `pyxis_identifier` and `pyxis_apikey_path` should be provided to submit the results of Preflight tests to Pyxis.

Here is the invocation:

```console
dci-openshift-app-agent-ctl -s -- -v \
-e kubeconfig_path=path/to/kubeconfig \
-e submit_preflight_to_pyxis=true \
-e @preflight_config.yaml
```