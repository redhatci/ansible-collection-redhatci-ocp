# oc_setup role

This role allows the setup of additional credentials for a running OCP cluster.
It configures the htpasswd identity provider to allow users to log in to OpenShift Container Platform with credentials from an htpasswd file.
See the [Users](./#Users) for information about the users and its roles created.

## Variables

| Variable                             | Default                     | Required  | Description                                   |
| ------------------------------------ | --------------------------- | --------- | --------------------------------------------- |
| os_config_dir                        | undefined                   | Yes       | Directory where the credentials will be saved |

## Requirements

Access to a valid kubeconfig file via an `KUBECONFIG` environment variable.

```Shell
export KUBECONFIG=<kubeconfig_path>
```

## Users

## Users

These are the users created and the roles associated to them. See [official documentation about the default roles](https://docs.redhat.com/en/documentation/openshift_container_platform/4.17/html/postinstallation_configuration/post-install-preparing-for-users#default-roles_post-install-preparing-for-users)

| Username      | Role          | Description
| ------------- | ------------- | -----------
| admin         | admin         | A project manager. If used in a local binding, an admin has rights to view any resource in the project and modify any resource in the project except for quota.
| basic_user    | basic-user    | A user that can get basic information about projects and users.
| cluster_admin | cluster-admin | A super-user that can perform any action in any project. When bound to a user with a local binding, they have full control over quota and every action on every resource in the project.
| nonadmin      | None          | A user without any role assigned.

# Role Outputs

A file with the created accounts is saved in the `os_config_dir` directory as `ocp_cred.txt`.

