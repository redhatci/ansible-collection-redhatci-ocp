# Role: deploy_cr

This Ansible role is used to deploy a Kubernetes Custom Resource (CR) to a specified namespace in an OpenShift or Kubernetes cluster.

## Role Variables

| Variable           | Required | Type   | Description                                                                                            
|--------------------|----------|--------|---------------------------------------------------------------------------------------------------------|                           
| dc_api_version     | yes      | str    | The API version of the CR (e.g., `hco.kubevirt.io/v1beta1`).                                            |
| dc_kind            | yes      | str    | The kind of the CR (e.g., `HyperConverged`).                                                            |
| dc_namespace       | no       | str    | The namespace in which the CR should be created. Defaults to `omit`                                     |
| dc_name            | yes      | str    | The name of the CR.                                                                                     |
| dc_spec            | yes      | dict   | The `spec` field of the CR.                                                                             |
| dc_wait_condition  | no       | dict   | Wait condition for the CR to be considered ready. Defaults to `{'type': 'Available', 'status': 'True'}` |
| dc_wait_timeout    | no       | int    | Timeout in seconds to wait for the CR to be ready.                                                      |
| dc_wait_retries    | no       | int    | Number of retries to check CR readiness.                                                                |
| dc_wait_delay      | no       | int    | Delay in seconds between retries.                                                                       |
| dc_wait_for_cr     | no       | bool   | Whether to wait for the CR to be ready. Defaults to `false`.                                            |
| dc_wait_mc_retries | no       | int    | Retries for changes that may trigger MCP updates. Defaults to: 600                                      |
| dc_wait_mc_delay   | no       | int    | Retries for changes that may trigger MCP updates. Defaults to 10                                        |


## Example Playbook

- name: Deploy a HyperConverged custom resource
  hosts: localhost
  gather_facts: false
  vars:
    my_cr:
      api_version: "hco.kubevirt.io/v1beta1"
      kind: "HyperConverged"
      namespace: "openshift-cnv"
      name: "kubevirt-hyperconverged"
      spec:
        infra:
          replicas: 2
      wait_condition:
        type: Available
        status: "True"
      wait_timeout: 600
      wait_retries: 10
      wait_delay: 30
      wait_for_cr: true
  tasks:
    - name: Deploy HyperConverged CR
      ansible.builtin.include_role:
        name: redhatci.ocp.deploy_cr
      vars:
        dc_api_version: "{{ my_cr.api_version }}"
        dc_kind: "{{ my_cr.kind }}"
        dc_namespace: "{{ my_cr.namespace }}"
        dc_name: "{{ my_cr.name }}"
        dc_spec: "{{ my_cr.spec }}"
        dc_wait_condition: "{{ my_cr.wait_condition }}"
        dc_wait_timeout: "{{ my_cr.wait_timeout }}"
        dc_wait_retries: "{{ my_cr.wait_retries }}"
        dc_wait_delay: "{{ my_cr.wait_delay }}"
        dc_wait_for_cr: "{{ my_cr.wait_for_cr }}"

# Deploy a KubeletConfig custom resource

- name: Deploy a KubeletConfig
  hosts: localhost
  gather_facts: false
  vars:
    kubelet_config_cr:
      api_version: "machineconfiguration.openshift.io/v1"
      kind: "KubeletConfig"
      name: "custom-kubelet-config"
      # For cluster-scoped resources, you can omit the namespace or set it to "omit"
      namespace: "omit"
      wait_condition:
        type: Success
        status: "True"
      spec:
        machineConfigPoolSelector:
          matchLabels:
            pools.operator.machineconfiguration.openshift.io/master: ""
        kubeletConfig:
          kubeReserved:
            cpu: "100m"
            memory: "2Gi"
          systemReserved:
            cpu: "1000m"
            memory: "2.5Gi"
  tasks:
    - name: Deploy KubeletConfig CR
      ansible.builtin.include_role:
        name: redhatci.ocp.deploy_cr
      vars:
        dc_api_version: "{{ kubelet_config_cr.api_version }}"
        dc_kind: "{{ kubelet_config_cr.kind }}"
        dc_namespace: "{{ kubelet_config_cr.namespace }}"
        dc_name: "{{ kubelet_config_cr.name }}"
        dc_spec: "{{ kubelet_config_cr.spec }}"
        dc_wait_condition: "{{ kubelet_config_cr.wait_condition }}"
