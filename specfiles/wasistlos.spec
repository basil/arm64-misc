Name: wasistlos
Version: 1.7.0
Release: 1%{?dist}
Summary: An unofficial WhatsApp desktop application for Linux.

License: GNU GPL v3
URL:     https://github.com/xeco23/WasIstLos
Source0: %{url}/archive/v%{version}/wasistlos-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: pkgconfig
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: gtk-layer-shell-devel
BuildRequires: gtkmm3.0-devel
BuildRequires: webkit2gtk4.1-devel
BuildRequires: libayatana-appindicator-gtk3-devel
BuildRequires: libcanberra-devel


%description
An unofficial WhatsApp desktop application for Linux.


%prep
%autosetup -n WasIstLos-1.7.0


%build
%cmake
%cmake_build


%install
%cmake_install


%files
%license LICENSE
%doc    README.md

%{_bindir}/wasistlos

%{_datadir}/applications/com.github.xeco23.WasIstLos.desktop
%{_datadir}/metainfo/com.github.xeco23.WasIstLos.appdata.xml

%{_datadir}/icons/hicolor/*/apps/com.github.xeco23.WasIstLos.png
%{_datadir}/icons/hicolor/*/status/com.github.xeco23.WasIstLos-tray*.png

%lang(bn)       %{_datadir}/locale/bn/LC_MESSAGES/wasistlos.mo
%lang(cs)       %{_datadir}/locale/cs/LC_MESSAGES/wasistlos.mo
%lang(de)       %{_datadir}/locale/de/LC_MESSAGES/wasistlos.mo
%lang(es)       %{_datadir}/locale/es/LC_MESSAGES/wasistlos.mo
%lang(fr)       %{_datadir}/locale/fr/LC_MESSAGES/wasistlos.mo
%lang(hu)       %{_datadir}/locale/hu/LC_MESSAGES/wasistlos.mo
%lang(it)       %{_datadir}/locale/it/LC_MESSAGES/wasistlos.mo
%lang(ka)       %{_datadir}/locale/ka/LC_MESSAGES/wasistlos.mo
%lang(nl)       %{_datadir}/locale/nl/LC_MESSAGES/wasistlos.mo
%lang(pl)       %{_datadir}/locale/pl/LC_MESSAGES/wasistlos.mo
%lang(pt_BR)    %{_datadir}/locale/pt_BR/LC_MESSAGES/wasistlos.mo
%lang(ru)       %{_datadir}/locale/ru/LC_MESSAGES/wasistlos.mo
%lang(si)       %{_datadir}/locale/si/LC_MESSAGES/wasistlos.mo
%lang(tr)       %{_datadir}/locale/tr/LC_MESSAGES/wasistlos.mo
%lang(uk)       %{_datadir}/locale/uk/LC_MESSAGES/wasistlos.mo
%lang(zh_Hans)  %{_datadir}/locale/zh_Hans/LC_MESSAGES/wasistlos.mo


%changelog
* Wed Jul 23 2025 Lachlan Marie <lchlnm@pm.me> - 1.7.0-1
- Initial RPM packaging of wasistlos
