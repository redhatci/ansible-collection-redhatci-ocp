GitOps configure Repo
=========

This Role configures a repository and the ssh key to the ArgoCD instance.

Requirements
------------

* ArgoCD/GitOps already configured
* The repository MUST grant access through SSH keys.
* The SSH key has permissions to read from the Git repository.

Role Variables
--------------

Name                        | Type   | Required | Default                                            | Description
--------------------------- | ------ | -------- | -------------------------------------------------- | -------------------------------------------------------------
gcr_ssh_key_path            | string | yes      | `{{ lookup('env', 'HOME') }}/.ssh/id_rsa`          | Path to the SSH private key file used to log into the GitOps manifest repository.
gcr_ssh_known_hosts         | string | no       | -                                                  | Should be the ssh known hosts. It is required by ArgoCD when working with a SSH key.
gcr_ztp_gitops_repo         | string | yes      | -                                                  | URL to the ZTP GitOps Git repository.

Dependencies
------------

License
-------

GNU GENERAL PUBLIC LICENSE version 3
