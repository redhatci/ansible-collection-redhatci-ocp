# Helm Chart Verifier role

This role is to execute the [chart-verifier](https://github.com/redhat-certification/chart-verifier) tool as part of the DCI App Agent.

## Variables

Name                               | Default                                           | Required    | Description
---------------------------------- | --------------------------------------------------|------------ | -------------------------------------------------------------
kubeconfig_path                    | undefined                                         | true        | Path to the kubeconfig file
ocp_version_full                   | undefined                                         | true        | OCP version
chart_verifier_image               | quay.io/redhat-certification/chart-verifier:1.3.0 | false       | Chart Verifier Image
dci_charts                         | undefined                                         | true        | A list of charts and its corresponding parameters to be used during testing. See [How to use with DCI](#how-to-use-with-dci) section for more details
logs_dir                           | /tmp                                              | false       | Directory to store the tests results.
github_token_path                  | undefined                                         | true        | GitHub token to be used to push the chart and the results to a repository. Defaults to [openshift-charts/charts](https://github.com/openshift-helm-charts/charts/)
partner_name                       | undefined                                         | true        | Partner name to be used in the pull request title
partner_email                      | undefined                                         | true        | Email address to be used in the pull request
sandbox_repository                 | undefined                                         | false       | Target repository to submit the PRs instead of openshift-helm-charts/charts/

## Helm charts Certification in a nut shell

In order to run the chart-verifier tool and get your helm chart certified the folllwing requisites must be met:

1. A project in [Red Hat Partner Connect](https://connect.redhat.com/) must be created for each chart to be tested.
1. An OWNERS file will be created by a bot in https://github.com/openshift-helm-charts/charts/tree/main/charts/partners/<partner_name>/<chart_name>/OWNERS. Once the project information is complete in the connect site. This may take a bit to complete.
1. The version of the chart and partner used during the tests must match with the values defined in the [Red Hat Partner Connect](https://connect.redhat.com/) project.
1. All the tests assigned to the partner profile must pass and the chart tests sucessfully executed against a running cluster.
1. A pull request will be created to submit the chart and the results to the [openshift-charts/charts](https://github.com/openshift-helm-charts/charts/) repository. If all the automated tests pass, the chart and report will be merged.

* A chart cannot be re-certified, it should be bumped to a new version. If a test needs to be re-run.

For more information about the certification process see the [helm charts documentation](https://github.com/openshift-helm-charts/charts/tree/main/docs) and [the Red Hat connect gitbook](https://redhat-connect.gitbook.io/partner-guide-for-red-hat-openshift-and-container/helm-chart-certification/overview).

## How this role works

This role integrates the chart-verifier as an additionl test suite available in DCI. The purpose is allowing partners to go through the charts certification process or getting familiar with it. The role will go over the list of charts defined in the `dci_charts` variable and run the chart-verifier tool for each of them. If the tests pass, the chart will be pushed to the [openshift-charts/charts](https://github.com/openshift-helm-charts/charts/).

The role supports defining a `sandbox_repository` variable, that will allow to submit the PRs to a different repository that already contains a fork of [openshift-charts/charts](https://github.com/openshift-helm-charts/charts/) repo. This will help partners to implement CI and get prepared with the real certification process.

This role requires a GitHub token that helps with automating the process of creating the pull request, SSH keys management and pushing the assets to the target repository.

The `dci_charts` variable is a list of charts that supports the following parameters:


| Parameter         | Type           | Default           | Description                                         |
|-------------------|----------------|-------------------|-----------------------------------------------------|
| chart_file        | string         | undefined         | Name of the chart to be tested                      |
| flags             | string         | undefined         | Values to be overriden in the chart or setting to be passed to the chart verifier tool. See: [Run helm chart checks](https://github.com/redhat-certification/chart-verifier/blob/main/docs/helm-chart-checks.md#run-helm-chart-checks). This field is optional |
| create_pr         | boolean        | false             | Creates a pull request on the defined repository (sandbox/openshfit-repo).   |
| values_file       | string         | undefined         | File with the values to be overriden in the chart. This field is optional      |
| deploy_chart      | boolean        | true              | Deploys the chart to the cluster. This step is mandatory for the certification |

* Other metadata like the chart name, and the chart version are automatically obtained from the chart's metadata.

And example of how to populate the `dci_charts` variable:

```yaml
dci_charts:
  - chart_file: https://github.com/ansvu/samplechart/releases/download/samplechart-0.1.1/samplechart-0.1.1.tgz
    flags: -S image.repository="registry.dfwt5g.lab:4443/chart/nginx-118"
    create_pr: false
    values_file: https://github.com/ansvu/samplechart/releases/download/samplechart-0.1.1/values.yaml
    deploy_chart: false
```

## Chart requirements and installation

All the images and other required files must be reachable from the cluster nodes to complete the deployment. Other Kubernetes resources not created by the chart should be prepared in advance. The chart report will show timeout errors if any of the images or dependencies are not available. Chart deployment on a cluster can disabled for testing purposes but this check is mandatory for the certification.

In DCI, the project defined by `dci_openshift_app_ns` variable can be used to deploy the charts. The charts will be removed after the verification is complete. If no namespaces is defined, the resources will be deployed in the default project.

The DCI integration of helm-chart-verifier has basic support for charts deployed in disconnected environments, it will identify the images used by the chart and executes the mirroring to the local repository defined as part of the DCI disconnected settings. If the chart allows overriding the registry URL of the images used by the chart, it will be deployed in the target cluster.

Please see the [known issues and limitations](#known-issues-and-limitations) regarding testing in disconnected environments.

## Results in DCI UI

If the tests are executed by DCI, the results will be stored in the DCI job files section. For local tests, the results will be stored in the path defined by `job_logs` variable.

## Using the sandbox environment

Testing without submitting the results to the [openshift-charts/charts](https://github.com/openshift-helm-charts/charts/) repository is possible by setting the `sandbox_respository` variable to a repository with a fork of [openshift-charts/charts](https://github.com/openshift-helm-charts/charts/) already available. The pull request will be done to the this repository. Having the `create_pr` variable set to true will create a pull request against the sandbox or the official openshift repository. Defining create_pr as false will save the test results in the `log_directory` or the DCI file section.

## Chart certificaton and submission to openshift-charts/charts

Partners who want to certify a Helm chart must create the corresponding project in [Red Hat Partner Connect](https://connect.redhat.com/). Please follow the [Partner Connect documentation](https://redhat-connect.gitbook.io/partner-guide-for-red-hat-openshift-and-container/helm-chart-certification/creating-a-helm-chart-certification-project) to create a Helm the project.

The `create_pr` variable is set to true by default for each chart, this will submit the chart to the [openshift-charts/charts](https://github.com/openshift-helm-charts/charts/) repository by creating a pull request if all the tests passed.

Creating the pull request requires the `github_token` variable set and the permissions to fork repositories in your GitHub account. See [creating-a-personal-access-token](https://docs.github.com/es/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) for more information. If the certification process is run by DCI, the token will be automatically provisioned by our dcicertbot account.

Helm Chart verifier defines 3 different test profiles: partner, redhat, and community. The DCI integration will run by default the ["partner"](https://github.com/redhat-certification/chart-verifier/blob/main/docs/helm-chart-checks.md#profiles) profile.

To fully comply with the certification process and test submission, the chart must be deployed on an OCP cluster and pass all the tests. Setting deploy_chart to `false` in the chart definition will skip the results submission. This setting combined with the use of the sandbox environment will allow to get familiar with the process and improve the chart testing before going through the certification process. The test results will be stored in the DCI job files section.

## How to use with DCI

### Usage in the dci-app-agent

An example of how to run the Helm chart verifier tests:

```console
$ dci-openshift-app-agent-ctl -s -- -v \
-e kubeconfig_path=path/to/kubeconfig \
-e ocp_version_full=4.7 \
-e logs_dir=results/ \
-e @helm_config.yml
```

where the config file looks like this:

```yaml
---
partner_name: telcoci
partner_email: telcoci@redhat.com
sandbox_respository: my-repo/charts
dci_charts:
  - chart_file: https://github.com/ansvu/samplechart/releases/download/samplechart-0.1.1/samplechart-0.1.2.tgz
    flags: -S image.repository="registry.dfwt5g.lab:4443/chart/nginx-118"
    create_pr: false
    values_file: https://github.com/ansvu/samplechart/releases/download/samplechart-0.1.1/values.yaml
    deploy_chart: false
  - chart_file: https://github.com/ansvu/samplechart/releases/download/samplechart-0.1.1/samplechart-0.1.2.tgz
    flags: -S image.repository="registry.dfwt5g.lab:4443/chart/nginx-118"
    create_pr: true
    values_file: https://github.com/ansvu/samplechart/releases/download/samplechart-0.1.1/values.yaml
    deploy_chart: false
```

### Usage in a DCI Pipeline

See below for an example of how to use the chart-verifier in a DCI pipeline.

* The file <https://github.com/ansvu/samplechart/releases/download/samplechart-0.1.1/samplechart-0.1.1.tgz> is a example of a valid chart that can be used for testing purposes.

```yaml
---
- name: helm-chart-verifier
  type: cnf
  prev_stages: [ocp-upgrade, ocp]
  ansible_playbook: /usr/share/dci-openshift-app-agent/dci-openshift-app-agent.yml
  ansible_cfg: /var/lib/dci/pipelines/ansible.cfg
  ansible_inventory: /var/lib/dci/inventories/dallas/8nodes/cluster6-post.yml
  dci_credentials: /etc/dci-openshift-app-agent/dci_credentials.yml
  ansible_extravars:
    dci_cache_dir: /var/lib/dci-pipeline
    provisionhost_registry: "registry.dfwt5g.lab:4443"
    partner_creds: "/opt/pull-secret.txt"
    do_chart_verifier: true
    chart_verifier_image: quay.io/redhat-certification/chart-verifier:main
    github_token_path: "/opt/cache/token.txt"
    partner_name: "telcoci at Red Hat"
    partner_email: "telcoci@redhat.com"
    sandbox_repository: betoredhat/charts
    dci_charts:
      - chart_file: https://github.com/ansvu/samplechart/releases/download/samplechart-0.1.1/samplechart-0.1.1.tgz
        flags: -S image.repository="registry.dfwt5g.lab:4443/chart/nginx-118"
        create_pr: false
      - chart_file: https://github.com/ansvu/samplechart/releases/download/samplechart-0.1.1/samplechart-0.1.1.tgz
        create_pr: true
  components: []
  inputs:
    kubeconfig: kubeconfig_path
  success_tag: helm-charts-ok
```

## Known issues and limitations

1. The helm-chart-verifier tool validates the images used in the charts by checking that the repository/image combined values match with the information available in the Red Hat certification datatabase. That limits the testing with DCI in disconnected environments where the registry hosting an already certified image do not match with the registry used to certify the image.

1. At this time there is no suppport to automatically manage certification projects in connect.redhat.com.

1. The pull requests that fail the tests need to be manually deleted by the partner.

1. The integration already supports charts that are already hosted on a reachable web server.
