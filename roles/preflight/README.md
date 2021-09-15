# This role is to run preflight cert suite

## Variables

Name                               | Default                                              | Description
---------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
do\_preflight\_tests               | false                                                | Launch the [Preflight Cert Suite](https://github.com/redhat-openshift-ecosystem/openshift-preflight)
preflight\_version                 | quay.io/opdev/preflight:1.0.4                        | [Version of Preflight Cert Suite to run](https://quay.io/repository/opdev/preflight?tab=tags)
preflight\_operators\_to\_check    | undefined                                            | List of operators to be checked with Preflight Cert Suite. Please check [example_preflight_config.yaml](#example-of-config-file-to-define-a-list-of-operators-to-check) for the example.
operator\_sdk\_tool\_path          | undefined                                            | Path to operator-sdk binary, optional. Please check [example_preflight_config.yaml](#example-of-config-file-to-define-a-list-of-operators-to-check) for the example.
preflight\_namespace               | preflight-testing                                    | Namespace to use for preflight tests

## Role structure

![](files/preflight_role_structure.png)

## Example of config file to define a list of operators to check

```yaml
---
# preflight-config.yaml
operator_sdk_tool_path: "/usr/local/bin/operator-sdk-flag"

preflight_operators_to_check:
  -
    image: "quay.io/rh-nfv-int/testpmd-operator-bundle@sha256:5e28f883faacefa847104ebba1a1a22ee897b7576f0af6b8253c68b5c8f42815"
    index_image: "quay.io/tkrishtop/index-testpmd-operator-bundle:v0.2.9"
  -
    image: "quay.io/opdev/simple-demo-operator-bundle@sha256:eff7f86a54ef2a340dbf739ef955ab50397bef70f26147ed999e989cfc116b79"
    index_image: "quay.io/opdev/simple-demo-operator-catalog:v0.0.3"
...
```

**Mandatory** `preflight_operators_to_check` should be provided to run preflight or operator-sdk tests.
**Optional** `operator_sdk_tool_path` should be provided to run operator-sdk scorecard tests.
Here is the invocation:

```console
dci-openshift-app-agent-ctl -s -- -v \
-e kubeconfig_path=path/to/kubeconfig \
-e do_preflight_tests=true \
-e @preflight_config.yaml
```
