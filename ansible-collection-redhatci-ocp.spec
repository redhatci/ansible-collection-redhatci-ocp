%global org redhatci
%global repo ocp
%global forgeurl https://github.com/%{org}/%{repo}

Name:           ansible-collection-%{org}-%{repo}
Version:        0.1.0
Release:        1.VERS%{?dist}
Summary:        Redhat OCP Collection for ansible

License:        GPL-2.0-or-later and Apache-2.0
URL:            %{forgeurl}
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  ansible-packaging

BuildArch:      noarch

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
* Tue Jul 18 2023 Jorge Gallegos <jgallego@redhat.com> - 0.1.0-1
- Initial RPM Spec
