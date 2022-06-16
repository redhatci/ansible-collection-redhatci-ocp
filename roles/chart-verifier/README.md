# This role is to run the chart-verifier tool

This role is to execute the [chart-verifier](https://github.com/redhat-certification/chart-verifier) tool as part of the DCI App Agent.

## Variables

Name                               | Default                                              | Description
---------------------------------- | ---------------------------------------------------- | -------------------------------------------------------------
kubeconfig\_path                   | undefined                                            | Path to the kubeconfig file
ocp\_version\_full                 | undefined                                            | OCP version
chart\_verifier\_image             | quay.io/redhat-certification/chart-verifier:1.3.0    | Chart Verifier Image
dci\_charts                        | See defaults/main.yml                                | A list of charts with additional parameters to be used during testing. Example:<br><br>dci_charts: <br>&nbsp;&nbsp;&nbsp; -<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; name: "<RELEASE_NAME>"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; chart_file: "http://xyz/chart.tgz" (required) <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; values_file: "http://xyz/values.yaml" (optional) <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; install: true\|false (required). Installs and verify the chart on the the OCP cluster. <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  flags: (optional). [See helm-chart-checks](https://github.com/redhat-certification/chart-verifier/blob/main/docs/helm-chart-checks.md) for available flags.
logs\_dir                          | /tmp                                                | Directory to store the tests results.

### Chart requirements and installation

If installation is enabled for a chart, all the images and other required files must be reachable from the cluster nodes in order to complete the deployment. Other Kubernetes resources not created by the chart should be prepared in advance too.

The chart report will show timeout errors if any of the images or files are not reachable.

In DCI, the namespaces defined and created by {{ dci_openshift_app_ns }} variable can be used to deploy chart. The chart will removed after the test verification is complete.

### Results

Once the test is completed, the results will be stored the job_logs directory. If the tests are executed by DCI, the results will be stored in the DCI job files section.

### Usage from the dci-app-agent

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
dci_charts:
  -
    name: mychart1
    chart_file: http://xyz/pub/projects/mychart1.tgz
    values_file: http://xyz/pub/projects/mychart1.yml
    install: false
  -
    name: mychart2
    chart: http://xyz/pub/projects/mychart2.tgz
    chart_values: http://xyz/pub/projects/mychart2.yml
    install: true
```

### Usage in a DCI Pipeline

See below for an example of how to use the chart-verifier in a DCI pipeline.

* <https://github.com/redhat-certification/chart-verifier/raw/main/pkg/chartverifier/checks/chart-0.1.0-v3.valid.tgz> is a example of a valid chart that can be used for testing purposes.

```yaml
type: cnf
  prev_stages: [ocp-upgrade, ocp]
  ansible_playbook: /usr/share/dci-openshift-app-agent/dci-openshift-app-agent.yml
  ansible_cfg: /var/lib/dci/pipelines/ansible.cfg
  ansible_inventory: /var/lib/dci/inventories/myinventory.yml
  dci_credentials: /etc/dci-openshift-app-agent/dci_credentials.yml
  ansible_extravars:
    dci_cache_dir: /var/lib/dci-pipeline
    dci_config_dir: /var/lib/dci-openshift-app-agent/samples/my_hooks_dir
    provisionhost_registry: "registry:port"
    partner_creds: "/opt/pull-secret.txt"
    do_chart_verifier: true
    chart_verifier_image: quay.io/redhat-certification/chart-verifier:main
    dci_charts:
      -
        name: mychart1
        chart_file: https://github.com/redhat-certification/chart-verifier/raw/main/pkg/chartverifier/checks/chart-0.1.0-v3.valid.tgz
        flags: -S image.repository=registry:port/nginx-unprivileged --set chart-testing.namespace=myns
        install: true
      -
        name: mychart2
        chart_file: http://xyz/chart.tgz
        values_file: http://xyz.yaml/my_values.yaml
        flags: -S image.repository=registry:port/certified_image # Overriding chart values
        install: false
  components: []
  inputs:
    kubeconfig: kubeconfig_path
  success_tag: helm-charts-ok
```
