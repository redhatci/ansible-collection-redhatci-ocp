Install operator GitOps
=========

This Role installs the GitOps operator, created the required namespace and checks that the pods are running.
It also create the AgentService


Requirements
------------

* Kubeconfig file of an OCP cluster already deployed

Role Variables
--------------

Variable | Type | Required | Default | Descrition
---------|------|-----------|---------|------------
metallb | boolean | no | true | Set it to true to modify the Provisioning resource to allow the Bare Metal Operator to watch all namespaces.
database_storage_request | bit size | no | 20Gi | Database storage size for the AgentService.
filesystem_storage_request | bit size | no |  20Gi | Filesystem storage size for the AgentService.
image_storage_request | bit size | no | 100Gi | Image storage for the AgentService.
iog_configure_only | boolean | no | false | Set it to skip installing the Gitops Operator and run only the configuration actions.
iog_oc_tool_path | string | no | {{ oc_tool_path | default('/usr/local/bin/oc') }} | Path to the OpenShift Command Line Interface binary.


Dependencies
------------

* ODF operator installed

License
-------

GNU GENERAL PUBLIC LICENSE version 3
