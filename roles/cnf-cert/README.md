# CNF-cert Role

This role encapulates the logic for the [Test Network Function (TNF)](https://github.com/test-network-function/cnf-certification-test). It is responsible for deploying the TNF framework and running the tests in DCI.

Before executing the CNF (Cloud-native network function) Cert Suite, it's important to label the pods to test using the autodiscovery feature. You can do it manually or programatically. An example of this can be found in [tnf_test_example](../../samples/tnf_test_example/README.md).

## Variables

Name                                    | Default                                              | Description
--------------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
tnf\_suites                             | `"-f access-control networking lifecycle observability platform-alteration operator manageability"` | List of  [test suites](https://github.com/test-network-function/cnf-certification-test#general-tests) that are executed or skipped. They must include the arguments that select the test suites to be executed/skipped, [according to the docs](https://github.com/test-network-function/cnf-certification-test#run-the-tests).<br> * Manageability test suite will only run with HEAD version.
test\_network\_function\_version        | v4.0.2                                               | CNF Cert Suite version downloaded. DCI App Agent supports the latest stable version, which is v4.0.2, and also it has backwards compatibility with v3.x.x, however it is not ensured that it is completely compatible with older versions. HEAD version (in the main branch) can be also used, but it is not guaranteed a complete compatibility with the latest unstable changes.
test\_network\_function\_project\_name  | cnf-certification-test                               | Directory name to look at on the tnf repo.
tnf\_config                             | tnf_config:<br>&nbsp;&nbsp; - namespace: "{{ dci_openshift_app_ns }}"<br>&nbsp;&nbsp; targetpodlabels: []<br>&nbsp;&nbsp; target_crds: []<br>&nbsp;&nbsp; operators_regexp: ""<br> &nbsp;&nbsp; exclude_connectivity_regexp: ""<br>                                  | A complex variable to define the configuration to be applied in CNF Cert Suite.<ul> <li> namespace: Target namespace. </li> <li>targetpodlabels: List of autodiscovery labels to be considered by the CNF Cert Suite for pod testing.</li><li>target_crds: List of CRDs under test in the targeted namespace.</li><li> operators_regexp:  A regexp to select operators to be tested by the CNF Cert Suite (optional). </li> <li>exclude_connectivity_regexp: A regexp to exclude containers from the connectivity test (optional).</li> </ul> See [this](../../samples/tnf_test_example/hooks/templates/test_statefulset.yml.j2) for more details.<br> * Testing multiple resources on different namespaces is supported.
accepted\_kernel\_taints                | []                                                   | Allow-list for tainted modules. It must be composed of a list of elements called module: "<module_name>"; e.g.:<br>accepted_kernel_taints:<br>&nbsp;&nbsp; - module: "taint1"<br>&nbsp;&nbsp; - module: "taint2"
tnf\_non\_intrusive\_only               | true                                                 | Skip intrusive tests which may disrupt cluster operations.
tnf\_run\_cfd\_test                     | false                                                | The test suites from [openshift-kni/cnf-feature-deploy](https://github.com/openshift-kni/cnf-features-deploy) will be run prior to the actual CNF certification test execution and the results are incorporated in the same claim.
tnf\_log\_level                         | "debug"                                              | Log level used to run the CNF Cert Suite. Possible values can be seen [here](https://github.com/test-network-function/cnf-certification-test#log-level)
tnf\_postrun\_delete\_resources         | true                                                 | Control if the deployed resources are kept after the CNF Cert Suite execution for debugging purposes

## Example of a tnf_config file to test pods deployed on multiple namespaces not using label prefixes

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

## Example of a tnf_config file to test pods deployed on multiple namespaces using label prefixes

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

## Defining Operators_regexp

In case of needing it, the code to handle it must be included in the partner's hooks
