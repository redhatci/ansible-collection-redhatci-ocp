# CNF_cert Role

This role encapsulates the logic for the [Test Network Function (TNF)](https://github.com/test-network-function/cnf-certification-test). It is responsible for deploying the TNF framework and running the tests in DCI.

Before executing the CNF (Cloud-native network function) Cert Suite, it's important to label the pods to test using the auto-discovery feature. You can do it manually or programmatically. An example of this can be found in [tnf_test_example](../../samples/tnf_test_example/README.md).

## Variables

Name                                    | Default                                                                                                                                                                                                                                 | Description
--------------------------------------- |-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| -------------------------------------------------------------
tnf\_stage                              | "tests"                                                                                                                                                                                                                                 | Stage to be run when calling the role from outside. Possible values: "tests" (default), "post-run" and "teardown".
tnf\_check\_commit\_sha                 | false                                                                                                                                                                                                                                   | Flag that allows to check if the tnf image used is based on the same commit SHA than the repository cloned in this role.
test\_network\_function\_repo           | https://github.com/test-network-function/cnf-certification-test                                                                                                                                                                         | Repository to download the tnf code.
test\_network\_function\_src\_dir       | undefined                                                                                                                                                                                                                               | If testing a cnf-certification-test PR, this variable will be injected from test-runner scripts (used in dci-pipeline and dci-openshift-agent projects) to refer to the file path where the code from the PR is placed in the jumphost, so that it can be used in cnf_cert role to build a new tnf container image based on that code
test\_network\_function\_version        | v5.0.7                                                                                                                                                                                                                                 | CNF Cert Suite version downloaded. DCI App Agent supports from v4.4.0 till the latest stable version. HEAD version (in the main branch) can be also used, but it is not guaranteed a complete compatibility with the latest unstable changes.
test\_network\_function\_project\_name  | cnf-certification-test                                                                                                                                                                                                                  | Directory name to look at on the tnf repo.
tnf\_labels                             | `"all"`                                                                                                                                                                                                                                 | List of [test suites](https://test-network-function.github.io/cnf-certification-test/test-spec/#available-test-specs) that are executed/skipped using labels. In particular, `tnf_labels` content must follow [these guidelines](https://onsi.github.io/ginkgo/#spec-labels), then dci-openshift-app-agent uses this string to run the tnf container with `-l` argument. Note that, when using labels, apart from using the tnf suite names as labels, you can also use, among others, `common` label to refer to non-Telco tnf suites, `telco` label to include Telco-related tests, `extended` to other Verizon-related tests, `faredge` to Far-Edge tests, and `preflight` to run preflight on tnf. With `all`, you will execute all suites. See the [cnf-certification-test README](https://test-network-function.github.io/cnf-certification-test/test-container/#run-the-tests) for more information, and also, check [CATALOG.md](https://github.com/test-network-function/cnf-certification-test/blob/main/CATALOG.md) to see the list of test suites available with the label that corresponds to each of them.
tnf\_config                             | tnf_config:<br>&nbsp;&nbsp; - namespace: "{{ dci_openshift_app_ns }}"<br>&nbsp;&nbsp; targetpodlabels: []<br>&nbsp;&nbsp; targetoperatorlabels: []<br>&nbsp;&nbsp; target_crds: []<br> &nbsp;&nbsp; exclude_connectivity_regexp: ""<br> | A complex variable to define the configuration to be applied in CNF Cert Suite.<ul> <li> namespace: Target namespace. </li> <li>targetpodlabels: List of autodiscovery labels to be considered by the CNF Cert Suite for pod testing.</li> <li>targetoperatorlabels: List of auto-discovery labels to be considered by the CNF Cert Suite for operator testing.</li> <li>target_crds: List of CRDs under test in the targeted namespace.</li> <li>exclude_connectivity_regexp: A regexp to exclude containers from the connectivity test (optional).</li> </ul> See [this](../../samples/tnf_test_example) for more details about an example defining this variable.<br> * Testing multiple resources on different namespaces is supported.
accepted\_kernel\_taints                | []                                                                                                                                                                                                                                      | Allow-list for tainted modules. It must be composed of a list of elements called module: "<module_name>"; e.g.:<br>accepted_kernel_taints:<br>&nbsp;&nbsp; - module: "taint1"<br>&nbsp;&nbsp; - module: "taint2"
tnf\_services\_ignore\_list             | []                                                                                                                                                                                                                                      | Ignore list for services under test. This allows CNF Cert Suite execution to skip these services for some specific unit tests, such as checking dual-stack configuration, among others.
tnf\_postrun\_delete\_resources         | true                                                                                                                                                                                                                                    | Control if the deployed resources are kept after the CNF Cert Suite execution for debugging purposes
tnf\_env\_vars                          | {"TNF_ENABLE_XML_CREATION": "true"}                                                                                                                                                                                                                                 | Environment variables to be provided in a dictionary for tnf execution. Check [the section below](#example-of-tnf_env_vars-variable) for more information. Note that `TNF_ENABLE_XML_CREATION: true` is required from tnf v5.0.0 (including HEAD), else JUnit file will not be created.
tnf\_feedback                           | Each entry of the dict is composed by key = tnf test name and value = "". Check [defaults/main.yml file](defaults/main.yml)                                                                                                                                                                                                                                    | You can provide feedback to the auto-generated report by tnf. You just need to fill the feedback for the desired tests in this new variable.

## Example of a tnf_config variable to test pods deployed on multiple namespaces not using label prefixes

The format of the targetpodlabels list has the following format: <label_name>=<label_value>

```yaml
---
tnf_config:
  - namespace: "test-cnf"
    targetpodlabels: [environment=test]
    exclude_connectivity_regexp: ""
  - namespace: "production-cnf"
    targetpodlabels: [environment=production]
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
    exclude_connectivity_regexp: ""
  - namespace: "production-cnf"
    targetpodlabels: [test-network-function.com/environment=production]
    exclude_connectivity_regexp: ""
...
```

## How to test operators?

It is allowed to auto-discover operators using custom labels. For this purpose, you can use `targetoperatorlabels` attribute for each `tnf_config` item. Of course this is optional.

Imagine you have an operator labeled as `operator-label=hello` in `test-cnf` namespace. You can auto-discover it by doing the following (just using the first `tnf_config` example showed above for the sake of completeness):

```yaml
---
tnf_config:
  - namespace: "test-cnf"
    targetpodlabels: [environment=test]
    targetoperatorlabels: [operator-label=hello]
    exclude_connectivity_regexp: ""
  - namespace: "production-cnf"
    targetpodlabels: [environment=production]
    targetoperatorlabels: []
    exclude_connectivity_regexp: ""
...
```

If the label value is empty, then just include the label key followed by `=`, for example, using the same label key (the same applies for `targetpodlabels`, in fact, in case we have pods with a label without value):

```yaml
---
tnf_config:
  - namespace: "test-cnf"
    targetpodlabels: [environment=test]
    targetoperatorlabels: [operator-label=]
    exclude_connectivity_regexp: ""
  - namespace: "production-cnf"
    targetpodlabels: [environment=production]
    targetoperatorlabels: []
    exclude_connectivity_regexp: ""
...
```

## Example of tnf_env_vars variable

This variable must be a dictionary, where the key is the tnf environment variable to be used during execution. You have some examples of possible variables to be provided in the [tnf docs](https://test-network-function.github.io/cnf-certification-test/runtime-env) or in the [script](https://github.com/test-network-function/cnf-certification-test/blob/main/script/run-container.sh) used to run the tnf container.

For example, the following configuration defines these three environment variables:

- `TNF_NON_INTRUSIVE_ONLY`: if set to true, skip intrusive tests which may disrupt cluster operations (default `false`).
- `TNF_LOG_LEVEL`: log level used to run the CNF Cert Suite (default `info`).
- `TNF_ALLOW_PREFLIGHT_INSECURE`: (required when running preflight on CNF Cert Suite) if set to true, allow the Preflight execution ran by CNF Cert Suite to access to insecure registries. This should be needed when accessing to private registries. Remember also to turn on preflight test suite with `preflight` label.

Also, note that `TNF_ENABLE_XML_CREATION: true` is required from tnf v5.0.0 (including HEAD), else JUnit file will not be created.

```yaml
---
tnf_env_vars:
  TNF_ENABLE_XML_CREATION: true
  TNF_NON_INTRUSIVE_ONLY: true
  TNF_LOG_LEVEL: "debug"
  TNF_ALLOW_PREFLIGHT_INSECURE: true
...
```

Note that cnf_cert role appends to `tnf_env_vars` the environment variables called `TNF_PARTNER_REPO`, `TNF_IMAGE` and `SUPPORT_IMAGE`, as they are defined in runtime. So please **do not define** these variables in `tnf_env_vars`; just let cnf_cert role do its job.

## Some reminders when running preflight with CNF Cert Suite

If you want to run preflight on CNF Cert Suite, you need to: 1) use the proper reference to preflight on `tnf_labels`, 2) define `partner_creds` variable, and 3) properly add `TNF_ALLOW_PREFLIGHT_INSECURE` variable to `tnf_env_vars`.

## Visualize the results with HTML results application.

In the job, starting from tnf v4.4.0 in advance, you will see that a new `tar.gz` file is submitted to the Files section in the DCI jobs. This is called `<timestamp>-cnf-test-results.tar.gz`.

If you extract the compressed files in one single place and open `results.html`, you can see a pre-loaded information extracted from `claim.json` file. If you choose the scenario of your case (telco, extended, etc.), you will see, in Results section, the report of the tnf tests with the corresponding results, having also the opportunity of providing feedback to each test.

It is also possible to provide feedback with `tnf_feedback` variable. You just need to write the feedback for the tests in which you are interested in, and then DCI will take care of pre-load that information in the HTML report.

In [defaults/main.yml](defaults/main.yml), you have a template that you can use in your pipeline file, so that you can fill the value for the tests you want to provide feedback. You don't need to include the tests that you don't want to provide feedback. To insert line breaks, use `\\n` (you need to escape it, else there can be rendering issues). Same for quotes and so on.

In any case, when you finish filling in the feedback in the report, you can generate a new report with that feedback included, by just selecting the scenario you want to evaluate (non-telco, telco, extended...), and pushing in the "Download Results Feedback" button. The resulting HTML resource should be the document to be provided when submitting CNF Certification.

You can also upload a `claim.json` file obtained from the execution (also available in the Files section of the DCI job) in the form you have at the top, if you want to load a different file. Anyway, the report already contains the `claim.json` file.

This is a feature provided by CNF Cert Suite, please check in their documentation for finding more information about this tool.
