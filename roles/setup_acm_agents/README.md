setup_acm_agents
=========

This role prepares agents on an on-premise inventory (whether bare metal or virtualized) for provisioning. The nodes must be accessible via Virtual Media.

Requirements
------------

* The nodes must be reachable via Virtual Media.
* Access to an OpenShift cluster with ACM and MCE operators
* Access to a valid kubeconfig file available using the `KUBECONFIG` environment variable.
* AgentServiceConfig and Provisioning configured on the host cluster

Role Variables
--------------

The following variables can be set to customize the role behavior:

### Required Variables

| Variable Name                           |  Type     | Required | Default Value                          | Description
| --------------------------------------- | --------- | -------- | -------------------------------------- | --------------
| setup_acm_agents_inventory              | List      | Yes      | []                                     | Inventory of bare metal hosts. It must contain the BMC credentials. See [Usage examples](#usage-examples)
| setup_acm_agents_infraenv_name          | String    | Yes      |                                        | Target the infrastructure environment
| setup_acm_agents_inject_dns             | Boolean   | No       | false                                  | Enables custom DNS injection. Set to true to pass custom DNS configuration; false disables it
| setup_acm_agents_inject_dns_nameserver  | String    | No       |                                        | Specifies the custom DNS server(s) to use when `setup_acm_agent_inject_dns` is set to true
| setup_acm_agents_location_label         | String    | No       | ""                                     | Location label                                                       
| setup_acm_agents_no_log                 | Boolean   | No       | `false`                                | Role's logging configuration

Usage examples
----------------

```yaml
---
- hosts: localhost
  tasks:
    - name: Setup ACM Agents
      include_role:
        name: setup_acm_agents
      vars:
        setup_acm_agents_infraenv_name: <InfraN>
        setup_acm_agent_inventory:
          - name: <server#1>
            address: idrac-virtualmedia://<idrac ip>/redfish/v1/Systems/System.Embedded.1
            bootMACAddress: <MAC address>
            username: <idrac/ilo username>
            password: <idrac/ilo password>
          - name: <server#2>
            address: idrac-virtualmedia://<idrac ip>/redfish/v1/Systems/System.Embedded.1
            bootMACAddress: <MAC address>
            username: <idrac/ilo username>
            password: <idrac/ilo password>
```
