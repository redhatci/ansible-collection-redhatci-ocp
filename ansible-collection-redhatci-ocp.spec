%global org redhatci
%global repo ansible-collection-redhatci-ocp
%global forgeurl https://github.com/%{org}/%{repo}

Name:           %{repo}
Version:        1.3.EPOCH
Release:        VERS%{?dist}
Summary:        Red Hat OCP CI Collection for Ansible

License:        GPL-2.0-or-later and Apache-2.0
URL:            %{forgeurl}
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  ansible-packaging
BuildArch:      noarch

Requires: ansible-collection-ansible-posix
Requires: ansible-collection-ansible-utils
Requires: ansible-collection-community-crypto
Requires: ansible-collection-community-general
Requires: ansible-collection-community-libvirt
Requires: ansible-collection-containers-podman
Requires: ansible-collection-kubernetes-core
Requires: git
Requires: jq
Requires: podman
Requires: python3-jmespath
Requires: python3-netaddr
Requires: python3-pyyaml
Requires: skopeo
Conflicts: dci-openshift-agent < 1.1.0

%description
%{summary}.


%prep
%autosetup -c %{name}-%{version}
find -type f ! -executable -name '*.py' -print -exec sed -i -e '1{\@^#!.*@d}' '{}' +


%build
%ansible_collection_build


%install
%ansible_collection_install


%files -f %{ansible_collection_filelist}
%doc README.md


%changelog
* Mon Feb 10 2025 Tony Garcia <tonyg@redhat.com> - 1.3.EPOCH-VERS
- Version bump for olm_operator role updates

* Tue Jan 28 2025 Beto Rdz <josearod@redhat.com> - 1.2.EPOCH-VERS
- Move vendor Eject task to a separated file

* Mon Jan 27 2025 Ramon Perez <raperez@redhat.com> - 1.1.EPOCH-VERS
- Version bump for updated monitor_agent_based_installer role

* Tue Jan 21 2025 Tony Garcia <tonyg@redhat.com> - 1.0.EPOCH-VERS
- Removes community.kubernetes collection as dependency

* Fri Jan 17 2025 Ramon Perez <raperez@redhat.com> - 0.27.EPOCH-VERS
- Version bump for updated generate_agent_iso role

* Fri Jan 10 2025 Beto Rdz <joserod@redhat.com> - 0.26.EPOCH-VERS
- Add cluster_compare role

* Wed Jan  8 2025 Tony Garcia <tonyg@redhat.com> - 0.25.EPOCH-VERS
- Introduce kubernetes.core collection as a dependency package

* Tue Jan  7 2025 Tony Garcia <tonyg@redhat.com> - 0.24.EPOCH-VERS
- Version bump for setup_gitea role updates

* Wed Oct 16 2024 Tony Garcia <tonyg@redhat.com> - 0.23.EPOCH-VERS
- Repurpose oc_setup role, into ocp_add_users role

* Tue Oct  8 2024 Tony Garcia <tonyg@redhat.com> - 0.22.EPOCH-VERS
- Add etcd_data role

* Fri Sep 27 2024 Tony Garcia <tonyg@redhat.com> - 0.21.EPOCH-VERS
- Version bump for ocp_setup role updates

* Thu Sep 12 2024 Manuel Rodriguez <manrodri@redhat.com> - 0.20.EPOCH-VERS
- Version bump for installer and node_prep roles updates

* Mon Sep  9 2024 Ramon Perez <raperez@redhat.com> - 0.19.EPOCH-VERS
- Removed cnf_cert deprecated role

* Sat Sep  7 2024 Tony Garcia <tonyg@redhat.com> - 0.18.EPOCH-VERS
- New version with fix to catalog_source role

* Fri Sep  6 2024 Ramon Perez <raperez@redhat.com> - 0.17.EPOCH-VERS
- Version bump for example_cnf_deploy role

* Wed Aug 28 2024 Tatiana Krishtop <tkrishto@redhat.com> - 0.16.EPOCH-VERS
- Limit max OCP version in operator annotations by deprecated API check

* Wed Jul 31 2024 Tony Garcia <tonyg@redhat.com> - 0.15.EPOCH-VERS
- Version bump for mirror_images role

* Fri Jul 26 2024 Tony Garcia <tonyg@redhat.com> - 0.14.EPOCH-VERS
- Version bump due to efi_boot_mgr role

* Fri Jul 26 2024 Ramon Perez <raperez@redhat.com> - 0.13.EPOCH-VERS
- Version bump due to deprecation of cnf_cert role, moving in favour of
  k8s_best_practices_certsuite role

* Wed Jul 10 2024 Ramon Perez <raperez@redhat.com> - 0.12.EPOCH-VERS
- Version bump due to create_vms and setup_sushy_tools roles

* Fri Jun 14 2024 Tony Garcia <tonyg@redhat.com> - 0.11.EPOCH-VERS
- Version bump due to mirror_ocp_release role

* Thu May  9 2024 Tony Garcia <tonyg@redhat.com> - 0.10.EPOCH-VERS
- Version bump in the collection due to baremetal installer 4.16+

* Tue Apr 30 2024 Beto Rodriguez <josearod@redhat.com> - 0.9.EPOCH-VERS
- Dependency for acm_* roles

* Wed Mar 20 2024 Jorge A Gallegos <jgallego@redhat.com> - 0.5.EPOCH-VERS
- Adding community.crypto dependency

* Mon Feb 12 2024 Tony Garcia <tonyg@redhat.com> - 0.4.EPOCH-VERS
- Add requirements

* Tue Nov 21 2023 Frederic Lepied <flepied@redhat.com> 0.3.EPOCH-VERS
- force a rebuild with a higher Y

* Tue Nov 21 2023 Frederic Lepied <flepied@redhat.com> 0.2.EPOCH-VERS
- switch to a versioning based on the UNIX epoch to be in sync with
  the versionning for Ansible Galaxy.

* Mon Oct 16 2023 Tony Garcia <tonyg@redhat.com> - 0.2.0-1
- To be consumed by agents

* Mon Oct 16 2023 Jorge A Gallegos <jgallego@redhat.com> - 0.1.1-4
- rebuilt

* Wed Oct 11 2023 Jorge A Gallegos <jgallego@redhat.com> - 0.1.1-3
- rebuilt

* Fri Oct 06 2023 Jorge A Gallegos <jgallego@redhat.com> - 0.1.1-2
- rebuilt

* Fri Oct 06 2023 Jorge A Gallegos <jgallego@redhat.com> - 0.1.1-1
- Force-pushed build to start from a clean slate

* Tue Jul 18 2023 Jorge Gallegos <jgallego@redhat.com> - 0.1.0-1
- Initial RPM Spec
