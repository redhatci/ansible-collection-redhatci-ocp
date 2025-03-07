# setup_gitea role

This role allows the deployment of [Gitea](https://gitea.com/). Gitea is:

[*"a painless, self-hosted, all-in-one software development service. It includes Git hosting, code review, team collaboration, package registry, and CI/CD. It is similar to GitHub, Bitbucket and GitLab."*](https://docs.gitea.com/)

Role tasks:
  - Validates requirements.
  - Creates a Gitea deployment.
  - Creates a route to the Gitea web console.
  - Initializes Gitea along with a default user.
  - Creates the default repository.
  - Mirrors an existing repository into the Gitea instance if it is defined.

## Variables

| Variable              | Default                               | Required | Description
| --------              | -------                               | -------- | -----------
| sg_action             | install                               | No       | Default role's action
| sg_gitea_image        | docker.io/gitea/gitea:latest-rootless | No       | Default Gitea server image
| sg_kubeconfig         | *undefined*                           | No       | Path to the OCP cluster's kubeconfig file
| sg_namespace          | gitea                                 | No       | Deployment Namespace
| sg_url                | http://localhost:3000                 | No       | Root URL to the Gitea service
| sg_username           | *undefined*                           | No       | Gitea's initial username. Mandatory if the initial repository (sg_repository) is created.
| sg_password           | *undefined*                           | No       | Gitea's initial password. Mandatory if the initial user (sg_username) is created.
| sg_email              | *undefined*                           | No       | E-mail address for the initial user. Mandatory if the initial user (sg_username) is created.
| sg_repository         | *undefined*                           | No       | Initial repository name. Mandatory if an external repository to mirror (sg_repo_mirror_url) is set.
| sg_repo_branch        | main                                  | No       | Main branch in the initial repository
| sg_repo_mirror_url    | *undefined*                           | No       | Git URL to mirror into the initial repository
| sg_repo_mirror_branch | main                                  | No       | Branch to mirror from the repository
| sg_repo_sshkey        | *undefined*                           | No       | The sshkey to clone the initial repository when the repo requires ssh authentication.

## Role requirements
  - The Ansible control node must have access to the registry where the `sg_gitea_image` is stored.
  - Likewise, it must have access to the Git repository to be mirrored into Gitea.

## Usage example

See below for some examples of how to use the setup_gitea role to deploy and setup a Gitea service.

Create an empty Gitea deployment:
```yaml
- name: "Setup Gitea deployment"
  ansible.builtin.include_role:
    name: redhatci.ocp.setup_gitea
```

Create a Gitea deployment with an initial user:
```yaml
- name: "Setup Gitea deployment"
  ansible.builtin.include_role:
    name: redhatci.ocp.setup_gitea
  vars:
    sg_username: gitea
    sg_password: Gi_Tea_1234
    sg_username: gitea@example.com
```

Create a Gitea deployment with an initial repository:
```yaml
- name: "Setup Gitea deployment"
  ansible.builtin.include_role:
    name: redhatci.ocp.setup_gitea
  vars:
    sg_username: gitea
    sg_password: Gi_Tea_1234
    sg_username: gitea@example.com
    sg_repository: gitea-repo
```

Create a Gitea deployment and mirror an external repository:
```yaml
- name: "Setup Gitea deployment"
  ansible.builtin.include_role:
    name: redhatci.ocp.setup_gitea
  vars:
    sg_username: gitea
    sg_password: Gi_Tea_1234
    sg_username: gitea@example.com
    sg_repository: gitea-repo
    sg_repo_mirror_url: git@gitea.com:gitea/gitea-repo.git
```

Remove resources created by the role.
```yaml
- name: "Remove the Gitea deployment"
  ansible.builtin.include_role:
    name: redhatci.ocp.setup_gitea
  vars:
    sg_action: cleanup
```

# Access Gitea

See below how to access the Gitea web console:

## From other namespaces
  - http://gitea-svc.\<namespace\>:3000

## From outside the cluster

Use the endpoint to connect:
  - http://gitea.\<cluster-apps-domain\>

# References

* [dci-openshfit-agent](https://github.com/redhat-cip/dci-openshift-agent/): An agent that allows the deployment of OCP clusters, it is integrated with DCI (Red Hat Distributed CI).
* [dci-openshfit-app-agent](https://github.com/redhat-cip/dci-openshift-app-agent/): An agent that allows the deployment of workloads and certification testing on top OCP clusters, it is integrated with DCI (Red Hat Distributed CI).
