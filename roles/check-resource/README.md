# check-resource role

Role to wait for the deployment of a given resource; applying workarounds based on the `dci_workaround` list for the case of `MachineConfigPool` resources.

Supported resources:

- MachineConfigPool
- SriovNetworkNodeState

## Parameters

Name                        | Required  | Default                | Description
--------------------------- |-----------|------------------------|-----------------------------------------------------------------------
resource\_to\_check         | Yes       | MachineConfigPool      | Name of the resource to check. Possible values: "MachineConfigPool", or "SriovNetworkNodeState".
check\_wait\_retries        | Yes       | Undefined              | Number of times in which the wait task is performed.
check\_wait\_delay          | Yes       | Undefined              | Time spent between wait tasks' iterations.
check\_reason               | No        | Undefined              | Reason for the check to be done.
