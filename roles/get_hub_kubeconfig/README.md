# Retrieve ACM Hub kubeconfig

Retrieves the ACM Hub cluster kubeconfig from a given secret on the spoke cluster and writes a self-contained kubeconfig file with embedded certificates.

## Requirements

- The `oc` CLI must be installed and in `$PATH`.

## Variables

| Variable                | Default                       | Required | Description                                                               |
| ----------------------- | ----------------------------- | -------- | ------------------------------------------------------------------------- |
| ghk_hub_kubeconfig_path | undefined                     | Yes      | Path to write the resulting hub kubeconfig file                           |
| ghk_namespace           | open-cluster-management-agent | No       | Namespace where the hub kubeconfig secret is stored                       |
| ghk_secret_name         | hub-kubeconfig-secret         | No       | Name of the secret containing the base64-encoded kubeconfig and certs     |

## Examples

Retrieve the ACM Hub kubeconfig and save it to `/tmp/hub.kubeconfig`:

```yaml
- name: Retrieve ACM Hub kubeconfig
  ansible.builtin.include_role:
    name: redhatci.ocp.get_hub_kubeconfig
  vars:
    ghk_hub_kubeconfig_path: /tmp/hub.kubeconfig
```

Retrieve the ACM Hub kubeconfig using a custom namespace and secret name:

```yaml
- name: Retrieve ACM Hub kubeconfig from custom secret
  ansible.builtin.include_role:
    name: redhatci.ocp.get_hub_kubeconfig
  vars:
    ghk_hub_kubeconfig_path: /tmp/hub.kubeconfig
    ghk_namespace: my-acm-namespace
    ghk_secret_name: my-custom-secret
```
