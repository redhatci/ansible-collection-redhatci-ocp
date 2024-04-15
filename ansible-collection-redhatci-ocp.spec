%global org redhatci
%global repo ansible-collection-redhatci-ocp
%global forgeurl https://github.com/%{org}/%{repo}

Name:           %{repo}
Version:        0.8.EPOCH
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
Requires: ansible-collection-community-kubernetes
Requires: ansible-collection-community-libvirt
Requires: ansible-collection-containers-podman
Requires: git
Requires: jq
Requires: podman
Requires: python3-jmespath
Requires: python3-netaddr
Requires: python3-pyyaml
Requires: skopeo

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
