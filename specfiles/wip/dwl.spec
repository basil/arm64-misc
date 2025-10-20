Name: dwl
Version: 0.7.1
Release: 1%{?dist}
Summary: DWM for Wayland

License: GNU GPL 3
URL: https://github.com/lacamar/dwl
Source0: https://github.com/lacamar/dwl/archive/refs/tags/0.7.1.tar.gz

BuildRequires: make
BuildRequires: gcc
BuildRequires: pkgconfig
BuildRequires: wayland-protocols-devel
BuildRequires: libinput
BuildRequires: libwayland-client
BuildRequires: libwayland-cursor
BuildRequires: libwayland-egl
BuildRequires: libwayland-server
BuildRequires: wlroots-devel
BuildRequires: libxcb-devel
BuildRequires: xcb-util-wm
BuildRequires: libxkbcommon-devel
BuildRequires: wlr-protocols-devel

Requires: libxkbcommon
Requires: libinput
Requires: libwayland-client
Requires: libwayland-cursor
Requires: libwayland-egl
Requires: libwayland-server
Requires: wlroots
Requires: libxcb
Requires: xcb-util-wm
Requires: xorg-x11-server-Xwayland

%description
DWM for Wayland

%prep
%autosetup

%build
make

%install
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}


%files
%license LICENSE
%doc README.md
%define debug_package %{nil}

%{_bindir}/dwl
%{_datadir}/man/man1/dwl.1.gz
%{_datadir}/wayland-sessions/dwl-uwsm.desktop
%{_datadir}/wayland-sessions/dwl.desktop



%changelog
* Wed Jun 25 2025 Lachlan Marie <lchlnm@pm.me> - 0.7.1-1
- Initial RPM packaging of DWL
