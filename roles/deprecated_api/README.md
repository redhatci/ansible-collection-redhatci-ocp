# redhatci.ocp.deprecated_api – Detect To-Be-Removed Kubernetes (K8s) APIs

- [Synopsis](https://galaxy.ansible.com/ui/repo/published/redhatci/ocp/content/role/deprecated_api/README.md#synopsis)
- [Requirements](https://galaxy.ansible.com/ui/repo/published/redhatci/ocp/content/role/deprecated_api/README.md#requirements)
- [Parameters](https://galaxy.ansible.com/ui/repo/published/redhatci/ocp/content/role/deprecated_api/README.md#parameters)
- [Examples](https://galaxy.ansible.com/ui/repo/published/redhatci/ocp/content/role/deprecated_api/README.md#examples)
- [Output](https://galaxy.ansible.com/ui/repo/published/redhatci/ocp/content/role/deprecated_api/README.md#output)

# Synopsis

- Connect to a running K8s cluster with an application workload already deployed.
- Utilize the community.kubernetes.k8s_info module to access K8s APIs.
- Parse workload APIs using the APIRequestCount object.
- Detect to-be-removed APIs by filtering through APIRequestCount.status.removedInRelease.
- Verify compatibility with the current Kubernetes version, the next version, and all versions up to the latest release mentioned in removedInRelease.
- Output a map from OpenShift versions to a list of workload APIs to be removed in each version.
- Generate a JUnit file containing the testsuite 'Workload Compatibility with OCP Versions'.


# Requirements

The role requires the following:

- Install `community.kubernetes.k8s_info` to access K8s APIs.
- Ensure the availability of the K8s [APIRequestCount](https://github.com/openshift/cluster-kube-apiserver-operator/blob/master/bindata/assets/kube-apiserver/apiserver.openshift.io_apirequestcount.yaml) object. For OpenShift, APIRequestCount is included in the standard distribution from OCP 4.9 onwards. For other distributions, deploy the required CRD and CR before using the role.
- Python version 3.6 or higher is needed to parse the APIs.


# Parameters

| Parameter               | Choices/Defaults      | Comments                                             |
|-------------------------|-----------------------|------------------------------------------------------|
| `kubeconfig`            | `~/.kube/config.json` | Path to an existing Kubernetes config file to be used by k8s_info dependency. If not provided, the OpenShift client will attempt to load the default configuration file from `~/.kube/config.json`. Can also be specified via `K8S_AUTH_KUBECONFIG` environment variable.                                                                                                |
| `deprecated_namespaces` | `undefined`           | List of namespaces the role will check for deprecated APIs. Typically, it should include the namespaces where you deploy the workload. If left undefined, the role will check all namespaces, excluding those starting with the `openshift` and `kube-` prefixes.                                                |
| `ocp_version`           | `"4.9"/"4.10"/etc`    | OpenShift version currently running on your cluster. |
| `job_logs`              | `undefined`           | Directory to store the output JUnit file containing the 'Workload Compatibility with OCP Versions' testsuite.                                                              |

# Examples

```
- name: Detect to-be-Removed APIs in all namespaces excluding ones starting with openshift and kube-
  include_role:
    name: redhatci.ocp.deprecated_api
  vars:
    ocp_version: "4.9"
    job_logs:
      path: "{{ playbook_dir }}"
```

# Output

The role sets the Ansible fact `ocp_compatibility` - a map from OpenShift versions to a list of workload APIs scheduled for removal in each version. Here is an example:

```
{"ansible_facts": {"ocp_compatibility": {"4.10": "compatible", "4.11": "compatible", "4.12": "podsecuritypolicies.v1beta1.policy", "4.13": "podsecuritypolicies.v1beta1.policy, prioritylevelconfigurations.v1beta1.flowcontrol.apiserver.k8s.io, flowschemas.v1beta1.flowcontrol.apiserver.k8s.io, horizontalpodautoscalers.v2beta2.autoscaling", "4.9": "compatible"}}, "changed": false}
```

The second output is a JUnit file generated in the job_logs folder, which contains the testsuite 'Workload Compatibility with OCP Versions'. Here is an example:

```
$ cat apirequestcounts_ocp_compatibility.xml 
<?xml version="1.0" ?>
<testsuites disabled="0" errors="0" failures="2" tests="5" time="0.0">
	<testsuite disabled="0" errors="0" failures="2" name="Workload Compatibility with OCP Versions" skipped="0" tests="5" time="0">
		<testcase classname="Workload Compatibility with OCP-4.9" name="Check compatibility with OCP-4.9"/>
		<testcase classname="Workload Compatibility with OCP-4.10" name="Check compatibility with OCP-4.10"/>
		<testcase classname="Workload Compatibility with OCP-4.11" name="Check compatibility with OCP-4.11"/>
		<testcase classname="Workload Compatibility with OCP-4.12" name="Check compatibility with OCP-4.12">
			<failure message="Workload uses APIs that are no longer available in OCP-4.12: podsecuritypolicies.v1beta1.policy" type="failure"/>
		</testcase>
		<testcase classname="Workload Compatibility with OCP-4.13" name="Check compatibility with OCP-4.13">
			<failure message="Workload uses APIs that are no longer available in OCP-4.13: podsecuritypolicies.v1beta1.policy, prioritylevelconfigurations.v1beta1.flowcontrol.apiserver.k8s.io, flowschemas.v1beta1.flowcontrol.apiserver.k8s.io, horizontalpodautoscalers.v2beta2.autoscaling" type="failure"/>
		</testcase>
	</testsuite>
</testsuites>
```

# Authors

Tatiana Krishtop (@tkrishtop)
