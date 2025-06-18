# argocd_config

A role to configure ArgoCD applications.

## Variables

| Variable           | Default                         | Required by                                                                                           | Description
| ------------------ | ------------------------------- | ----------------------------------------------------------------------------------------------------- | -----------
| ac_action          | None                            | config-app, config-app-create, config-app-delete, config-app-sync                                     | The action to perform on the ArgoCD application (create, delete, delete-cascade, sync-on, sync-off).
| ac_app_dir_recurse | false                           | config-app-create                                                                                     | Whether to scan a directory recursively for manifests.
| ac_app_name        | None                            | config-app-create, config-app-delete, config-app-sync, wait-for-healthy                               | The name of the ArgoCD application to create.
| ac_app_namespace   | None                            | config-app-create, config-repo                                                                        | The namespace where the ArgoCD application will be created.
| ac_app_path        | None                            | config-app-create                                                                                     | The path in the Git repository where application is located.
| ac_cluster_api     | https://kubernetes.default.svc  | config-project                                                                                        | The OpenShift cluster API URL.
| ac_gh_token        | None                            | config-repo                                                                                           | The GitHub token to use for accessing the Git repository.
| ac_gh_username     | None                            | config-repo                                                                                           | The GitHub username to use for accessing the Git repository.
| ac_hide_secrets    | True                            | config-repo                                                                                           | Whether to hide sensitive information in logs.
| ac_namespace       | openshift-gitops                | config-namespace, config-app-create, config-app-delete, config-app-sync, config-repo, wait-for-healty | The namespace where ArgoCD is installed.
| ac_permissions_def | <sup>2</sup>                    | config-permissions                                                                                    | The ArgoCD permissions definition.
| ac_project_def     | <sup>1</sup>                    | config-project                                                                                        | The ArgoCD project definition.
| ac_project         | project                         | config-app-create                                                                                     | The ArgoCD project to use. 
| ac_repo_branch     | main                            | config-app-create                                                                                     | The branch of the Git repository to use.
| ac_repo            | None                            | config-app-create, config-repo                                                                        | The Git repository URL for the application.
| ac_ssh_key         | None                            | config-app-create, config-repo                                                                        | The SSH key to use for accessing the Git repository.
| ac_wait_retries    | 30                              | wait-for-healthy                                                                                      | The number of retries to wait for the application to become healthy.
| ac_wait_delay      | 10                              | wait-for-healthy                                                                                      | The time to wait between retries for the application to become healthy.

<sup>1</sup> See [defaults](defaults/main.yml) for the default project definition.
<sup>2</sup> See [defaults](defaults/main.yml) for the default permissions definition.

## Usage examples

### Create a Project

```yaml
- name: Create ArgoCD project
  ansible.builtin.include_role:
    name: redhatci.ocp.argocd_config
    tasks_from: config-project
```

### Set Permissions

```yaml
- name: Create ArgoCD permissions
  ansible.builtin.include_role:
    name: redhatci.ocp.argocd_config
    tasks_from: config-permissions
```

### Create Repository

```yaml
- name: Configure ArgoCD repository
  ansible.builtin.include_role:
    name: redhatci.ocp.argocd_config
    tasks_from: config-repo
  vars:
    ac_repo: my-repo-url
    ac_repo_branch: main
    ac_ssh_key: /path/to/ssh/key
```

### Create Application

```yaml
- name: Create ArgoCD application
  ansible.builtin.include_role:
    name: redhatci.ocp.argocd_config
    tasks_from: config-app
  vars:
    ac_action: create
    ac_app_name: my-app
    ac_app_namespace: my-namespace
    ac_app_path: path/to/app
    ac_repo: my-repo-url
    ac_repo_branch: main
```

### Delete Application

```yaml
- name: Delete ArgoCD application
  ansible.builtin.include_role:
    name: redhatci.ocp.argocd_config
    tasks_from: config-app
  vars:
    ac_action: delete
    ac_app_name: my-app
```

### Set Application Sync-off

```yaml
- name: Set ArgoCD application sync-off
  ansible.builtin.include_role:
    name: redhatci.ocp.argocd_config
    tasks_from: config-app
  vars:
    ac_action: sync-off
    ac_app_name: my-app
```

### Wait for Application to be Healthy

```yaml
- name: Wait for ArgoCD application to be healthy
  ansible.builtin.include_role:
    name: redhatci.ocp.argocd_config
    tasks_from: wait-for-healthy
  vars:
    ac_app_name: my-app
    ac_wait_retries: 30
    ac_wait_delay: 10
```
