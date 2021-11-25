# Single Node OpenShift
Single Node OpenShift is a Red Hat Openshift deployment designed to have a small footprint that fits constrained environments and Edge computing needs.

The deployment consists on  a Single Cluster Node playing the Master and Worker Node at the same time. Single-node OpenShift deployment does not have an option to add additional hosts Single-node OpenShift isn’t highly-available. It explicitly does not assume zero downtime of the Kubernetes API.

## Pre-requisites

A provisioner node with the following:
- A RHEL >= 8.4 server
- Ansible >= 2.9
- A valid Red Hat subscription
  - Access to `rhel-8-for-x86_64-baseos-rpms` and `rhel-8-for-x86_64-appstream-rpms` repositories is required
  - If the vars activation_key and org_id are provided, the system registration to the proper subscriptions is done during the deployment

### Hardware Requirements

SNO can be installed in a virtual machine on top of libvirt in the provisioner node, or it can be an independent baremetal node.

These are the minimum recommended resources to run:
- CPU: 8 cores
- RAM: 32 GB
- Storage: 120 GB
- 1 Network Interface
- Our of Band console (Baremetal only)

Virtual SNO implementation can be deployed with less resources, but there is no much room for applications:
- vCPU: 6
- RAM: 16 GB
- Storage: 20 GB

## Installation

See https://github.com/redhat-cip/dci-openshift-agent/tree/master/roles/sno-installer/#readme for details
