# CNF-cert Role

This role encapulates the logic for the [Test Network Function (TNF)](https://github.com/test-network-function/cnf-certification-test). It is responsible for deploying the TNF framework and running the tests in DCI.

Before executing the CNF (Cloud-native network function) Cert Suite, it's important to label the pods to test using the autodiscovery feature. You can do it manually or programatically. An example of this can be found in [tnf_test_example](../../samples/tnf_test_example/README.md).

## Variables

Name                                    | Default                                              | Description
--------------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
test\_network\_function\_repo           | https://github.com/test-network-function/cnf-certification-test | Repository to download the tnf code. However, if we are testing a pull request from cnf-certification-test repo, this variable will be pointing to the file path where the pull request code has been downloaded in the jumphost.
test\_network\_function\_version        | v4.0.2                                               | CNF Cert Suite version downloaded. DCI App Agent supports the latest stable version, which is v4.0.2, and also it has backwards compatibility with v3.x.x, however it is not ensured that it is completely compatible with older versions. HEAD version (in the main branch) can be also used, but it is not guaranteed a complete compatibility with the latest unstable changes.
test\_network\_function\_project\_name  | cnf-certification-test                               | Directory name to look at on the tnf repo.
tnf\_suites                             | `"access-control networking lifecycle observability platform-alteration operator manageability affiliated-certification-container-is-certified"` | List of [test suites](https://github.com/test-network-function/cnf-certification-test#general-tests) that are executed. In particular, `tnf_suites` content must be the list of suites to be run, space separated, so that dci-openshift-app-agent uses this string list to run the tnf container with `-f` argument. See the [cnf-certification-test README](https://github.com/test-network-function/cnf-certification-test/tree/v4.0.2#run-the-tests) for more information.<br> * Manageability test suite will only run with HEAD version.
tnf\_skip\_suites                       | ""                                                   | List of [test suites](https://github.com/test-network-function/cnf-certification-test#general-tests) that are skipped. In particular, `tnf_skip_suites` content must be the list of suites to be skipped, space separated, so that dci-openshift-app-agent uses this string list to run the tnf container with `-s` argument. Remember that this argument is discarded if no `tnf_suites` are provided. See the [cnf-certification-test README](https://github.com/test-network-function/cnf-certification-test/tree/v4.0.2#run-the-tests) for more information.
tnf\_labels                             | ""                                                   | List of [test suites](https://github.com/test-network-function/cnf-certification-test#general-tests) that are executed/skipped using labels. In particular, `tnf_labels` content must follow [these guidelines](https://onsi.github.io/ginkgo/#spec-labels), then dci-openshift-app-agent uses this string to run the tnf container with `-l` argument. See the [cnf-certification-test README](https://github.com/test-network-function/cnf-certification-test#run-the-tests) for more information.<br> * This way of defining test suites can only be used with HEAD version.
tnf\_config                             | tnf_config:<br>&nbsp;&nbsp; - namespace: "{{ dci_openshift_app_ns }}"<br>&nbsp;&nbsp; targetpodlabels: []<br>&nbsp;&nbsp; target_crds: []<br>&nbsp;&nbsp; operators_regexp: ""<br> &nbsp;&nbsp; exclude_connectivity_regexp: ""<br>                                  | A complex variable to define the configuration to be applied in CNF Cert Suite.<ul> <li> namespace: Target namespace. </li> <li>targetpodlabels: List of autodiscovery labels to be considered by the CNF Cert Suite for pod testing.</li><li>target_crds: List of CRDs under test in the targeted namespace.</li><li> operators_regexp:  A regexp to select operators to be tested by the CNF Cert Suite (optional). </li> <li>exclude_connectivity_regexp: A regexp to exclude containers from the connectivity test (optional).</li> </ul> See [this](../../samples/tnf_test_example/hooks/templates/test_statefulset.yml.j2) for more details.<br> * Testing multiple resources on different namespaces is supported.
accepted\_kernel\_taints                | []                                                   | Allow-list for tainted modules. It must be composed of a list of elements called module: "<module_name>"; e.g.:<br>accepted_kernel_taints:<br>&nbsp;&nbsp; - module: "taint1"<br>&nbsp;&nbsp; - module: "taint2"
tnf\_non\_intrusive\_only               | true                                                 | Skip intrusive tests which may disrupt cluster operations.
tnf\_run\_cfd\_test                     | false                                                | The test suites from [openshift-kni/cnf-feature-deploy](https://github.com/openshift-kni/cnf-features-deploy) will be run prior to the actual CNF certification test execution and the results are incorporated in the same claim.
tnf\_log\_level                         | "debug"                                              | Log level used to run the CNF Cert Suite. Possible values can be seen [here](https://github.com/test-network-function/cnf-certification-test#log-level)
tnf\_postrun\_delete\_resources         | true                                                 | Control if the deployed resources are kept after the CNF Cert Suite execution for debugging purposes
tnf\_certified\_container\_info         | []                                                   | Container images to be tested with [affiliated-certification test suite](https://github.com/test-network-function/cnf-certification-test/blob/main/CATALOG.md#container-is-certified) (you must specify that suite, or at least the test called affiliated-certification-container-is-certified, in tnf\_suite to get them tested). Each item are composed by the following variables: <ul> <li>name (mandatory): Container image name.</li> <li>repository (mandatory): Public registry where the container image is placed.</li> <li>tag (optional, "latest" assumed if empty): Container image tag.</li> <li>digest (optional; if set, it takes precedente over tag): Container image digest.</li></ul> Examples with these four values filled can be seen in the `tnf_config.yml` [file](https://github.com/test-network-function/cnf-certification-test/blob/main/cnf-certification-test/tnf_config.yml) provided in cnf-certification-test repository, within the `certifiedcontainerinfo` variable.

## Example of a tnf_config variable to test pods deployed on multiple namespaces not using label prefixes

The format of the targetpodlabels list has the following format: <label_name>=<label_value>

```yaml
---
tnf_config:
  - namespace: "test-cnf"
    targetpodlabels: [environment=test]
    operators_regexp: ""
    exclude_connectivity_regexp: ""
  - namespace: "production-cnf"
    targetpodlabels: [environment=production]
    operators_regexp: ""
    exclude_connectivity_regexp: ""
...
```

## Example of a tnf_config variable to test pods deployed on multiple namespaces using label prefixes

The format of the targetpodlabels list has the following format: <label_prefix>/<label_name>=<label_value>

```yaml
---
tnf_config:
  - namespace: "test-cnf"
    targetpodlabels: [test-network-function.com/environment=test]
    operators_regexp: ""
    exclude_connectivity_regexp: ""
  - namespace: "production-cnf"
    targetpodlabels: [test-network-function.com/environment=production]
    operators_regexp: ""
    exclude_connectivity_regexp: ""
...
```

## Defining operators_regexp in tnf_config variable

In case of needing it, the code to handle it must be included in the partner's hooks

## Example of tnf_certified_container_info variable

This example is based on the content that can be retrieved in the `tnf_config.yml` [file](https://github.com/test-network-function/cnf-certification-test/blob/main/cnf-certification-test/tnf_config.yml) provided in cnf-certification-test repository, within the `certifiedcontainerinfo` variable.

```yaml
---
tnf_certified_container_info:
  - name: rocketchat/rocketchat
    repository: registry.connect.redhat.com
    tag: 0.56.0-1 # optional, "latest" assumed if empty
    digest: # if set, takes precedence over tag. e.g. "sha256:aa34453a6417f8f76423ffd2cf874e9c4a1a5451ac872b78dc636ab54a0ebbc3"
  - name: rocketchat/rocketchat
    repository: registry.connect.redhat.com
    tag: 0.56.0-1
    digest: sha256:c358eee360a1e7754c2d555ec5fba4e6a42f1ede2bc9dd9e59068dd287113b33
...
```
