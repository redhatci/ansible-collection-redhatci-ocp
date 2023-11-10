# CNF_cert Role

This role encapulates the logic for the [Test Network Function (TNF)](https://github.com/test-network-function/cnf-certification-test). It is responsible for deploying the TNF framework and running the tests in DCI.

Before executing the CNF (Cloud-native network function) Cert Suite, it's important to label the pods to test using the autodiscovery feature. You can do it manually or programmatically. An example of this can be found in [tnf_test_example](../../samples/tnf_test_example/README.md).

## Variables

Name                                    | Default                                                                                                                                                                                                                                 | Description
--------------------------------------- |-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| -------------------------------------------------------------
tnf\_stage                              | "tests"                                                                                                                                                                                                                                 | Stage to be run when calling the role from outside. Possible values: "tests" (default), "post-run" and "teardown".
tnf\_check\_commit\_sha                 | false                                                                                                                                                                                                                                   | Flag that allows to check if the tnf image used is based on the same commit SHA than the repository cloned in this role.
test\_network\_function\_repo           | https://github.com/test-network-function/cnf-certification-test                                                                                                                                                                         | Repository to download the tnf code.
test\_network\_function\_src\_dir       | undefined                                                                                                                                                                                                                               | If testing a cnf-certification-test PR, this variable will be injected from test-runner scripts (used in dci-pipeline and dci-openshift-agent projects) to refer to the file path where the code from the PR is placed in the jumphost, so that it can be used in cnf_cert role to build a new tnf container image based on that code
test\_network\_function\_version        | v4.5.5                                                                                                                                                                                                                                  | CNF Cert Suite version downloaded. DCI App Agent supports the latest stable version. HEAD version (in the main branch) can be also used, but it is not guaranteed a complete compatibility with the latest unstable changes. The versions prior to v4.0.0 are not compatible with the agent. Note that, starting from v4.1.6 (also with HEAD branch), tnf will also launch Preflight from CNF Cert Suite (included in `common` label until `v4.2.2`; from `v4.2.3` in advance, you need to explicitly use `preflight` label).
test\_network\_function\_project\_name  | cnf-certification-test                                                                                                                                                                                                                  | Directory name to look at on the tnf repo.
tnf\_labels                             | `"common,telco,extended"`                                                                                                                                                                                                               | (This is the recommended way of selecting/skipping test suites starting from CNF Cert Suite v4.1.0, and the only supported method since tnf v4.3.4) List of [test suites](https://test-network-function.github.io/cnf-certification-test/test-spec/#available-test-specs) that are executed/skipped using labels. In particular, `tnf_labels` content must follow [these guidelines](https://onsi.github.io/ginkgo/#spec-labels), then dci-openshift-app-agent uses this string to run the tnf container with `-l` argument. Note that, when using labels, apart from using the tnf suite names as labels, you can also use, among others, `common` label to refer to all the stable tnf suites, `telco` label to include Telco-related tests (starting in v4.3.0), `extended` to new features added in v4.1.0, and `preflight` to run preflight on tnf. See the [cnf-certification-test README](https://test-network-function.github.io/cnf-certification-test/test-container/#run-the-tests) for more information, and also, check [CATALOG.md](https://github.com/test-network-function/cnf-certification-test/blob/main/CATALOG.md) to see the list of test suites available with the label that corresponds to each of them.
tnf\_suites                             | ""                                                                                                                                                                                                                                      | (WARNING: this option is not supported since tnf v4.3.4. Also, it is not the recommended option to list test suites starting from CNF Cert Suite v4.1.0. Use `tnf_labels` instead) List of [test suites](https://test-network-function.github.io/cnf-certification-test/test-spec/#available-test-specs) that are executed. In particular, `tnf_suites` content must be the list of suites to be run, space separated (can be test suites and/or individual tests), so that dci-openshift-app-agent uses this string list to run the tnf container with `-f` argument. See the [cnf-certification-test README](https://github.com/test-network-function/cnf-certification-test/tree/v4.0.2#run-the-tests) for more information.
tnf\_skip\_suites                       | ""                                                                                                                                                                                                                                      | (WARNING: this option is not supported since tnf v4.3.4. Also, it is not the recommended option to skip test suites starting from CNF Cert Suite v4.1.0. Use `tnf_labels` instead) List of [test suites](https://test-network-function.github.io/cnf-certification-test/test-spec/#available-test-specs) that are skipped (optional). In particular, `tnf_skip_suites` content must be the list of suites to be skipped, space separated (can be test suites and/or individual tests), so that dci-openshift-app-agent uses this string list to run the tnf container with `-s` argument. Remember that this argument is discarded if no `tnf_suites` are provided. See the [cnf-certification-test README](https://github.com/test-network-function/cnf-certification-test/tree/v4.0.2#run-the-tests) for more information.
tnf\_config                             | tnf_config:<br>&nbsp;&nbsp; - namespace: "{{ dci_openshift_app_ns }}"<br>&nbsp;&nbsp; targetpodlabels: []<br>&nbsp;&nbsp; targetoperatorlabels: []<br>&nbsp;&nbsp; target_crds: []<br> &nbsp;&nbsp; exclude_connectivity_regexp: ""<br> | A complex variable to define the configuration to be applied in CNF Cert Suite.<ul> <li> namespace: Target namespace. </li> <li>targetpodlabels: List of autodiscovery labels to be considered by the CNF Cert Suite for pod testing.</li> <li>targetoperatorlabels (mandatory from tnf v4.2.3 if you want to test operators): List of autodiscovery labels to be considered by the CNF Cert Suite for operator testing.</li> <li>target_crds: List of CRDs under test in the targeted namespace.</li> <li>exclude_connectivity_regexp: A regexp to exclude containers from the connectivity test (optional).</li> </ul> See [this](../../samples/tnf_test_example) for more details about an example defining this variable.<br> * Testing multiple resources on different namespaces is supported.
accepted\_kernel\_taints                | []                                                                                                                                                                                                                                      | Allow-list for tainted modules. It must be composed of a list of elements called module: "<module_name>"; e.g.:<br>accepted_kernel_taints:<br>&nbsp;&nbsp; - module: "taint1"<br>&nbsp;&nbsp; - module: "taint2"
tnf\_postrun\_delete\_resources         | true                                                                                                                                                                                                                                    | Control if the deployed resources are kept after the CNF Cert Suite execution for debugging purposes
tnf\_certified\_container\_info         | []                                                                                                                                                                                                                                      | Container images to be tested with [affiliated-certification test suite](https://github.com/test-network-function/cnf-certification-test/blob/main/CATALOG.md#container-is-certified) (you must specify that suite, or at least the test called affiliated-certification-container-is-certified, in tnf\_suite to get them tested). Each item are composed by the following variables: <ul> <li>name (mandatory): Container image name.</li> <li>repository (mandatory): Public registry where the container image is placed.</li> <li>tag (optional, "latest" assumed if empty): Container image tag.</li> <li>digest (optional; if set, it takes precedente over tag): Container image digest.</li></ul> Examples with these four values filled can be seen in the `tnf_config.yml` [file](https://github.com/test-network-function/cnf-certification-test/blob/main/cnf-certification-test/tnf_config.yml) provided in cnf-certification-test repository, within the `certifiedcontainerinfo` variable.
tnf\_env\_vars                          | {}                                                                                                                                                                                                                                      | Environment variables to be provided in a dictionary for tnf execution. Check [the section below](#example-of-tnf_env_vars-variable) for more information.
tnf\_non\_intrusive\_only               | false                                                                                                                                                                                                                                   | If set to true, skip intrusive tests which may disrupt cluster operations. *Note that the recommended way of defining the environment variable is to use `tnf_env_vars` variable defined above.*
tnf\_run\_cfd\_test                     | false                                                                                                                                                                                                                                   | The test suites from [openshift-kni/cnf-feature-deploy](https://github.com/openshift-kni/cnf-features-deploy) will be run prior to the actual CNF certification test execution and the results are incorporated in the same claim. *Note that the recommended way of defining the environment variable is to use `tnf_env_vars` variable defined above.*
tnf\_log\_level                         | "debug"                                                                                                                                                                                                                                 | Log level used to run the CNF Cert Suite. Possible values can be seen [here](https://github.com/test-network-function/cnf-certification-test/tree/v4.0.2#log-level). *Note that the recommended way of defining the environment variable is to use `tnf_env_vars` variable defined above.*
tnf\_use\_legacy\_operator\_label       | false                                                                                                                                                                                                                                   | From tnf v4.2.3, operators can be autodiscovered using custom labels, instead of default `test-network-function.com/operator: target`. If this variable is set to true, these custom labels will be ignored and only the operators with `test-network-function.com/operator: target` label (that are in the selected namespaces in `tnf_config` variable) will be tested. Note this option is deprecated in tnf versions >= v4.2.3.
tnf\_feedback                           | Each entry of the dict is composed by key = tnf test name and value = "". Check [defaults/main.yml file](defaults/main.yml)                                                                                                                                                                                                                                    | From tnf v4.3.3, you can provide feedback to the autogenerated report by tnf. You just need to fill the feedback for the desired tests in this new variable.

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

Until tnf v4.2.3, to test operators with the operator test suite (and also the operator-related test in affiliated-certification test suite), it requires the following label and annotation to be declared in the CSV under test:

* label: `test-network-function.com/operator=target`
* annotation: `test-network-function.com/subscription_name:<SUBSCRIPTION_NAME>`

We had, in fact, a legacy `operators_regexp` attribute that was used to help the introduction of operators to test, but then you needed to add the logic in the hooks to be able to handle that information. It was not really practical, so this attribute has been removed from `tnf_config` (however, it does not affect to configurations that use this attribute, as it was always optional).

But, from tnf v4.2.3 (and in HEAD version), it is allowed to autodiscover operators using custom labels. For this purpose, you can use `targetoperatorlabels` attribute for each `tnf_config` item. Of course this is optional.

Imagine you have an operator labeled as `operator-label=hello` in `test-cnf` namespace. You can autodiscover it by doing the following (just using the first `tnf_config` example showed above for the sake of completeness):

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

## Example of tnf_certified_container_info variable

> This feature is not compatible to CNF Cert Suite versions higher or equal than `v4.5.0`.

This example is based on the content that can be retrieved in the `tnf_config.yml` [file](https://github.com/test-network-function/cnf-certification-test/blob/main/cnf-certification-test/tnf_config.yml) provided in cnf-certification-test repository, within the `certifiedcontainerinfo` variable.

```yaml
---
tnf_certified_container_info:
  - name: rocketchat/rocketchat
    repository: registry.connect.redhat.com
    tag: 0.56.0-1 # optional, "latest" assumed if empty
    digest: # if set, takes precedence over tag. e.g. "sha256:03f7f2499233a302351821d6f78f0e813c3f749258184f4133144558097c57b0"
  - name: rocketchat/rocketchat
    repository: registry.connect.redhat.com
    tag: 0.56.0-1
    digest: sha256:03f7f2499233a302351821d6f78f0e813c3f749258184f4133144558097c57b0
...
```

## Example of tnf_env_vars variable

This variable must be a dictionary, where the key is the tnf environment variable to be used during execution. You have some examples of possible variables to be provided in the [tnf docs](https://test-network-function.github.io/cnf-certification-test/runtime-env) or in the [script](https://github.com/test-network-function/cnf-certification-test/blob/main/script/run-container.sh) used to run the tnf container.

For example, the following configuration defines these four environment variables:

- `TNF_NON_INTRUSIVE_ONLY`: if set to true, skip intrusive tests which may disrupt cluster operations (default `false`).
- `TNF_LOG_LEVEL`: log level used to run the CNF Cert Suite (default `info`).
- `TNF_ALLOW_PREFLIGHT_INSECURE`: (required when running preflight on CNF Cert Suite) if set to true, allow the Preflight execution ran by CNF Cert Suite to access to insecure registries. This should be needed when accessing to private registries. Remember this feature is only valuable for tnf versions from v4.1.6 in advance. Remember also to turn on preflight test suite with `preflight` label.

```yaml
---
tnf_env_vars:
  TNF_NON_INTRUSIVE_ONLY: true
  TNF_LOG_LEVEL: "debug"
  TNF_ALLOW_PREFLIGHT_INSECURE: true
...
```

Note that cnf_cert role appends to `tnf_env_vars` the environment variables called `TNF_PARTNER_REPO` and `TNF_IMAGE`, as they are defined in runtime. So please **do not define** these variables in `tnf_env_vars`; just let cnf_cert role do its job.

Also, take into account that cnf_cert role still maintains backward compatibility with the usage of variables such as `tnf_non_intrusive_only` and `tnf_log_level`, which are related to the environment variables described above. **In case of not overriding `tnf_env_vars` default value (which is `{}`, empty dictionary), the values of these three variables will be used, else these three variables will be ignored.**

## Some reminders when running preflight with CNF Cert Suite

If you want to run preflight on CNF Cert Suite, you need to: 1) use the proper reference to preflight on `tnf_labels`, 2) define `partner_creds` variable, and 3) properly add `TNF_ALLOW_PREFLIGHT_INSECURE` variable to `tnf_env_vars`.

## Note regarding CNF Cert Suite v4.2.3

CNF Cert Suite v4.2.3 introduced some news, as explained in this README file, but also there were some inconsistencies with the support of legacy format of tnf_config.yml file. Having said that, we recommend not to use that version and go directly to the currently latest supported, where these issues are already fixed.

## Visualize the results with HTML results application.

In the job, starting from tnf v4.3.0 in advance, you will see that a new `tar.gz` file is submitted to the Files section in the DCI jobs. Depending on the tnf version, this is called:

  - `tnf-results-web-page.tar.gz`, if using v4.3.0.
  - `<timestamp>-cnf-test-results.tar.gz`, if using v4.3.1 in advance.

If you extract the compressed files in one single place and open `results.html`, you can see a pre-loaded information extracted from `claim.json` file. If you choose the scenario of your case (telco, extended, etc.), you will see, in Results section, the report of the tnf tests with the corresponding results, having also the opportunity of providing feedback to each test.

Starting from tnf v4.3.3, it is also possible to provide feedback with `tnf_feedback` variable. You just need to write the feedback for the tests in which you are interested in, and then DCI will take care of pre-load that information in the HTML report.

In [defaults/main.yml](defaults/main.yml), you have a template that you can use in your pipeline file, so that you can fill the value for the tests you want to provide feedback. You don't need to include the tests that you don't want to provide feedback. To insert line breaks, use `\\n` (you need to escape it, else there can be rendering issues). Same for quotes and so on.

In any case, when you finish filling in the feedback in the report, you can generate a new report with that feedback included, by just selecting the scenario you want to evaluate (non-telco, telco, extended...), and pushing in the "Download Results Feedback" button. The resulting HTML resource should be the document to be provided when submitting CNF Certification.

You can also upload a `claim.json` file obtained from the execution (also available in the Files section of the DCI job) in the form you have at the top, if you want to load a different file. Anyway, the report (starting with v4.3.1) already contains the `claim.json` file.

This is a feature provided by CNF Cert Suite, please check in their documentation for finding more information about this tool.

## About using tnf_labels and tnf_suites/tnf_skip_suites

These two options cannot be mixed when selecting the suites to run in the CNF Cert Suite execution. If you configure `tnf_labels`, you cannot use `tnf_suites` and/or `tnf_skip_suites`, and the opposite; if you configure `tnf_suites` and/or `tnf_skip_suites`, you cannot use `tnf_labels`.

Also, remember that `tnf_labels` is the preferrable way of selecting suites since tnf v4.1.0, and the only way since tnf v4.3.4.
