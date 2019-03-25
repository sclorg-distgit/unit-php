# remirepo/fedora spec file for unit-php
#
# Copyright (c) 2019 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

%global gh_owner     nginx
%global project      unit
%global gh_commit    204dfec87970bb3d5ca0508e5f4ed740bd35ebe4
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})

%undefine _debugsource_packages

# Disable RPATH check
%global __arch_install_post /bin/true

# Disable auto-provides (php_plugin.so is not a library)
AutoProv: 0

%if 0%{?scl:1}
%scl_package unit-php
%global modname %scl
AutoReq: 0
# ensure correct dependencies
Requires: %{scl_prefix}php-cli
Requires: %{scl_prefix}php-embedded
%else
%global _root_libdir          %{_libdir}
%global _root_sharedstatedir  %{_sharedstatedir}
%global modname php
%endif

Name:          %{?scl_prefix}%{project}-php
Version:       1.8.0
Release:       1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
Summary:       PHP module for NGINX Unit
License:       ASL 2.0
URL:           https://unit.nginx.org/

Source0:       https://github.com/%{gh_owner}/%{project}/archive/%{gh_commit}/%{project}-%{version}-%{gh_short}.tar.gz

BuildRequires: %{?dtsprefix}gcc
BuildRequires: %{?scl_prefix}php-devel
BuildRequires: %{?scl_prefix}php-embedded
BuildRequires: openssl-devel

Requires:      %{project} = %{version}


%description
This package contains the PHP module for NGINX unit,
designed to work with %{project} in nginx official repository.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}
and NGINX unit %{version}.


%prep
%setup -qn %{project}-%{gh_commit}


%build
%{?dtsenable}

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
%{?dtsenable}

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
* Sat Mar  2 2019 Remi Collet <remi@remirepo.net> - 1.8.0-1
- update to 1.8.0

* Fri Feb  8 2019 Remi Collet <remi@remirepo.net> - 1.7.1-1
- update to 1.7.1

* Wed Jan 16 2019 Remi Collet <remi@remirepo.net> - 1.7-2
- rebuild

* Mon Jan 14 2019 Remi Collet <remi@remirepo.net> - 1.7-1
- initial package
