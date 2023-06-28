Install operator GitOps
=========

This Role installs the GitOps operator, created the required namespace and checks that the pods are running.
It also create the AgentService


Requirements
------------

* Kubeconfig file of an OCP cluster already deployed

Role Variables
--------------

metallb: True or false. Set it to true to modify the Provisioning resource to allow the Bare Metal Operator to watch all namespaces
database_storage_request: i.e 20Gi for the AgentService
filesystem_storage_request: i.e 20Gi for AgentService
image_storage_request: i.e 100Gi for the AgentService

Dependencies
------------

* ODF operator installed

License
-------

GNU GENERAL PUBLIC LICENSE version 3
