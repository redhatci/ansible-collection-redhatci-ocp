# oc_setup role

This role allows the setup of additional credentials for a running OCP cluster.
It configures the htpasswd identity provider to allow users to log in to OpenShift Container Platform with credentials from an htpasswd file.
It creates three accounts with different role each: `nonadmin`, `admin`, and `cluster_admin`.
It also allows to set SSH Public Keys at day2 to SSH the cluster nodes.

## Variables

| Variable                             | Default                     | Required  | Description                                                             |
| ------------------------------------ | --------------------------- | --------- | ----------------------------------------------------------------------- |
| os_config_dir                        | undefined                   | Yes       | Directory where the credentials will be saved                           |
| oc_ssh_extra_keys_paths              | undefined                   | No        | List of paths where SSH keys are located in the ansible controller node |


## Requirements

- Access to a valid kubeconfig file via an `KUBECONFIG` environment variable.
- `check_resource` role from ansible-collection-redhatci-ocp.

```Shell
export KUBECONFIG=<kubeconfig_path>
```

# Role Outputs

A file with the created accounts is saved in the `os_config_dir` directory as `ocp_cred.txt`.


# Example of how to pass SSH public Keys

```Shell
oc_ssh_extra_keys_paths:
  - ~/.ssh/id_rsa.pub
  - ~/.ssh/id_ed25519.pub
```
