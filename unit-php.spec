# centos/sclo spec file for unit-php, from:
#
# remirepo/fedora spec file for unit-php
#
# Copyright (c) 2019-2020 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%if 0%{?scl:1}
%scl_package       unit-php
%global sub_prefix %{scl_prefix}
%if "%{scl}" == "rh-php72"
%global sub_prefix sclo-php72-
%endif
%if "%{scl}" == "rh-php73"
%global sub_prefix sclo-php73-
%endif
%global modname %scl
AutoReq: 0
# ensure correct dependencies
Requires: %{scl_prefix}php-cli
Requires: %{scl_prefix}php-embedded
%else
%global _root_bindir          %{_bindir}
%global _root_libdir          %{_libdir}
%global _root_sharedstatedir  %{_sharedstatedir}
%global modname php
%endif

%global gh_owner     nginx
%global project      unit
%global gh_commit    ba445d31f17194be335fb8bf6295bceac991299d
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})

%undefine _debugsource_packages

# Disable RPATH check
%global __arch_install_post /bin/true

# Disable auto-provides (php_plugin.so is not a library)
AutoProv: 0

Name:          %{?sub_prefix}%{project}-php
Version:       1.19.0
Release:       1%{?dist}
Summary:       PHP module for NGINX Unit
License:       ASL 2.0
URL:           https://unit.nginx.org/

Source0:       https://github.com/%{gh_owner}/%{project}/archive/%{gh_commit}/%{project}-%{version}-%{gh_short}.tar.gz

BuildRequires: %{?dtsprefix}gcc
BuildRequires: %{?scl_prefix}php-devel
BuildRequires: %{?scl_prefix}php-embedded
BuildRequires: openssl-devel

%if "%{?scl_prefix}" != "%{?sub_prefix}"
Provides:      %{?scl_prefix}%{project}-php         = %{version}-%{release}
Provides:      %{?scl_prefix}%{project}-php%{?_isa} = %{version}-%{release}
%endif

Requires:      %{project} = %{version}


%description
This package contains the PHP module for NGINX unit,
designed to work with %{project} in nginx official repository.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}
and NGINX unit %{version}.


%prep
%setup -qn %{project}-%{gh_commit}


%build
modbuild() {
: Main unit configuration
./configure \
  --prefix=%{_prefix} \
  --state=%{_root_sharedstatedir}/unit \
  --control="unix:/var/run/unit/control.sock" \
  --pid=/var/run/unit/unit.pid \
  --log=/var/log/unit/unit.log \
  --openssl \
  --cc-opt="%{optflags}" \
  --ld-opt="-L%{_libdir} %{?scl:-Wl,-rpath,%{_libdir}}" \
  $*

: PHP module configuration
./configure php --config=%{_bindir}/php-config --module=%{modname}

make %{modname} %{?_smp_mflags}
}

: Debug build
modbuild --modules=%{_root_libdir}/unit/debug-modules --debug
mv build deb-build

: Standard build
modbuild --modules=%{_root_libdir}/unit/modules
mv build std-build



%install
rm -f build
ln -s deb-build build
make %{modname}-install DESTDIR=%{buildroot}

rm -f build
ln -s std-build build
make %{modname}-install DESTDIR=%{buildroot}


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc NOTICE README CHANGES
%doc pkg/rpm/rpmbuild/SOURCES/unit.example-php-app
%doc pkg/rpm/rpmbuild/SOURCES/unit.example-php-config
%{_root_libdir}/unit/debug-modules/%{modname}.unit.so
%{_root_libdir}/unit/modules/%{modname}.unit.so


%changelog
* Fri Aug 14 2020 Remi Collet <remi@remirepo.net> - 1.19.0-1
- update to 1.19.0

* Fri Apr 17 2020 Remi Collet <remi@remirepo.net> - 1.17.0-1
- update to 1.17.0

* Fri Feb  7 2020 Remi Collet <remi@remirepo.net> - 1.15.0-1
- update to 1.15.0

* Thu Jan  2 2020 Remi Collet <remi@remirepo.net> - 1.14.0-1
- update to 1.14.0

* Fri Nov 15 2019 Remi Collet <remi@remirepo.net> - 1.13.0-1
- update to 1.13.0

* Fri Oct  4 2019 Remi Collet <remi@remirepo.net> - 1.12.0-1
- update to 1.12.0

* Fri Sep 20 2019 Remi Collet <remi@remirepo.net> - 1.11.0-1
- update to 1.11.0

* Fri Aug 23 2019 Remi Collet <remi@remirepo.net> - 1.10.0-1
- update to 1.10.0

* Sat Mar  2 2019 Remi Collet <remi@remirepo.net> - 1.8.0-1
- cleanup for SCLo build

* Sat Mar  2 2019 Remi Collet <remi@remirepo.net> - 1.8.0-1
- update to 1.8.0

* Fri Feb  8 2019 Remi Collet <remi@remirepo.net> - 1.7.1-1
- update to 1.7.1

* Wed Jan 16 2019 Remi Collet <remi@remirepo.net> - 1.7-2
- rebuild

* Mon Jan 14 2019 Remi Collet <remi@remirepo.net> - 1.7-1
- initial package
