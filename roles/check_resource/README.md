# check_resource role

Role to wait for the deployment of a given resource.

Supported resources:

- MachineConfigPool
- SriovNetworkNodeState

## Parameters

Name                        | Required  | Default                | Description
--------------------------- |-----------|------------------------|-----------------------------------------------------------------------
resource\_to\_check         | No        | MachineConfigPool      | Name of the resource to check. Possible values: "MachineConfigPool", or "SriovNetworkNodeState".
check\_wait\_retries        | Yes       | Undefined              | Number of times in which the wait task is performed.
check\_wait\_delay          | Yes       | Undefined              | Time spent between wait tasks' iterations.

## Requirements

A running OpenShift cluster with the proper credentials is required, credentials must be passed as by setting the KUBECONFIG environment.

## Example of usage

Confirm that Machine Config Pools are not updating
```
- name: "Wait for updated MCP after applying ICSP"
  include_role:
    name: redhatci.ocp.check_resource
  vars:
    resource_to_check: "MachineConfigPool"
    check_wait_retries: 120
    check_wait_delay: 10
```

Confirming SRIOV node state
```
- name: "Wait for updated MCP after applying ICSP"
  include_role:
    name: redhatci.ocp.check_resource
  vars:
    resource_to_check: "SriovNetworkNodeState"
    check_wait_retries: 120
    check_wait_delay: 10
```
