Name: interception-tools
Version:        0.6.8
Release:        1%{?dist}
Summary:        Interception Tools - A minimal composable infrastructure on top of libudev and libevdev.

License: GNU GPL v3
URL: https://gitlab.com/interception/linux/tools
Source0: https://gitlab.com/interception/linux/tools/-/archive/v%{version}/tools-v%{version}.tar.gz

BuildRequires: boost-devel
BuildRequires: cmake
BuildRequires: pkgconfig
BuildRequires: gcc
BuildRequires: g++
BuildRequires: libevdev-devel
BuildRequires: yaml-cpp-devel
BuildRequires: systemd-devel

Requires: libevdev
Requires: systemd
Requires: yaml-cpp
Requires: glibc

%description
The Interception Tools is a small set of utilities for operating on input events of evdev devices.

%prep
%setup -qn tools-v%{version}

%build
cmake -B build \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{_prefix}
cmake --build build -j%{?_smp_build_nproc}

%install
make -C build install DESTDIR=%{buildroot}
install -Dm0755 udevmon.service %{buildroot}/%{_unitdir}/udevmon.service

%files
%license LICENSE.md
%doc README.md
%{_bindir}/udevmon
%{_bindir}/intercept
%{_bindir}/uinput
%{_bindir}/mux
%{_unitdir}/udevmon.service
%define debug_package %{nil}

%changelog
* Thu May 29 2025 Lachlan Marie <lchlnm@pm.me> - 0.6.8-1
- Initial RPM packaging of interception-tools
