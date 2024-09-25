# oc_setup role

This role allows the setup of additional credentials for a running OCP cluster.
It configures the htpasswd identity provider to allow users to log in to OpenShift Container Platform with credentials from an htpasswd file.
It creates three accounts with different role each: `nonadmin`, `admin`, and `cluster_admin`.

## Variables

| Variable                             | Default                     | Required  | Description                                   |
| ------------------------------------ | --------------------------- | --------- | --------------------------------------------- |
| os_config_dir                        | undefined                   | Yes       | Directory where the credentials will be saved |


## Requirements

Access to a valid kubeconfig file via an `KUBECONFIG` environment variable.

```Shell
export KUBECONFIG=<kubeconfig_path>
```

# Role Outputs

A file with the created accounts is saved in the `os_config_dir` directory as `ocp_cred.txt`.

