Name:           urserver
Version:        3.13.0.2505
Release:        1%{?dist}
Summary:        Server for universal remote control

License:        Private
URL:            https://www.unifiedremote.com/
Source0:        https://www.unifiedremote.com/download/linux-arm64-portable
Source1:        https://www.unifiedremote.com/download/linux-x64-rpm

BuildRequires:  atool
BuildRequires:  patchelf

%define debug_package      %{nil}

%description
Server for universal remote control

%prep
%setup -qn %{name}-%{version}
aunpack %{SOURCE1}
rm -r linux-x64-rpm/usr/lib
rm    linux-x64-rpm/opt/urserver/urserver
mv    urserver                   linux-x64-rpm/opt/urserver

%build
# no build step for this package

%install
# install /opt and /usr trees
cp -a linux-x64-rpm/opt    %{buildroot}/opt
cp -a linux-x64-rpm/usr    %{buildroot}/usr

# fix RPATH on the main binary
patchelf --remove-rpath %{buildroot}/opt/urserver/urserver
patchelf --set-rpath '$ORIGIN/../lib' %{buildroot}/opt/urserver/urserver

# add symlink into user PATH
mkdir -p %{buildroot}/usr/bin
ln -s /opt/urserver/urserver %{buildroot}/usr/bin/urserver

%files
%defattr(-,root,root,0755)

# core server files
%dir /opt/urserver
/opt/urserver/*

# symlink in PATH
%{_bindir}/urserver

# desktop integration
%{_datadir}/applications/urserver.desktop

# icons
%{_datadir}/pixmaps/urserver.png
%{_datadir}/icons/urserver.png
%{_datadir}/icons/hicolor/48x48/apps/urserver.png
%{_datadir}/icons/hicolor/72x72/apps/urserver.png
%{_datadir}/icons/hicolor/96x96/apps/urserver.png

%changelog
* Thu May 29 2025  Lachlan Marie <lchlnm@pm.me>  - 3.13.0.2505-1
- add /usr/bin/urserver symlink to the main executable
