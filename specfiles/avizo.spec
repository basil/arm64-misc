Name:     avizo
Version:  1.3
Release:  1%{?dist}
Summary:  A neat notification daemon

License: GNU GPL v3
URL: https://github.com/heyjuvi/avizo
Source0: https://github.com/heyjuvi/avizo/archive/refs/tags/%{version}.tar.gz

BuildRequires: boost
BuildRequires: cmake
BuildRequires: pkgconfig
BuildRequires: meson
BuildRequires: gcc
BuildRequires: vala
BuildRequires: gtk3-devel
BuildRequires: gtk-layer-shell-devel

Requires: pamixer
Requires: pulseaudio-utils
Requires: brightnessctl

%description
Avizo is a simple notification daemon, mainly intended to be used for multimedia keys for example with Sway.

%prep
%autosetup

%build
meson setup build \
    -Dbuildtype=release \
    -Dprefix=%{_prefix}
ninja -C build

%install
DESTDIR=%{buildroot} ninja -C build install



%files
%license LICENSE
%doc README.md
%define debug_package %{nil}

%config(noreplace) %{_sysconfdir}/xdg/avizo/config.ini

%{_bindir}/avizo-client
%{_bindir}/avizo-service
%{_bindir}/lightctl
%{_bindir}/volumectl


%changelog
* Thu May 29 2025 Lachlan Marie <lchlnm@pm.me> - 1.3-1
- Initial RPM packaging of avizo
