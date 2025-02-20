[![Ansible Collection](https://img.shields.io/badge/dynamic/json?color=orange&style=flat&label=collection&prefix=v&url=https://galaxy.ansible.com/api/v3/collections/redhatci/ocp/&query=highest_version.version)](https://galaxy.ansible.com/ui/repo/published/redhatci/ocp/)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/redhatci/ansible-collection-redhatci-ocp)](https://github.com/redhatci/ansible-collection-redhatci-ocp/commits/main)
[![GitHub Contributors](https://img.shields.io/github/contributors/redhatci/ansible-collection-redhatci-ocp)](https://github.com/redhatci/ansible-collection-redhatci-ocp/graphs/contributors)
[![Zuul RPM build](https://softwarefactory-project.io/zuul/api/tenant/local/badge?pipeline=dci-post&project=redhatci/ansible-collection-redhatci-ocp)](https://softwarefactory-project.io/zuul/t/local/builds?project=redhatci%252Fansible-collection-redhatci-ocp&pipeline=dci-post)
[![Ansible Galaxy Publish](https://github.com/redhatci/ansible-collection-redhatci-ocp/actions/workflows/publish.yml/badge.svg)](https://github.com/redhatci/ansible-collection-redhatci-ocp/actions/workflows/publish.yml)
[![DCI Merge Queue](https://github.com/redhatci/ansible-collection-redhatci-ocp/actions/workflows/dci-merge.yml/badge.svg)](https://github.com/redhatci/ansible-collection-redhatci-ocp/actions/workflows/dci-merge.yml)

# RedHat CI OCP collection

This repository hosts the `redhatci.ocp` Ansible collection.

The collection includes Ansible roles and modules to help automate OpenShift Platform interactions, as well as the deployment, testing and continuous integration of the clusters or related components.

> [!IMPORTANT]
> Red Hat does not provide commercial support for the content of this collection

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
[redhatci.ocp.setup_acm_agents](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/setup_acm_agents/README.md) | This role allows to setup ACM agents used for Bare-metal deployments.
[redhatci.ocp.acm_setup](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/acm_setup/README.md) | Performs the Advanced Cluster Management (ACM) post-installation tasks
[redhatci.ocp.acm_sno](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/acm_sno/README.md) | Deployment of SNO (Single Node OpenShift) instances using ACM (Advanced Cluster Management)
[redhatci.ocp.acm_spoke_mgmt](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/acm_spoke_mgmt/README.md) | This role allows to perform multiple management operations related to a spoke cluster,e.g. attach a spoke cluster to a given hub cluster, or detach a spoke cluster from a given hub cluster.
[redhatci.ocp.add_day2_node](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/add_day2_node/README.md) | Adds as nodes to a pre-existing cluster using a pre-existing on-prem assisted installer instance.
[redhatci.ocp.apply_nmstate](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/apply_nmstate/README.md) | Applies nmstate network configuration to a host.
[redhatci.ocp.approve_csrs](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/approve_csrs/README.md) |Checks for Cert Signing Requests in the pending state and approves them until nodes in the day2_workers group are present in the oc nodes output.
[redhatci.ocp.boot_disk](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/boot_disk/README.md) | Reboots nodes to the disk based on its vendor.
[redhatci.ocp.boot_iso](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/boot_iso/README.md) | Boots nodes to the provided ISO on its vendor.
[redhatci.ocp.catalog_source](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/catalog_source/README.md) | A Role to deploy an OLM-based CatalogSource
[redhatci.ocp.chart_verifier](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/chart_verifier/README.md) | Executes the [chart-verifier](https://github.com/redhat-certification/chart-verifier) tool.
[redhatci.ocp.check_resource](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/check_resource/README.md) | Role to wait for the deployment of a given resource
[redhatci.ocp.cluster_compare](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/cluster_compare/README.md) | A role to facilitate the comparison of Kubernetes cluster configurations by using the kube-compare tool.
[redhatci.ocp.configure_ztp_gitops_apps](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/configure_ztp_gitops_apps/README.md) | Connects the OpenShift Gitops Operator to a remote Git repository to pull the SiteConfig and PolicyGenTemplate manifests.
[redhatci.ocp.configure_ztp_gitops_repo](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/configure_ztp_gitops_repo/README.md) | Pushes the SiteConfig and PolicyGenTemplate manifests to the Git repository, thus triggering the Spoke Cluster deployment process.
[redhatci.ocp.conserver](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/conserver/README.md) | Setup of [conserver](https://www.conserver.com/) to log serial console.
[redhatci.ocp.create_certification_project](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/create_certification_project/README.md) | Creation of a container certification project
[redhatci.ocp.create_cluster](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/create_cluster/README.md) | Creates a cluster definition in an on-prem assisted installer instance.
[redhatci.ocp.create_day2_cluster](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/create_day2_cluster/README.md) | Creates an add-hosts cluster definition in an on-prem assisted installer instance which can be used to add day2 nodes to the cluster.
[redhatci.ocp.create_rhde_builder](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/create_rhde_builder/README.md) | Create a VM ready for building RHDE images.
[redhatci.ocp.create_vms](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/create_vms/README.md) | Provisions libvirt network, storage pools and the KVM Nodes.
[redhatci.ocp.create_helmchart](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/create_helmchart/README.md) | Creation of a Helm Chart certification project
[redhatci.ocp.create_pr](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/create_pr/README.md) | Pull-Request handling for helm chart certification and operator bundle certification.
[redhatci.ocp.deploy_cr](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/deploy_cr/README.md) | Deploys a custom resource
[redhatci.ocp.deprecated_api](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/deprecated_api/README.md) | Extracts deprecated API calls in a cluster
[redhatci.ocp.destroy_vms](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/destroy_vms/README.md) | Destroys libvirt network, storage pools and the KVM Nodes and the network bridge connection.
[redhatci.ocp.display_deployment_plan](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/display_deployment_plan/README.md) | Displays the crucible deployment plan and waits for user confirmation.
[redhatci.ocp.efi_boot_mgr](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/efi_boot_mgr/README.md) | Removes the non-active UEFI boot entries from OCP nodes.
[redhatci.ocp.etcd_data](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/etcd_data/README.md) | Allows to query, encrypt or decrypt etcd data using the supported encryption types.
[redhatci.ocp.example_cnf_deploy](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/example_cnf_deploy/README.md) | Deploys the example-cnf workload on top of an OpenShift cluster
[redhatci.ocp.extract_openshift_installer](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/extract_openshift_installer/README.md) | Extracts openshift_installer binary from the release image.
[redhatci.ocp.generate_agent_iso](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/generate_agent_iso/README.md) | Creates the boot ISO using OpenShift_installer's agent sub-command
[redhatci.ocp.generate_discovery_iso](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/generate_discovery_iso/README.md) | Creates the discovery ISO for a pre-existing cluster definition using a pre-existing on-prem assisted installer
[redhatci.ocp.generate_manifests](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/generate_manifests/README.md) | Generates the manifests required for OpenShift_installer's agent sub-command
[redhatci.ocp.generate_ssh_key_pair](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/generate_ssh_key_pair/README.md) | Produces an ssh key pair
[redhatci.ocp.get_image_hash](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/get_image_hash/README.md) | Uses `skopeo` to produce a dictionary of image digests for images used in various playbooks.
[redhatci.ocp.gitops_configure_repo](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/gitops_configure_repo/README.md) | Configures the SSH Git repo credentials for the openshift-gitops-operator to be able to connect to the repositories.
[redhatci.ocp.fbc_catalog](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/fbc_catalog/README.md) | Create File Base Catalogs (FBC) for Operator Lifecycle Manager (OLM).
[redhatci.ocp.get_logs_from_namespace](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/get_logs_from_namespace/README.md) | Extracts multiple logs from pods and events in a Namespace.
[redhatci.ocp.hco_setup](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/hco_setup/README.md) | Deploys and configures the `hco-operator` through the `kubevirt-hyperconverged` CRs.
[redhatci.ocp.hostedbm](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/hostedbm/README.md) | This role allows to create hosted guest clusters with BM workers.
[redhatci.ocp.include_components](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/include_components/README.md) | Create and attach DCI components to DCI jobs from git repositories, RPMs or commit URLs.
[redhatci.ocp.insert_dns_records](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/insert_dns_records/README.md) | Setups `dnsmasq` (either directly or via `NetworkManager`) inserting the DNS A records required for OpenShift install.
[redhatci.ocp.install_cluster](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/install_cluster/README.md) | Waits for nodes to be discovered by the on-prem assisted installer then then patches cluster networking and triggers the install process
[redhatci.ocp.installer](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/installer/README.md) | [IPI installer](https://github.com/openshift-kni/baremetal-deploy)
[redhatci.ocp.install_operator_gitops](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/install_operator_gitops/README.md) | Installs and configures the openshift-gitops-operator so it can be used for ZTP deployments. Installation is optional and may be skipped by setting the variable ```ioc_configure_only: true``
[redhatci.ocp.jenkins_job_launcher](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/jenkins_job_launcher/README.md) | Launch Jenkins jobs
[redhatci.ocp.k8s_best_practices_certsuite](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/k8s_best_practices_certsuite/README.md) | Executes the [Red Hat Best Practices Test Suite for Kubernetes](https://github.com/redhat-best-practices-for-k8s/certsuite) tool.
[redhatci.ocp.kvirt_vm](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/kvirt_vm/README.md) | Deployment of Kubevirt virtual machines.
[redhatci.ocp.label_nodes](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/label_nodes/README.md) | Applies labels defined at inventory level to the OCP cluster nodes.
[redhatci.ocp.manage_firewalld_zone](roles/manage_firewalld_zone/README.md) | Manage a FirewallD zone.
[redhatci.ocp.merge_registry_creds](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/merge_registry_creds/README.md) | Combines multiple registry credentials in JSON format passed as dictionaries
[redhatci.ocp.metallb_setup](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/metallb_setup/README.md) | Setup of the MetalLB operator in BGP mode.
[redhatci.ocp.microshift_generate_iso](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/microshift_generate_iso/README.md) | Generate a MicroShift ISO image.
[redhatci.ocp.mirror_catalog](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/mirror_catalog/README.md) | Mirrors a catalog and its related images.
[redhatci.ocp.mirror_from_directory](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/mirror_from_directory/README.md) | Mirror operators from a local directory into a container registry using the `oc-mirror` plugin.
[redhatci.ocp.mirror_images](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/mirror_images/README.md) | Mirrors images from one repository to another.
[redhatci.ocp.mirror_ocp_release](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/mirror_ocp_release/README.md) | Mirrors a given OpenShift release version to a given cache directory.
[redhatci.ocp.monitor_agent_based_installer](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/monitor_agent_based_installer/README.md) | Tracks the progress of the agent based installation via openshift_installer
[redhatci.ocp.monitor_cluster](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/monitor_cluster/README.md) | Tracks the progress of the cluster installation via an on-prem assisted installer
[redhatci.ocp.monitor_host](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/monitor_host/README.md) | Tracks host status dusing the installation via an on-prem assisted installer and triggers a reboot to disk if needed
[redhatci.ocp.mount_discovery_iso_for_pxe](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/mount_discovery_iso_for_pxe/README.md) | Extracts the required artifacts for a pxe boot from a discovery iso
[redhatci.ocp.multibench_run](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/multibench_run/README.md) | Launch a crucible scenario on OCP
[redhatci.ocp.nfs_external_storage](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/nfs_external_storage/README.md) | Add NFS external storage provisioner to a cluster.
[redhatci.ocp.node_prep](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/node_prep/README.md) | [Preparation for IPI installer](https://github.com/openshift-kni/baremetal-deploy)
[redhatci.ocp.ocp_add_users](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/ocp_add_users/README.md) | Add users to an OpenShift cluster through htpasswd Identity Provider.
[redhatci.ocp.ocp_remove_nodes](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/ocp_remove_nodes/README.md) | Remove (worker) nodes from an OCP cluster. 
[redhatci.ocp.ocp_logging](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/ocp_logging/README.md) | Enables the OCP logging subsystem.
[redhatci.ocp.ocp_on_libvirt](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/ocp_on_libvirt/README.md) | Creation of a libvirt environment to install OCP
[redhatci.ocp.odf_setup](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/odf_setup/README.md) | Setup of [OpenShift Data Foundation (ODF)](https://www.redhat.com/en/technologies/cloud-computing/openshift-data-foundation)
[redhatci.ocp.olm_operator](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/olm_operator/README.md) | Deploys an OLM-based operator.
[redhatci.ocp.opcap_tool](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/opcap_tool/README.md) | Runs OPCAP tool to test the installation of the Openshift operators.
[redhatci.ocp.openshift_cnf](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/openshift_cnf/README.md) | Generate an Openshift-cnf certification project.
[redhatci.ocp.operator_sdk](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/operator_sdk/README.md) | Setup Operator-SDK Scorecard test suite
[redhatci.ocp.patch_cluster](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/patch_cluster/README.md) | Patches definition of a cluster in an on-prem assisted installer.
[redhatci.ocp.patch_host_config](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/patch_host_config/README.md) | Patches host configuration in an on-prem assisted installer.
[redhatci.ocp.populate_mirror_registry](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/populate_mirror_registry/README.md) | Copies the images required for installation to a local registry
[redhatci.ocp.post_install](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/post_install/README.md) | Waits for the cluster to become operational then copies the kubeconfig and kubeadmin
[redhatci.ocp.preflight](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/preflight/README.md) | Container and Operator certification through Preflight
[redhatci.ocp.prereq_facts_check](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/prereq_facts_check/README.md) | Patches host definition in pre-existing on-prem assisted installer
[redhatci.ocp.process_kvm_nodes](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/process_kvm_nodes/README.md) | Creates and distributes kvm node specifications to vm hosts
[redhatci.ocp.process_nmstate](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/process_nmstate/README.md) | Renders nmstate from crucible network_config
[redhatci.ocp.prune_catalog](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/prune_catalog/README.md) | Create a pruned catalog, leaving only the specified operators.
[redhatci.ocp.pyxis](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/pyxis/README.md) | Interacts with Pyxis API to submit Preflight certification results
[redhatci.ocp.redhat_tests](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/redhat_tests/README.md) | [Openshift End to End tests](https://github.com/openshift/openshift-tests)
[redhatci.ocp.remove_ztp_gitops_resources](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/remove_ztp_gitops_resources/README.md) | Remove all GitOps related resources for a given spoke cluster, excepting the cluster namespace, which is not deleted because this will imply the spoke cluster is detached from the hub cluster.
[redhatci.ocp.resources_to_components](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/resources_to_components/README.md) | Creates DCI components based on Kubernetes resources
[redhatci.ocp.rhoai](roles/rhoai/README.md) | Install the Red Hat OpenShift AI operators
[redhatci.ocp.setup_assisted_installer](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/setup_assisted_installer/README.md) | Deploys an on-prem assisted installer
[redhatci.ocp.setup_gitea](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/setup_gitea/README.md) | Deployment of [Gitea](https://about.gitea.com)
[redhatci.ocp.setup_http_store](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/setup_http_store/README.md) | Sets up a web host which can be used to distribute iso's for `boot_iso` role
[redhatci.ocp.setup_minio](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/setup_minio/README.md) | Deployment of [Minio](https://min.io/).
[redhatci.ocp.setup_mirror_registry](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/setup_mirror_registry/README.md) | Deploys a local container registry
[redhatci.ocp.setup_netobserv_stack](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/setup_netobserv_stack/README.md) | Set up the OCP Network Observability subsystem
[redhatci.ocp.setup_ntp](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/setup_ntp/README.md) | Deploys chrony
[redhatci.ocp.setup_radvd](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/setup_radvd/README.md) | Deploys the router advertisement daemon (radvd) for IPV6 installations
[redhatci.ocp.setup_selfsigned_cert](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/setup_selfsigned_cert/README.md) | Generates self signed SSL certs
[redhatci.ocp.setup_sushy_tools](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/setup_sushy_tools/README.md) | deploys virtual redfish for kvm
[redhatci.ocp.setup_tftp](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/setup_tftp/README.md) | Deploys a TFTP server
[redhatci.ocp.setup_vm_host_network](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/setup_vm_host_network/README.md) | Configures the network for vm hosts
[redhatci.ocp.sideload_kernel](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/sideload_kernel/README.md) | Side-load a given realtime kernel onto an OpenShift SNO instance.
[redhatci.ocp.sno_installer](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/sno_installer/README.md) | Deploy OCP SNO in a very opinionated fashion.
[redhatci.ocp.sno_node_prep](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/sno_node_prep/README.md) | Preparation to deploy OCP SNO
[redhatci.ocp.sos_report](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/sos_report/README.md) | Generate SOS report from a list of OCP nodes.
[redhatci.ocp.sriov_config](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/sriov_config/README.md) | Configure SR-IOV node policies and/or networks.
[redhatci.ocp.storage_tester](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/storage_tester/README.md) | Storage Service tests during cluster upgrade
[redhatci.ocp.upi_installer](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/upi_installer/README.md) | UPI Installer
[redhatci.ocp.vbmc](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/vbmc/README.md) | Setup [Virtual BMC](https://docs.openstack.org/virtualbmc/latest/user/index.html)
[redhatci.ocp.validate_dns_records](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/validate_dns_records/README.md) | Checks for the required dns entries for ingress and api VIPs
[redhatci.ocp.validate_http_store](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/validate_http_store/README.md) | Checks via a round trip that http store is functional
[redhatci.ocp.validate_inventory](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/validate_inventory/README.md) | Validates a crucible inventory
[redhatci.ocp.vendors.dell](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/vendors/dell/README.md) | Boots a dell iDRAC machine to iso or disk via redfish
[redhatci.ocp.vendors.hpe](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/vendors/hpe/README.md) | Boots a hpe ilo machine to iso or disk via redfish
[redhatci.ocp.vendors.kvm](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/vendors/kvm/README.md) | Boots a vm to iso or disk via redfish (sushy tools)
[redhatci.ocp.vendors.lenovo](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/vendors/lenovo/README.md) | Boots a lenovo machine to iso or disk via redfish
[redhatci.ocp.vendors.pxe](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/vendors/pxe/README.md) | Boots a machine to pxe or disk via ipmi
[redhatci.ocp.vendors.supermicro](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/vendors/supermicro/README.md) | Boots a supermicro machine to iso or disk via redfish
[redhatci.ocp.vendors.zt](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/vendors/zt/README.md) | Boots a zt machine to iso or disk via redfish
[redhatci.ocp.verify_tests](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/verify_tests/README.md) | Verification of tests based on rules
[redhatci.ocp.ztp.setup_cluster_image_set](https://github.com/redhatci/ansible-collection-redhatci-ocp/blob/main/roles/ztp/setup_cluster_image_set/README.md) | Create a clusterImageSet object in the hub cluster aligned with the values in the site config manifest.


## Plugins

Name | Type | Description
--- | --- | ---
[redhatci.ocp.junit2dict]() | Filter | Transforms a JUnit into a dictionary
[redhatci.ocp.ocp_compatibility]() | Filter | Parse the deprecated and to-be-deprecated API after the workload installation
[redhatci.ocp.regex_diff]() | Filter | Obtain differences between two lists
[redhatci.ocp.get_compatible_rhocp_repo]() | Module | A module to find the latest available version of the RHOCP repository
[redhatci.ocp.nmcli]() | Module | A modified module to manage networking based on [community.general.nmcli](https://github.com/ansible-collections/community.general)

## License

See roles or module documentation to find their license. This is a list of the different licenses used in this repository

- [Apache License 2.0](./LICENSE-Apache-2.0)
- [GNU General Public License v3.0](./LICENSE-GPL-3.0)
