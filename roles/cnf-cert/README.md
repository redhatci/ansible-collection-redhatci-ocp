# CNF-cert Role

This role encapulates the logic for the [Test Network Function (TNF)](https://github.com/test-network-function/cnf-certification-test). It is responsible for deploying the TNF framework and running the tests in DCI.

Before executing the CNF (Cloud-native network function) Cert Suite, it's important to label the pods to test using the autodiscovery feature. You can do it manually or programatically. An example of this can be found in [tnf_test_example](../../samples/tnf_test_example/README.md).

## Variables

Name                                    | Default                                              | Description
--------------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
tnf\_stage                              | "tests"                                              | Stage to be run when calling the role from outside. Possible values: "tests" (default), "post-run" and "teardown".
test\_network\_function\_repo           | https://github.com/test-network-function/cnf-certification-test | Repository to download the tnf code. However, if we are testing a pull request from cnf-certification-test repo, this variable will be pointing to the file path where the pull request code has been downloaded in the jumphost.
test\_network\_function\_version        | v4.2.2                                               | CNF Cert Suite version downloaded. DCI App Agent supports the latest stable version, which is v4.2.2. HEAD version (in the main branch) can be also used, but it is not guaranteed a complete compatibility with the latest unstable changes. The versions prior to v4.0.0 are not compatible with the agent. Note that, starting from v4.1.6 (also with HEAD branch), tnf will also launch Preflight from CNF Cert Suite (as long as `common` label is selected in `tnf_labels`).
test\_network\_function\_project\_name  | cnf-certification-test                               | Directory name to look at on the tnf repo.
tnf\_suites                             | ""                                                   | (Note that this variable is not the recommended option to list test suites starting from CNF Cert Suite v4.1.0. Use `tnf_labels` instead) List of [test suites](https://test-network-function.github.io/cnf-certification-test/test-spec/#available-test-specs) that are executed. In particular, `tnf_suites` content must be the list of suites to be run, space separated (can be test suites and/or individual tests), so that dci-openshift-app-agent uses this string list to run the tnf container with `-f` argument. See the [cnf-certification-test README](https://github.com/test-network-function/cnf-certification-test/tree/v4.0.2#run-the-tests) for more information.
tnf\_skip\_suites                       | ""                                                   | (Note that this variable is not the recommended option to skip test suites starting from CNF Cert Suite v4.1.0. Use `tnf_labels` instead) List of [test suites](https://test-network-function.github.io/cnf-certification-test/test-spec/#available-test-specs) that are skipped (optional). In particular, `tnf_skip_suites` content must be the list of suites to be skipped, space separated (can be test suites and/or individual tests), so that dci-openshift-app-agent uses this string list to run the tnf container with `-s` argument. Remember that this argument is discarded if no `tnf_suites` are provided. See the [cnf-certification-test README](https://github.com/test-network-function/cnf-certification-test/tree/v4.0.2#run-the-tests) for more information.
tnf\_labels                             | `"platform-alteration,networking,affiliated-certification,lifecycle,access-control,observability,operator,manageability"`                         | (This is the recommended way of selecting/skipping test suites starting from CNF Cert Suite v4.1.0) List of [test suites](https://test-network-function.github.io/cnf-certification-test/test-spec/#available-test-specs) that are executed/skipped using labels. In particular, `tnf_labels` content must follow [these guidelines](https://onsi.github.io/ginkgo/#spec-labels), then dci-openshift-app-agent uses this string to run the tnf container with `-l` argument. Note that, when using labels, apart from using the tnf suite names as labels, you can also use, among others, `common` label to refer to all the stable tnf suites, `extended` to new features added in v4.1.0, and `preflight` to run preflight on tnf. See the [cnf-certification-test README](https://test-network-function.github.io/cnf-certification-test/test-container/#run-the-tests) for more information, and also, check [CATALOG.md](https://github.com/test-network-function/cnf-certification-test/blob/main/CATALOG.md) to see the list of test suites available with the label that corresponds to each of them.
tnf\_config                             | tnf_config:<br>&nbsp;&nbsp; - namespace: "{{ dci_openshift_app_ns }}"<br>&nbsp;&nbsp; targetpodlabels: []<br>&nbsp;&nbsp; target_crds: []<br>&nbsp;&nbsp; operators_regexp: ""<br> &nbsp;&nbsp; exclude_connectivity_regexp: ""<br>                                  | A complex variable to define the configuration to be applied in CNF Cert Suite.<ul> <li> namespace: Target namespace. </li> <li>targetpodlabels: List of autodiscovery labels to be considered by the CNF Cert Suite for pod testing.</li><li>target_crds: List of CRDs under test in the targeted namespace.</li><li> operators_regexp:  A regexp to select operators to be tested by the CNF Cert Suite (optional). </li> <li>exclude_connectivity_regexp: A regexp to exclude containers from the connectivity test (optional).</li> </ul> See [this](../../samples/tnf_test_example/hooks/templates/test_pods.yml.j2) for more details.<br> * Testing multiple resources on different namespaces is supported.
accepted\_kernel\_taints                | []                                                   | Allow-list for tainted modules. It must be composed of a list of elements called module: "<module_name>"; e.g.:<br>accepted_kernel_taints:<br>&nbsp;&nbsp; - module: "taint1"<br>&nbsp;&nbsp; - module: "taint2"
tnf\_postrun\_delete\_resources         | true                                                 | Control if the deployed resources are kept after the CNF Cert Suite execution for debugging purposes
tnf\_certified\_container\_info         | []                                                   | Container images to be tested with [affiliated-certification test suite](https://github.com/test-network-function/cnf-certification-test/blob/main/CATALOG.md#container-is-certified) (you must specify that suite, or at least the test called affiliated-certification-container-is-certified, in tnf\_suite to get them tested). Each item are composed by the following variables: <ul> <li>name (mandatory): Container image name.</li> <li>repository (mandatory): Public registry where the container image is placed.</li> <li>tag (optional, "latest" assumed if empty): Container image tag.</li> <li>digest (optional; if set, it takes precedente over tag): Container image digest.</li></ul> Examples with these four values filled can be seen in the `tnf_config.yml` [file](https://github.com/test-network-function/cnf-certification-test/blob/main/cnf-certification-test/tnf_config.yml) provided in cnf-certification-test repository, within the `certifiedcontainerinfo` variable.
tnf\_env\_vars                          | {}                                                   | Environment variables to be provided in a dictionary for tnf execution. Check [the section below](#example-of-tnf_env_vars-variable) for more information.
tnf\_non\_intrusive\_only               | false                                                | If set to true, skip intrusive tests which may disrupt cluster operations. *Note that the recommended way of defining the environment variable is to use `tnf_env_vars` variable defined above.*
tnf\_run\_cfd\_test                     | false                                                | The test suites from [openshift-kni/cnf-feature-deploy](https://github.com/openshift-kni/cnf-features-deploy) will be run prior to the actual CNF certification test execution and the results are incorporated in the same claim. *Note that the recommended way of defining the environment variable is to use `tnf_env_vars` variable defined above.*
tnf\_log\_level                         | "debug"                                              | Log level used to run the CNF Cert Suite. Possible values can be seen [here](https://github.com/test-network-function/cnf-certification-test/tree/v4.0.2#log-level). *Note that the recommended way of defining the environment variable is to use `tnf_env_vars` variable defined above.*

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

In case of needing it, the code to handle it must be included in the partner's hooks.

Note that, to test operators with the operator test suite, it requires the following label and annotation to be declared in the CSV under test:

* label: `test-network-function.com/operator=target`
* annotation: `test-network-function.com/subscription_name:<SUBSCRIPTION_NAME>`

## Example of tnf_certified_container_info variable

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
- `TNF_ALLOW_PREFLIGHT_INSECURE`: (required when running preflight on CNF Cert Suite) if set to true, allow the Preflight execution ran by CNF Cert Suite to access to insecure registries. This should be needed when accesing to private registries. Remember this feature is only valuable for tnf versions from v4.1.6 in advance.

```yaml
---
tnf_env_vars:
  TNF_NON_INTRUSIVE_ONLY: true
  TNF_LOG_LEVEL: "debug"
  TNF_ALLOW_PREFLIGHT_INSECURE: true
...
```

Note that cnf-cert role appends to `tnf_env_vars` the environment variables called `TNF_PARTNER_REPO` and `TNF_IMAGE`, as they are defined in runtime. So please **do not define** these variables in `tnf_env_vars`; just let cnf-cert role do its job.

Also, take into account that cnf-cert role still maintains backward compatibility with the usage of variables such as `tnf_non_intrusive_only` and `tnf_log_level`, which are related to the environment variables described above. **In case of not overriding `tnf_env_vars` default value (which is `{}`, empty dictionary), the values of these three variables will be used, else these three variables will be ignored.**

## Some reminders when running preflight with CNF Cert Suite

If you want to run preflight on CNF Cert Suite, you need to: 1) use the proper reference to preflight on `tnf_labels`, 2) define `partner_creds` variable, and 3) properly add `TNF_ALLOW_PREFLIGHT_INSECURE` variable to `tnf_env_vars`.
