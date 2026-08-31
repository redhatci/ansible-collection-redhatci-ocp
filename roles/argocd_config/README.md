# argocd_config

A role to manage ArgoCD projects, repositories and applications.

## Variables

| Variable           | Default                                                           | Required by                                      | Description
| ------------------ | -------                                                           | -----------                                      | -----------
| ac_cluster_role    | openshift-gitops-{{ ac_namespace }}-argocd-application-controller | config-permissions                               | ClusterRole to bind to the ArgoCD application controller. The default follows the operator-generated naming pattern `<argocd_name>-<argocd_namespace>-argocd-application-controller`, and comes from [GitOps ZTP Reference CR](https://docs.redhat.com/en/documentation/openshift_container_platform/4.22/html/scalability_and_performance/telco-hub-ref-design-specs#gitops-ztp-crs_telco-hub).
| ac_action          | None                                                              | config-app                                       | The action to perform on the ArgoCD application (create, delete, delete-cascade, sync-on, sync-off).
| ac_app_dir_recurse | false                                                             | config-app-create                                | Whether to scan a directory recursively for manifests.
| ac_app_name        | None                                                              | config-app-create, wait-for-healthy              | The name of the ArgoCD application to create.
| ac_app_namespace   | None                                                              | config-app-create, config-project, config-repo   | The namespace where the ArgoCD application will be created.
| ac_app_path        | None                                                              | config-app-create                                | The path in the Git repository where application is located.
| ac_server_api      | https://kubernetes.default.svc                                    | config-project                                   | The OpenShift server API URL, where ArgoCD will interact with.
| ac_scm_token       | None                                                              | config-repo                                      | The token to use for accessing the Git repository.
| ac_scm_username    | None                                                              | config-repo                                      | The username to use for accessing the Git repository.
| ac_hide_secrets    | True                                                              | config-repo                                      | Whether to hide sensitive information in logs.
| ac_namespace       | openshift-gitops                                                  | config-app-create, config-repo, wait-for-healthy | The namespace where ArgoCD is installed.
| ac_permissions_def | <sup>1</sup>                                                      | config-permissions                               | The ArgoCD permissions definition.
| ac_project_def     | <sup>2</sup>                                                      | config-project                                   | The ArgoCD project definition. Default scopes to `ac_app_namespace`, `ac_server_api`, and `ac_repo`.
| ac_project         | project                                                           | config-app-create                                | The ArgoCD project to use.
| ac_repo_revision   | main                                                              | config-app-create                                | The branch or commit hash of the Git repository to use.
| ac_repo            | None                                                              | config-app-create, config-project, config-repo   | The Git repository URL for the application. For SSH repositories, don't include the scheme or port. See ac_ssh_port.
| ac_ssh_key         | None                                                              | config-app-create, config-repo                   | The SSH key to use for accessing the Git repository.
| ac_ssh_port        | 22                                                                | config-repo                                      | The SSH port to use for the repository connection.
| ac_wait_retries    | 30                                                                | wait-for-healthy                                 | The number of retries to wait for the application to become healthy.
| ac_wait_delay      | 10                                                                | wait-for-healthy                                 | The time to wait between retries for the application to become healthy.

<sup>1</sup> See [defaults](defaults/main.yml) for the default permissions definition.

<sup>2</sup> See [defaults](defaults/main.yml) for the default project definition.

> [!IMPORTANT]
> When using a custom port, do not include it in the `ac_repo`, it will be added
> automatically through the role.
> Example:
>   ac_repo: git@git.example.com:org/repo.git
>   ac_ssh_port: 1234
>   becomes: ssh://git@git.example.com:1234/org/repo.git

## Usage examples

### Create a Project

```yaml
- name: Create ArgoCD project
  ansible.builtin.include_role:
    name: redhatci.ocp.argocd_config
    tasks_from: config-project
  vars:
    ac_app_namespace: my-namespace
    ac_repo: git@git.example.com/org/repo.git
```

> [!NOTE]
> The default `ac_project_def` scopes the project to `ac_app_namespace`,
> `ac_server_api`, and `ac_repo`, so those must be provided unless you
> supply a custom `ac_project_def`. Override `ac_project_def` when the
> application needs extra cluster-scoped kinds, destinations, or source
> repositories. Setting `ac_project_def` replaces the entire AppProject
> spec; copy the default and extend it.

### Create a custom Project

```yaml
- name: Create a custom ArgoCD project
  ansible.builtin.include_role:
    name: redhatci.ocp.argocd_config
    tasks_from: config-project
  vars:
    ac_app_namespace: my-namespace
    ac_repo: git@git.example.com/org/repo.git
    ac_project_def:
      apiVersion: argoproj.io/v1alpha1
      kind: AppProject
      metadata:
        name: "{{ ac_project }}"
        namespace: "{{ ac_namespace }}"
      spec:
        clusterResourceWhitelist:
          - group: ''
            kind: Namespace
          - group: rbac.authorization.k8s.io
            kind: ClusterRole
          - group: rbac.authorization.k8s.io
            kind: ClusterRoleBinding
          - group: storage.k8s.io
            kind: StorageClass
        namespaceResourceWhitelist:
          - group: '*'
            kind: '*'
        destinations:
          - namespace: "{{ ac_app_namespace }}"
            server: "{{ ac_server_api }}"
        sourceRepos:
          - "{{ ac_repo }}"
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
    ac_repo: git@git.example.com/org/repo.git
    ac_repo_revision: main
    ac_ssh_key: /path/to/ssh/key
    ac_ssh_port: 2222
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
    ac_repo: git@git.example.com/org/repo.git
    ac_repo_revision: main
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
