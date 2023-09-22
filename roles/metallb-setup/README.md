# metallb-setup role

This role setups the MetalLB operator in BGP mode. It allows to advertise IPv4/IPv6 service addresses with mutiple BGP peers.

Main role tasks:
  - Validates the required variables are defined.
  - Validates that the MetalLB CustomResources are present.
  - Configures MetalLB resources in BGP mode.
  - Confirms pods are running and BGP peers listed.

NOTE: This role only works on OCP 4.10 and newer.

## Variables

| Variable               | Default        | Type         | Required    | Description                                                              |
| ---------------------- | ---------------|------------- | ----------- | -------------------------------------------------------------------------|
| mlb_setup_name         | undefined      | String       | Yes         | Name of the BGP Instance to setup, could represent a vlan or network name|
| mlb_ipaddr_pool        | undefined      | List         | Yes         | Pool of addresses to advertise, could be a range, a CIDR, IPv4, IPv6     |
| mlb_bgp_peers          | undefined      | List         | Yes         | A list of values to create BGP Peers for MetalLB. See variables below.   |
|   name                 | undefined      | String       | Yes         | Name to identify the BGP Peer                                            |
|   address              | undefined      | IP           | Yes         | IP address of the BGP Peer, IPv4 or IPv6                                 |
|   remote_asn           | undefined      | Int          | Yes         | Autonomous System (AS) of the Remote Peer                                |
|   local_asn            | undefined      | Int          | Yes         | Autonomous System (AS) of the Local setup with MetalLB                   |
| mlb_ipv4_enabled       | true           | Boolean      | No          | By default BGP setup with IPv4 is deployed, hence pools need to be IPv4  |
| mlb_ipv6_enabled       | false          | Boolean      | No          | If IPv6 Pools are defined for BGP, enable this boolean                   |
| mlb_ocp_supported      | >= 4.10        | String       | No          | Only OCP >= 4.10 is supported                                            |
| mlb_namespace          | metallb-system | String       | No          | Default name of the namespace to use to install operator resources       |
| mlb_bfd_profile        | bfd-fastest    | String       | No          | Name of the BFD profile to use for BGP                                   |
| mlb_settings           | ""             | File Path    | No          | An optional yaml file with the variables listed above.                   |

## Role requirements
  - An Openshift cluster with worker nodes using OCP >= 4.10.
  - MetalLB operator already installed.
  - BGP Peers configured and ready to accept connections (A Router or a FFR Instance).
  - BGP Peers should be accessible (Use NMstate at day2 if you need to setup configurations).

## Usage example

This is an example of how to use the metallb role to configure a MetalLB instance.

Passing the variables at role level:
```yaml
- name: "Setup MetalLB Operator"
  include_role:
    name: metallb-setup
  vars:
    mlb_setup_name: vlan123
    mlb_ipaddr_pool:
      - 1.2.3.10-1.2.3.20
      - fdb0:5b21:e84a:55::10-fdb0:5b21:e84a:55::20
    mlb_bgp_peers:
      - name: "switch01-clusterX-vlan123-ipv4"
        address: 192.168.90.2
        remote_asn: 65451
        local_asn: 65452
      - name: "switch01-clusterX-vlan123-ipv6"
        address: fdb0:5b21:e84a:90::2
        remote_asn: 65451
        local_asn: 65452
```

## Validaton

To confirm that the BGP routing is working properly:
1. Create a service that uses MetalLB labels, and use a deployment with for example an HTTP service in port 8080
    ```YAML
    apiVersion: v1
    kind: Service
    metadata:
      name: metallb-vlan123
      annotations:
        metallb.universe.tf/address-pool: svcpool-vlan123
    spec:
      selector:
        app: vlan123
      ports:
        - port: 8080
          targetPort: 8080
          protocol: TCP
      type: LoadBalancer
      loadBalancerIP: 1.2.3.20
    ```
1. From a client that uses the Router as GW (BGP Peer). Launch a request to the Advertised Pool IP.
    ```ShellSession
    $ curl -IL 1.2.3.20:8080
    HTTP/1.1 200 OK
    ```

## Troubleshooting

See [Troubleshooting MetalLB](https://docs.openshift.com/container-platform/4.13/networking/metallb/metallb-troubleshoot-support.html)

1. Confirm that all the pods in the `metallb-system` namespace are running.
    ```ShellSession
    oc -n metallb-system get pods
    ```
1. One liners to get MetalLB setup information.
    ```ShellSession
    oc -n metallb-system exec daemonset/speaker -c frr -- vtysh -c "show bgp summary"
    oc -n metallb-system exec daemonset/speaker -c frr -- vtysh -c "show ip bgp"
    oc -n metallb-system exec daemonset/speaker -c frr -- vtysh -c "show bfd peers"
    oc -n metallb-system exec daemonset/speaker -c frr -- vtysh -c "show running-config"
    ```
1. Commands to get setup information from the BGP Peers (Routers compatible with IOS & NX-OS compatible)
    ```ShellSession
    show ip bgp summary
    show ip bgp
    show ip bgp neighbors < IP >
    show ip bgp peer-group cluster5
    show ip route bgp
    ```

## References

* [MetalLB Operator documentation](https://docs.openshift.com/container-platform/4.13/networking/metallb/about-metallb.html)
