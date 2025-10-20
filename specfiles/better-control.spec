Name: better-control
Version:        6.12.1
Release:        1%{?dist}
Summary:        A simple control panel for linux based on the GTK framework

License: GNU GPL v3
URL: https://github.com/better-ecosystem/better-control
Source0: https://github.com/better-ecosystem/better-control/archive/refs/tags/v%{version}.tar.gz
BuildRequires: make

Requires: gtk3
Requires: python3-gobject
Requires: NetworkManager
Requires: bluez
Requires: pulseaudio-utils
Requires: python3-dbus
Requires: python3
Requires: gammastep
Requires: python3-requests
Requires: python3-qrcode
Requires: python3-setproctitle
Requires: python3-pillow
Requires: usbguard
Requires: brightnessctl


%description
A simple control panel for linux based on the GTK framework

%prep
%autosetup

%build


%install
make install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{_datadir}/better-control/*
%{_bindir}/better-control
%{_bindir}/control
%{_bindir}/betterctl
%{_datadir}/applications/better-control.desktop
%define debug_package %{nil}


%changelog
* Fri Jun 06 2025 Lachlan Marie <lchlnm@pm.me> - 6.12.1-1
- Initial RPM packaging of better-control
