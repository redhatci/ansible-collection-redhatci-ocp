# Operator_SDK test suite Role

This role integrates the Operator-SDK Scorecard test suite as part of the DCI Application Agent. Operator-SDK is a [command-line interface](https://github.com/operator-framework/operator-sdk) used to generate and validate operators.

Please note that these tests do not have a standalone Red Hat certification associated with them. However, a subset of these tests is included in the [Preflight certification suite](https://github.com/redhat-openshift-ecosystem/openshift-preflight), while another subset is part of the PR tests with the Tekton pipeline in the [certified-operators repository](https://github.com/redhat-openshift-ecosystem/certified-operators/pulls). You can utilize this role to thoroughly validate your operator.

## Global Variables

| Name                               | Default   | Description  |
| ---------------------------------- | --------- | ------------ |
| scorecard_operators     | undefined | Mandatory, list of operators to be checked with Operator-SDK Suite. You could find an example [here](#operator-end-to-end-certification). |
| scorecard_namespace                | scorecard-testing | Optional, namespace to use. |
| operator_sdk_img   | quay.io/operator-framework/operator-sdk@sha256:bbf540202645b1e24b02803b22618df7c16e414ac8e12ee0fb77c8a19b1ec780 | Optional, main image with the binary, latest v1.30.0 https://quay.io/repository/operator-framework/operator-sdk?tab=tags |
| scorecard_test_img | quay.io/operator-framework/scorecard-test@sha256:9b527bcd4f6e5cd879dc36beb1dd700491eacc68762dc75ebea590f53c4a56ee | Optional, image for the test pod, latest v1.30.0: https://quay.io/repository/operator-framework/scorecard-test?tab=tags |
| scorecard_storage_img | quay.io/operator-framework/scorecard-storage@sha256:a3bfda71281393c7794cabdd39c563fb050d3020fd0b642ea164646bdd39a0e2 | Optional, storage image, latest 1.28.1 https://quay.io/repository/operator-framework/scorecard-storage?tab=tags |
| scorecard_untar_img | quay.io/operator-framework/scorecard-untar@sha256:2e728c5e67a7f4dec0df157a322dd5671212e8ae60f69137463bd4fdfbff8747 | Optional, untar image, latest 1.28.1 https://quay.io/repository/operator-framework/scorecard-untar?tab=tags |


## Variables to define for each operator in scorecard_operators

Name                               | Default                                              | Description
---------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
bundle_image                       | undefined                                            | Mandatory. In the connected environment, the image could be provided by tag. In the disconnected, you have to provide the image by digest. |
index_image                        | undefined                                            | Mandatory for connected environments |

## Dependencies

### Variable dependencies

Please be aware that the following global variables must be set to use the role:

- oc_tool_path
- partner_creds
- kubeconfig_path
- pullsecret_tmp_file
- job_logs
- dci_local_registry
- dci_disconnected

These variables are referred to within the role with the "scorecard_" prefix, with the intention of making the role standalone in the future. However, their functionality remains the same. For the default values, please review the group_vars/all file.

### Role dependencies:

```
---
dependencies:
  - role: mirror_images
  - role: fbc_catalog
  - role: check_resource
  - role: mirror_catalog
...
```

## Example of the config

1. Disconnected environment

```
scorecard_operators:
    - bundle_image: "icr.io/cpopen/ibm-mq-operator-bundle@sha256:11639e73211324978bde65fbe35d7f71ee2b7efd96e4d5d1c8158855256c2cae" # v1.3.2
    - bundle_image: "quay.io/telcoci/simple-demo-operator-bundle@sha256:6cfbca9b14a51143cfc5d0d56494e7f26ad1cd3e662eedd2bcbebf207af59c86" # v0.0.6
```

2. Connected environment

```
scorecard_operators:
    - bundle_image: "icr.io/cpopen/ibm-mq-operator-bundle:v1.3.2"
      index_image: "icr.io/cpopen/ibm-operator-catalog:v1.30"
    - bundle_image: "quay.io/telcoci/simple-demo-operator-bundle:v0.0.6"
      index_image: "quay.io/telcoci/simple-demo-operator-catalog:v0.0.6"
```


## Generated output for each operator in scorecard_operators

| Filename                                                 | Content |
| -------------------------------------------------------- | ------- |
| scorecard_{{ operator_name }}_basic_check_spec_test.json | [Basic Test Suite](https://sdk.operatorframework.io/docs/testing-operators/scorecard/#basic-test-suite) |
| scorecard_{{ operator_name }}_errors_basic_check_spec_test.json | [Errors if Operator-SDK produced timeout](https://github.com/operator-framework/operator-sdk/issues/5452) |
| scorecard_{{ operator_name }}_suite_olm.json | [OLM Test Suite](https://sdk.operatorframework.io/docs/testing-operators/scorecard/#olm-test-suite) |
