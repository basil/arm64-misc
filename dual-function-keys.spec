Name: dual-function-keys
Version:        1.5.0
Release:        1%{?dist}
Summary:        Interception - dual function keys

License: MIT
URL: https://gitlab.com/interception/linux/plugins/dual-function-keys
Source0: https://gitlab.com/interception/linux/plugins/dual-function-keys/-/archive/%{version}/dual-function-keys-%{version}.tar.gz

BuildRequires: boost
BuildRequires: cmake
BuildRequires: pkgconfig
BuildRequires: g++
BuildRequires: gcc
BuildRequires: libevdev-devel
BuildRequires: yaml-cpp-devel

Requires: interception-tools
Requires: libevdev
Requires: systemd
Requires: yaml-cpp
Requires: glibc

%description
Tap for one key, hold for another. Great for modifier keys like: hold for ctrl, tap for delete. A hand-saver for those with restricted finger mobility. A plugin for interception tools.

%prep
%autosetup

%build
make DESTDIR=%{buildroot} PREFIX=%{_prefix} -j%{?_smp_build_nproc}

%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}


%files
%license LICENSE.md
%doc README.md
%define debug_package %{nil}

%{_bindir}/dual-function-keys
%{_mandir}/man1/dual-function-keys.1.gz

%changelog
* Thu May 29 2025 Lachlan Marie <lchlnm@pm.me> - 1.5.0-1
- Initial RPM packaging of dual-function-keys
