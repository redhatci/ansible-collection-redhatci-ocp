# Insert DNS Records roles

Setups `dnsmasq` (either directly or via `NetworkManager`) inserting the DNS A records required for OpenShift install.

## Role Variables

| Variable              | Required | Default        | Options                 | Comments                                                    |
| --------------------- | -------- | -------------- | ----------------------- | ----------------------------------------------------------- |
| domain                | yes      |                |                         | base for the DNS entries                                    |
| dns_entries_file_name | no       | domains.dns    |                         |                                                             |
| dns_service_name      | no       | NetworkManager | NetworkManager, dnsmasq | the name of the service you want to manage your DNS records |
| node_dns_records      | no       |                |                         | dns records for the nodes of the OpenShift cluster          |
| extra_dns_records     | no       |                |                         | used to defined dns records which are excess of the         |

The structure of `node_dns_records` and `extra_dns_records` is the same and as follows:

```yaml
node_dns_records:
  master-0:
    address: "<node.cluster.domain>"
    ip: "<ip>"
extra_dns_records:
  place-0:
    name: "place-0"
    address: "<address>"
    ip: "<ip>"
    use_dhcp: false
```

## Example Playbook

```yaml
- name: Setup DNS Records
  hosts: dns_host
  roles:
    - insert_dns_records
  vars:
    domain: "cluster.example.com"
    node_dns_records:
      master-0:
        name: "master-0"
        address: "master-0.cluster.example.com"
        ip: "111.111.111.111"
        use_dhcp: false
      master-1:
        name: "master-1"
        address: "master-1.cluster.example.com"
        ip: "111.111.111.112"
        use_dhcp: false
      master-2:
        name: "master-2"
        address: "master-2.cluster.example.com"
        ip: "111.111.111.113"
        use_dhcp: false
```
