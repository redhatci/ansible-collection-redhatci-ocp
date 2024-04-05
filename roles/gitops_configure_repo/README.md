GitOps configure Repo
=========

This Role configures a repository and the ssh key to the ArgoCD instance.

Requirements
------------

* ArgoCD/GitOps already configured
* The repository MUST be hosted in GitLab
* The SSH key has permissions to read from GitLab repository.

Role Variables
--------------

Variable | Type | Required | Default | Description
---------|------|-----------|---------|------------
gitlab_ssh_known_hosts | String | yes | | Should be the ssh known hosts. It is required by ArgoCD when working with a SSH key.

Dependencies
------------

License
-------

GNU GENERAL PUBLIC LICENSE version 3
