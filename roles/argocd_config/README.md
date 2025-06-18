# argocd_config

A role to configure ArgoCD applications.

## Variables

| Variable                | Default          | Required by        | Description
| ----------------------- | ---------------- | ------------------ | -----------
| ac_project_def          | <sup>1</sup>     | config-project     | The ArgoCD project definition.
| ac_permissions_def      |  <sup>2</sup>    | config-permissions | The ArgoCD permissions definition.
| ac_namespace            | openshift-gitops | config-namespace, config-app-create, config-app-delete, config-app-sync, config-repo   | The namespace where ArgoCD is installed.
| ac_project              | siteconfig-v2    | config-app-create  | The ArgoCD project to use. 
| ac_app_name             | None             | config-app-create, config-app-delete, config-app-sync  | The name of the ArgoCD application to create.
| ac_app_namespace        | None             | config-app-create  | The namespace where the ArgoCD application will be created.
| ac_app_path             | None             | config-app-create  | The path in the Git repository where application is located.
| ac_repo                 | None             | config-app-create  | The Git repository URL for the application.
| ac_repo_branch          | main             | config-app-create  | The branch of the Git repository to use.
| ac_action               | None             | config-app, config-app-create, config-app-delete, config-app-sync  | The action to perform on the ArgoCD application (create, delete, delete-cascade, sync-on, sync-off).
| ac_ssh_key              | None             | config-app-create  | The SSH key to use for accessing the Git repository.
| ac_gh_token             | None             | config-app-create  | The GitHub token to use for accessing the Git repository.
| ac_gh_username          | None             | config-app-create  | The GitHub username to use for accessing the Git repository.

<sup>1</sup> See [defaults](defaults/main.yml) for the default project definition.

<sup>2</sup> See [defaults](defaults/main.yml) for the default permissions definition.

## Usage examples

### Create ArgoCD project

```yaml
- name: Create ArgoCD project
  ansible.builtin.include_role:
    name: redhatci.ocp.argocd_config
    tasks_from: config-project
```

### Create ArgoCD permissions

```yaml
- name: Create ArgoCD permissions
  ansible.builtin.include_role:
    name: redhatci.ocp.argocd_config
    tasks_from: config-permissions
```

### Configure ArgoCD repo

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

### Create ArgoCD Application

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

### Delete ArgoCD Application

```yaml
- name: Delete ArgoCD application
  ansible.builtin.include_role:
    name: redhatci.ocp.argocd_config
    tasks_from: config-app
  vars:
    ac_action: delete
    ac_app_name: my-app
```
