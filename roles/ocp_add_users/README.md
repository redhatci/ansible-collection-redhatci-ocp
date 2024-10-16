# ocp_add_users role

This role adds users to an OpenShift cluster through htpasswd Identity Provider.

It configures the [htpasswd identity provider](https://docs.redhat.com/en/documentation/openshift_container_platform/4.17/html-single/authentication_and_authorization/index#configuring-htpasswd-identity-provider) to allow new users to login into OpenShift Container Platform with credentials from an htpasswd file.

When users already exist through htpasswd IdP, it will append the new users or replace old users with new password and new role.

See the [Roles](./#Roles) for information about the type of roles used to create users.

## Requirements

Access to a valid kubeconfig file via an `KUBECONFIG` environment variable.

```Shell
export KUBECONFIG=<kubeconfig_path>
```

## Variables

| Variable           | Default    | Required  | Description
| ------------------ | ---------- | --------- | -----------
| oau_config_dir     | undefined  | Yes       | Directory where the credentials will be saved.
| oau_users          | undefined  | Yes       | List of users to create and their associated [role](#roles). See [formatting](#formatting) for details.
| oau_passwd_len     | 15         | No        | Password length.
| oau_secure_log     | true       | No        | Whether or not hide sensitive logs.

## Formatting

The `oau_users` expects a list of users and its [role](#roles) divided by `:`, no spaces, i.e. `<username>:<role>`.
The `username` must include alphanumeric characters or the special character `-`.
The `role` must include only valid roles, see [roles](#roles) for more details.

In this example, three users will be created: `admin`, `basic-user` and `nonadmin`, each user will have a role associated, `admin`, `basic-user`, and `none` respectively.

```yaml
oau_users:
  - admin:admin
  - basic-user:basic-user
  - nonadmin:none
```

## Roles

These are the roles assigned to the users on creation. See [official documentation about the default roles](https://docs.redhat.com/en/documentation/openshift_container_platform/4.17/html/postinstallation_configuration/post-install-preparing-for-users#default-roles_post-install-preparing-for-users)

| Role             | Description
| ---------------- | -----------
| admin            | A project manager. If used in a local binding, an admin has rights to view any resource in the project and modify any resource in the project except for quota.
| basic-user       | A user that can get basic information about projects and users.
| cluster-admin    | A super-user that can perform any action in any project. When bound to a user with a local binding, they have full control over quota and every action on every resource in the project.
| cluster-status   | A user that can get basic cluster status information.
| cluster-reader   | A user that can get or view most of the objects but cannot modify them.
| edit             | A user that can modify most objects in a project but does not have the power to view or modify roles or bindings.
| self-provisioner | A user that can create their own projects.
| view             | A user who cannot make any modifications, but can see most objects in a project. They cannot view or modify roles or bindings.
| none             | No role is assigned.

## Role Outputs

A file with the created accounts is saved in the `oau_config_dir` directory as `ocp_cred.txt`.

## Usage example

- Adding two users

```yaml
- name: Add OCP users
  ansible.builtin.include_role:
    name: redhatci.ocp.ocp_add_user
  vars:
    oau_config_dir: /path/to/some/dir
    oau_users:
      - custom-admin:admin
      - test-user-0:basic-user
      - test-user-1:view
      - nonadmin:none
```
