Install operator GitOps
=========

This Role installs the GitOps operator, created the required namespace and checks that the pods are running.
It also create the AgentService


Requirements
------------

* Kubeconfig file of an OCP cluster already deployed

Role Variables
--------------

Variable | Type | Mandatory | Default | Descrition
=========|======|===========|=========|============
metallb | boolean | no | true | Set it to true to modify the Provisioning resource to allow the Bare Metal Operator to watch all namespaces.
database_storage_request | bit size | no | 20Gi | Database storage size for the AgentService.
filesystem_storage_request | bit size | no |  20Gi | Filesystem storage size for the AgentService.
image_storage_request | bit size | no | 100Gi | Image storage for the AgentService.
iog_configure_only | boolean | no | false | Set it to skip installing the Gitops Operator and run only the configuration actions.


Dependencies
------------

* ODF operator installed

License
-------

GNU GENERAL PUBLIC LICENSE version 3
