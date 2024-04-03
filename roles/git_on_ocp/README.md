# Git on OCP

Deploys a lightweight, single repo, Git repository server on an OpenShift cluster.

## Requirements

* A running OCP cluster with a valid kubeconfig file.

* The KUBECONFIG environment variable must be defined and point to the kubeconfig file.

## Variables

Variable | Required | Default | Description
---------|----------|---------|-------------
goo_namespace | No | git_repos | Namespace where the Git service will be deployed in.
goo_repo_name | No | repo | Name of the repository hosted by the deployment. The resulting repo URL will be ssh://git@{{ svc }}:2222/git/{{ goo_repo_name }}. Bear in mind is a common practice to add the suffix ".git" to the repo names.
goo_ssh_authorized_keys | Yes | - | A text string formatted as the SSH authorized kyes file, containing the SSH public keys for the users authorized to push changes into the repository.
