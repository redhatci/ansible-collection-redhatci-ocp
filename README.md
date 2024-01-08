[![Ansible Collection](https://img.shields.io/badge/dynamic/json?color=orange&style=flat&label=collection&prefix=v&url=https://galaxy.ansible.com/api/v3/collections/redhatci/ocp/&query=highest_version.version)](https://galaxy.ansible.com/ui/repo/published/redhatci/ocp/)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/redhatci/ansible-collection-redhatci-ocp)](https://github.com/redhatci/ansible-collection-redhatci-ocp/commits/main)
[![GitHub Contributors](https://img.shields.io/github/contributors/redhatci/ansible-collection-redhatci-ocp)](https://github.com/redhatci/ansible-collection-redhatci-ocp/graphs/contributors)
[![Zuul RPM build](https://softwarefactory-project.io/zuul/api/tenant/local/badge?pipeline=dci-post&project=redhatci/ansible-collection-redhatci-ocp)](https://softwarefactory-project.io/zuul/t/local/builds?project=redhatci%252Fansible-collection-redhatci-ocp&pipeline=dci-post)
[![Ansible Galaxy Publish](https://github.com/redhatci/ansible-collection-redhatci-ocp/actions/workflows/publish.yml/badge.svg)](https://github.com/redhatci/ansible-collection-redhatci-ocp/actions/workflows/publish.yml)
[![DCI Merge Queue](https://github.com/redhatci/ansible-collection-redhatci-ocp/actions/workflows/dci-merge.yml/badge.svg)](https://github.com/redhatci/ansible-collection-redhatci-ocp/actions/workflows/dci-merge.yml)

# RedHat CI OCP collection

This repository hosts the `redhatci.ocp` Ansible collection.

The collection includes Ansible roles and modules to help automate OpenShift Platform interactions, as well as the deployment, testing and continuous integration of the clusters or related components.


## Installing the collection

### Ansible Galaxy

```Shell
ansible-galaxy collection install redhatci.ocp
```

### RPM package

```Shell
dnf -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
dnf -y install https://packages.distributed-ci.io/dci-release.el8.noarch.rpm
dnf -y install ansible-collection-redhatci-ocp
```

## Roles

Name | Description
--- | ---
[redhatci.ocp.acm_hypershift](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/acm_hypershift/README.md) | Deployment of Hypershift (Hosted Control Planes) through ACM (Advanced Cluster Management).
[redhatci.ocp.acm_setup](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/acm_setup/README.md) | Performs the Advanced Cluster Management (ACM) post-installation tasks
[redhatci.ocp.acm_sno](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/acm_sno/README.md) | Deployment of SNO (Single Node Openshift) instances using ACM (Advanced Cluster Management)
[redhatci.ocp.catalog_source](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/catalog_source/README.md) | A Role to deploy an OLM-based CatalogSource
[redhatci.ocp.chart_verifier](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/chart_verifier/README.md) | Executes the [chart-verifier](https://github.com/redhat-certification/chart-verifier) tool.
[redhatci.ocp.check_resource](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/check_resource/README.md) | Role to wait for the deployment of a given resource
[redhatci.ocp.cnf_cert](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/cnf_cert/README.md) | Executes the [Test Network Function (TNF)](https://github.com/test-network-function/cnf-certification-test) tool.
[redhatci.ocp.conserver](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/conserver/README.md) | Setup of [conserver](https://www.conserver.com/) to log serial console.
[redhatci.ocp.create_certification_project](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/create_certification_project/README.md) | Creation of a container certification project
[redhatci.ocp.create_helmchart](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/create_helmchart/README.md) | Creation of a Helm Chart certification project
[redhatci.ocp.create_pr](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/create_pr/README.md) | Pull-Request handling for helm chart certification and operator bundle certification.
[redhatci.ocp.deploy_cr](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/deploy_cr/README.md) | Deploys a custom resource
[redhatci.ocp.deprecated_api](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/deprecated_api/README.md) | Extracts deprecated API calls in a cluster
[redhatci.ocp.fbc_catalog](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/fbc_catalog/README.md) | Create File Base Catalogs (FBC) for Operator Lifecycle Manager (OLM).
[redhatci.ocp.get_logs_from_namespace](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/get_logs_from_namespace/README.md) | Extracts the logs from pods in a namespace
[redhatci.ocp.hco_setup](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/hco_setup/README.md) | Deploys and configures the `hco-operator` through the `kubevirt-hyperconverged` CRs.
[redhatci.ocp.include_components](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/include_components/README.md) | Adds components in the DCI jobs from software resources available
[redhatci.ocp.installer](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/installer/README.md) | [IPI installer](https://github.com/openshift-kni/baremetal-deploy)
[redhatci.ocp.label_nodes](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/label_nodes/README.md) | Applies labels defined at inventory level to the OCP cluster nodes.
[redhatci.ocp.merge_registry_creds](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/merge_registry_creds/README.md) | Combines multiple registry credentials in JSON format passed as dictionaries
[redhatci.ocp.metallb_setup](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/metallb_setup/README.md) | Setup of the MetalLB operator in BGP mode.
[redhatci.ocp.mirror_catalog](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/mirror_catalog/README.md) | Mirrors a catalog and its related images.
[redhatci.ocp.mirror_from_directory](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/mirror_from_directory/README.md) | Mirror operators from a local directory into a container registry using the `oc-mirror` plugin.
[redhatci.ocp.mirror_images](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/mirror_images/README.md) | Mirrors images from one repository to another.
[redhatci.ocp.mirror_ocp_release](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/mirror_ocp_release/README.md) | Mirrors a given OpenShift release version to a given cache directory.
[redhatci.ocp.nfs_external_storage](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/nfs_external_storage/README.md) | Add NFS external storage provisioner to a cluster.
[redhatci.ocp.node_prep](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/node_prep/README.md) | [Preparation for IPI installer](https://github.com/openshift-kni/baremetal-deploy)
[redhatci.ocp.ocp_logging](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/ocp_logging/README.md) | Enables the OCP logging subsystem.
[redhatci.ocp.ocp_on_libvirt](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/ocp_on_libvirt/README.md) | Creation of a libvirt environment to install OCP
[redhatci.ocp.oc_setup](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/oc_setup/README.md) | Setup additional credentials (httpasswd) for a running OCP cluster.
[redhatci.ocp.odf_setup](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/odf_setup/README.md) | Setup of [OpenShift Data Foundation (ODF)](https://www.redhat.com/en/technologies/cloud-computing/openshift-data-foundation)
[redhatci.ocp.olm_operator](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/olm_operator/README.md) | Deploys an OLM-based operator.
[redhatci.ocp.opcap_tool](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/opcap_tool/README.md) | Runs OPCAP tool to test the installation of the Openshift operators.
[redhatci.ocp.openshift_cnf](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/openshift_cnf/README.md) | Generate an Openshift-cnf certification project.
[redhatci.ocp.operator_sdk](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/operator_sdk/README.md) | Setup Operator-SDK Scorecard test suite
[redhatci.ocp.preflight](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/preflight/README.md) | Container and Operator certification through Preflight
[redhatci.ocp.prune_catalog](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/prune_catalog/README.md) | Create a pruned catalog, leaving only the specified operators.
[redhatci.ocp.pyxis](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/pyxis/README.md) | Interacts with Pyxis API to submit Preflight certification results
[redhatci.ocp.redhat_tests](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/redhat_tests/README.md) | [Openshift End to End tests](https://github.com/openshift/openshift-tests)
[redhatci.ocp.resources_to_components](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/resources_to_components/README.md) | Creates DCI components based on Kubernetes resources
[redhatci.ocp.setup_minio](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/setup_minio/README.md) | Deployment of [Minio](https://min.io/).
[redhatci.ocp.sno_installer](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/sno_installer/README.md) | Deploy OCP SNO in a very opinionated fashion.
[redhatci.ocp.sno_node_prep](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/sno_node_prep/README.md) | Preparation to deploy OCP SNO
[redhatci.ocp.sos_report](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/sos_report/README.md) | Generate SOS report from a list of OCP nodes.
[redhatci.ocp.storage_tester](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/storage_tester/README.md) | Storage Service tests during cluster upgrade
[redhatci.ocp.upi_installer](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/upi_installer/README.md) | UPI Installer
[redhatci.ocp.vbmc](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/vbmc/README.md) | Stup [Virtual BMC](https://docs.openstack.org/virtualbmc/latest/user/index.html)
[redhatci.ocp.verify_tests](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/verify_tests/README.md) | Verification of tests based on rules

## Plugins

Name | Type | Description
--- | --- | ---
[redhatci.ocp.junit2dict]() | Filter | Transforms a JUnit into a dictionary
[redhatci.ocp.ocp_compatibility]() | Filter | Parse the deprecated and to-be-deprecated API after the workload installation
[redhatci.ocp.regex_diff]() | Filter | Obtain differences between two lists
[redhatci.ocp.nmcli]() | Module | A modified module to manage networking based on [community.general.nmcli](https://github.com/ansible-collections/community.general)
[redhatci.ocp.virt]() | Module | A copy of the module [community.libvirt.virt](https://github.com/ansible-collections/community.libvirt) to manage libvirt 

## License

See [LICENSES](./LICENSES) directory for the list of licences used in this repository
