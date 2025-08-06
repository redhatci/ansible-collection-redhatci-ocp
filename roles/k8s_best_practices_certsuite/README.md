# k8s_best_practices_certsuite role

This role encapsulates the logic for the [Red Hat Best Practices Test Suite for Kubernetes](https://github.com/redhat-best-practices-for-k8s/certsuite, formerly Test Network Function (TNF). It is responsible for deploying the certsuite and running the tests.

Before executing the certsuite, it's important to label the pods to test using the auto-discovery feature. You can do it manually or programmatically. An example of this can be found in [this example from DCI](https://github.com/redhat-cip/dci-openshift-app-agent/blob/master/samples/tnf_test_example/README.md).

## Variables

Name                                    | Default                                                                                                                                                                                                                                 | Description
--------------------------------------- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------
kbpc_check_commit_sha                   | false                                                                                                                                                                                                                                   | Flag that allows to check if the certsuite image used is based on the same commit SHA than the repository cloned in this role.
kbpc_version                            | See [default vars file](defaults/main.yml) for the latest version supported by the agent                                                                                                                                                                                                                           | Certsuite downloaded version. The role supports from v5.5.0 till the latest stable version. HEAD version (in the main branch) can be also used, but it is not guaranteed a complete compatibility with the latest unstable changes.
kbpc_repo_org_name                      | redhat-best-practices-for-k8s                                                                                                                                                                                                           | Repository organization.
kbpc_project_name                       | certsuite                                                                                                                                                                                                                               | Project name. Also, directory name to look at on the certsuite repo.
kbpc_repository                         | "https://github.com/{{ kbpc_repo_org_name }}/{{ kbpc_project_name }}"                                                                                                                                                                                                                                       | Repository to download the certsuite code.
kbpc_test_labels                        | `"all"`                                                                                                                                                                                                                                 | List of [test suites](https://redhat-best-practices-for-k8s.github.io/certsuite/test-spec/#available-test-specs) that are executed/skipped using labels. In particular, `kbpc_test_labels` content must follow [these guidelines](https://onsi.github.io/ginkgo/#spec-labels), then the role uses this string to run the certsuite container with `-l` argument. Note that, when using labels, apart from using the test suite names as labels, you can also use, among others, `common` label to refer to non-Telco test suites, `telco` label to include Telco-related tests, `extended` to other Verizon-related tests, `faredge` to Far-Edge tests, and `preflight` to run preflight on certsuite. With `all`, you will execute all suites. See the [certsuite README](https://redhat-best-practices-for-k8s.github.io/certsuite/test-run/#test-labels) for more information, and also, check [CATALOG.md](https://github.com/redhat-best-practices-for-k8s/certsuite/blob/main/CATALOG.md) to see the list of test suites available with the label that corresponds to each of them.
kbpc_test_config                        | kbpc_test_config:<br>&nbsp;&nbsp; - namespace: ""<br>&nbsp;&nbsp; targetpodlabels: []<br>&nbsp;&nbsp; targetoperatorlabels: []<br>&nbsp;&nbsp; target_crds: []<br> &nbsp;&nbsp; exclude_connectivity_regexp: ""<br> | A complex variable to define the configuration to be applied in the certsuite.<ul> <li> namespace: Target namespace. </li> <li>targetpodlabels: List of autodiscovery labels to be considered by the certsuite for pod testing.</li> <li>targetoperatorlabels: List of auto-discovery labels to be considered by the certsuite for operator testing.</li> <li>target_crds: List of CRDs under test in the targeted namespace.</li> <li>exclude_connectivity_regexp: A regexp to exclude containers from the connectivity test (optional).</li> </ul> See [this](https://github.com/redhat-cip/dci-openshift-app-agent/blob/master/samples/tnf_test_example/README.md) for more details about an example defining this variable.<br> * Testing multiple resources on different namespaces is supported.
kbpc_accepted_kernel_taints             | []                                                                                                                                                                                                                                      | Allow-list for tainted modules. It must be composed of a list of elements called module: "<module_name>"; e.g.:<br>kbpc_accepted_kernel_taints:<br>&nbsp;&nbsp; - module: "taint1"<br>&nbsp;&nbsp; - module: "taint2"
kbpc_services_ignore_list               | []                                                                                                                                                                                                                                      | Ignore list for services under test. This allows certsuite execution to skip these services for some specific unit tests, such as checking dual-stack configuration, among others.
kbpc_allow_preflight_insecure           | false                                                                                                                                                                                                                                   | (Required when running preflight on certsuite) if set to true, allow the Preflight execution ran by certsute to access to insecure registries. This should be needed when accessing to private registries. Remember also to turn on preflight test suite with `preflight` label.
kbpc_enable_xml_creation                | true                                                                                                                                                                                                                                    | Enable the creation of JUnit file. If this is not set to true, JUnit file will not be created.
kbpc_intrusive                          | true                                                                                                                                                                                                                                    | If set to false, skip intrusive tests which may disrupt cluster operations (default `true`).
kbpc_log_level                          | info                                                                                                                                                                                                                                    | Log level used to run the certsuite (default `info`).
kbpc_postrun_delete_resources           | true                                                                                                                                                                                                                                    | Control if the deployed resources are kept after the certsuite execution for debugging purposes
kbpc_pullsecret                         | ""                                                                                                                                                                                                                                      | Pullsecret for mirroring images used in this role to a local registry. Useful in disconnected environments.
kbpc_registry                           | ""                                                                                                                                                                                                                                      | Registry for mirroring images used in this role. Useful in disconnected environments.
kbpc_partner_creds                      | ""                                                                                                                                                                                                                                      | Authfile with registries' creds. Needed for launching preflight with certsuite. [In this link](https://man.archlinux.org/man/community/containers-common/containers-auth.json.5.en#FORMAT), there are examples about how the files should be formatted.
kbpc_feedback                           | Each entry of the dict is composed by key = certsuite test name and value = "". Check [defaults/main.yml file](defaults/main.yml)                                                                                                                                                                                                                                    | You can provide feedback to the auto-generated report by certsuite. You just need to fill the feedback for the desired tests in this new variable.
kbpc_image_name                         | certsuite                                                                                                                                                                                                                               | Certification test suite image to be downloaded from Quay.io.
kbpc_image_suffix                       | (random string with 16 characters)                                                                                                                                                                                                                             | Suffix to append to the custom certsuite image created in this role, to avoid issues when running executions in parallel in the same server.
kbpc_support_image_name                 | certsuite-probe                                                                                                                                                                                                                         | Certification probe image to be downloaded from Quay.io.
kbpc_kubeconfig                         | undefined                                                                                                                                                                                                                               | Cluster kubeconfig. This variable is required to run the certification tests.
kbpc_log_path                           | undefined                                                                                                                                                                                                                               | Path to a directory where logs are saved. This is mainly used for using this role with DCI to submit log results to the DCI job.
kbpc_code_src_dir                       | undefined                                                                                                                                                                                                                               | If testing a certsuite PR, this variable will be injected from test-runner scripts (used in dci-pipeline and dci-openshift-agent projects) to refer to the file path where the code from the PR is placed in the jumphost, so that it can be used in this role to build a new certsuite container image based on that code.
kbpc_cwe_apikey_path                    | /opt/cache/cwe-apikey.txt                                                                                                                                                                                                                                     | Path to the file containing CWE Hydra API key. It must be generated in Connect UI and saved in this file beforehand.
kbpc_cwe_project_id                     | undefined                                                                                                                                                                                                                               | Best Practices CNF project ID in Connect UI. Must be retrieved from Connect UI or from the DCI job that created the CNF project.
kbpc_partner_name                       |  ""                                                                                                                                                                                                                                      | Partner name used for feeding the collector DB when submitting a result. This is optional.
kbpc_collector_app_password             |  ""                                                                                                                                                                                                                                      | Password used for feeding the collector DB when submitting a result. This is optional.

## How to call the role

Basic call would be the following, assuming you provide proper values to the variables defined above. You mainly need to provide the kubeconfig and the folder to save logs in case you run this with DCI.

```yaml
- name: "k8s_best_practices_certsuite tests"
  include_role:
    name: redhatci.ocp.k8s_best_practices_certsuite
  vars:
    kbpc_kubeconfig: "/path/to/kubeconfig"
    kbpc_log_path: "/path/to/log/folder"
```

## Example of a kbpc_test_config variable to test pods deployed on multiple namespaces not using label prefixes

The format of the targetpodlabels list has the following format: <label_name>=<label_value>

```yaml
---
kbpc_test_config:
  - namespace: "test-cnf"
    targetpodlabels: [environment=test]
    exclude_connectivity_regexp: ""
  - namespace: "production-cnf"
    targetpodlabels: [environment=production]
    exclude_connectivity_regexp: ""
...
```

## Example of a kbpc_test_config variable to test pods deployed on multiple namespaces using label prefixes

The format of the targetpodlabels list has the following format: <label_prefix>/<label_name>=<label_value>

```yaml
---
kbpc_test_config:
  - namespace: "test-cnf"
    targetpodlabels: [test-network-function.com/environment=test]
    exclude_connectivity_regexp: ""
  - namespace: "production-cnf"
    targetpodlabels: [test-network-function.com/environment=production]
    exclude_connectivity_regexp: ""
...
```

## How to test operators?

It is allowed to auto-discover operators using custom labels. For this purpose, you can use `targetoperatorlabels` attribute for each `kbpc_test_config` item. Of course this is optional.

Imagine you have an operator labeled as `operator-label=hello` in `test-cnf` namespace. You can auto-discover it by doing the following (just using the first `kbpc_test_config` example showed above for the sake of completeness):

```yaml
---
kbpc_test_config:
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
kbpc_test_config:
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

## Some reminders when running preflight

If you want to run preflight on certsuite, you need to: 1) use `preflight` label on `kbpc_test_labels`, 2) define `kbpc_partner_creds` variable, and 3) properly set `kbpc_allow_preflight_insecure` var to `true`

## Visualize the results with HTML results application using DCI

In the job, you will see that a new `tar.gz` file is submitted to the Files section in the DCI jobs. This is called `<timestamp>-cnf-test-results.tar.gz`.

If you extract the compressed files in one single place and open `results.html`, you can see a pre-loaded information extracted from `claim.json` file. If you choose the scenario of your case (telco, extended, etc.), you will see, in Results section, the report of the certsuite tests with the corresponding results, having also the opportunity of providing feedback to each test.

It is also possible to provide feedback with `kbpc_feedback` variable. You just need to write the feedback for the tests in which you are interested in, and then DCI will take care of pre-load that information in the HTML report.

In [defaults/main.yml](defaults/main.yml), you have a template that you can use in your pipeline file, so that you can fill the value for the tests you want to provide feedback. You don't need to include the tests that you don't want to provide feedback. To insert line breaks, use `\\n` (you need to escape it, else there can be rendering issues). Same for quotes and so on.

In any case, when you finish filling in the feedback in the report, you can generate a new report with that feedback included, by just selecting the scenario you want to evaluate (non-telco, telco, extended...), and pushing in the "Download Results Feedback" button. The resulting HTML resource should be the document to be provided when submitting CNF Certification.

You can also upload a `claim.json` file obtained from the execution (also available in the Files section of the DCI job) in the form you have at the top, if you want to load a different file. Anyway, the report already contains the `claim.json` file.

This is a feature provided by certsuite, please check in their documentation for finding more information about this tool.

## Upload Certsuite results to your CNF project

It is possible to automatically upload the tar.gz results files directly to the Red Hat Connect API if you have a valid API Key and Project ID. For this to work, you need to configure these two variables with proper values:

- `kbpc_cwe_apikey_path`: path to CWE Hydra API key, generated beforehand on https://rhcert.connect.redhat.com/#/token by using your Red Hat account. The key will be only visible once it's created. After that moment, you will not be able to see it again, so please save the key value it when you create it.
- `kbpc_cwe_project_id`: CNF Certification project ID that is provided once you create it. You can create the CNF Certification project beforehand, or create it with [dci-openshift-app-agent](https://github.com/redhat-cip/dci-openshift-app-agent) in the same job that runs Certsuite execution, as long as you define the `cnf_to_certify` variable that allows the job to call to [openshift_cnf role](../openshift_cnf/README.md). In the docs of that role, you can find what's the format to define the `cnf_to_certify` variable.

You can check what is the related rhcert case to your project ID by sending this request:

```
$ curl --location 'https://access.redhat.com/hydra/cwe/rest/v1.0/projects/certifications' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--header 'x-api-key: <your API key>' \
--data '{"projectId": "<your projectId>"}'

# result: check rhcertUrl to access to the rhcert case assigned to your projectId
```

If these conditions are met, Certsuite will try to upload the results using the CWE Hydra API. If it works, you will see the following logs in Certsuite execution:

```
[INFO] [Feb 13 09:49:14.886] [certsuite.go: 233] Sending results to Red Hat Connect API for project ID <projectId>
[INFO] [Feb 13 09:49:14.886] [archiver.go: 45] Compressing results artifacts into /usr/certsuite/results/<date>-cnf-test-results.tar.gz
[DEBUG] [Feb 13 09:49:14.886] [archiver.go: 59] Zipping file /usr/certsuite/results/claim.json
[DEBUG] [Feb 13 09:49:15.306] [archiver.go: 59] Zipping file /usr/certsuite/results/claimjson.js
[DEBUG] [Feb 13 09:49:15.714] [archiver.go: 59] Zipping file /usr/certsuite/results/results.html
[DEBUG] [Feb 13 09:49:15.715] [archiver.go: 59] Zipping file /usr/certsuite/results/certsuite.log
[DEBUG] [Feb 13 09:49:15.719] [certsuite.go: 249] Get CertificationID from the Red Hat Connect API
[INFO] [Feb 13 09:49:15.719] [rhconnect.go: 47] Getting certification ID from Red Hat Connect API
[DEBUG] [Feb 13 09:49:15.719] [rhconnect.go: 71] Request Body: {{ "projectId": "<projectId>" }}
[DEBUG] [Feb 13 09:49:15.719] [rhconnect.go: 79] Sending request to https://access.redhat.com/hydra/cwe/rest/v1.0/projects/certifications
[DEBUG] [Feb 13 09:49:15.719] [rhconnect.go: 206] Sending request to https://access.redhat.com/hydra/cwe/rest/v1.0/projects/certifications
[INFO] [Feb 13 09:49:16.697] [rhconnect.go: 96] Certification ID retrieved from the API: <certificationId>
[DEBUG] [Feb 13 09:49:16.697] [certsuite.go: 264] Sending ZIP file /usr/certsuite/results/<date>-cnf-test-results.tar.gz to Red Hat Connect
[INFO] [Feb 13 09:49:16.697] [rhconnect.go: 119] Sending results to Red Hat Connect
[DEBUG] [Feb 13 09:49:16.697] [rhconnect.go: 133] Creating form file for /usr/certsuite/results/<date>-cnf-test-results.tar.gz
[DEBUG] [Feb 13 09:49:16.707] [rhconnect.go: 206] Sending request to https://access.redhat.com/hydra/cwe/rest/v1.0/attachments/upload
[INFO] [Feb 13 09:49:28.263] [rhconnect.go: 199] Download URL: https://access.redhat.com/hydra/cwe/rest/v1.0/certifications/<certificationId>/attachments/<fileUuid>/download
[INFO] [Feb 13 09:49:28.263] [rhconnect.go: 200] Upload Date: 2025-02-13 09:49:18.637 +0000 UTC
[INFO] [Feb 13 09:49:28.263] [certsuite.go: 275] Results successfully sent to Red Hat Connect with CertificationID <certificationId>
```

With all this, you will be able to see the tar.gz file generated by Certsuite on the rhcert case.

If the submission doesn't work, the Certsuite execution logs will show you the error and the Ansible task that launches the Certsuite execution will report a failure.

Note that the partner feedback is not included in this automatic submission. This must be generated and submitted afterwards to the rhcert case on a manual way.

