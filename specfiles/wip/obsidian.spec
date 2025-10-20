Name:           obsidian
Version:        1.8.10
Release:        1%{?dist}
Summary:        Obsidian – a proprietary note-taking and knowledge-base app
License:        Proprietary
URL:            https://obsidian.md
Source0:        https://github.com/obsidianmd/obsidian-releases/releases/download/v%{version}/Obsidian-%{version}-arm64.AppImage

BuildArch:      aarch64
BuildRequires:  bash
BuildRequires:  zlib-ng-compat-devel
Requires:       /usr/bin/env

# disable automatic debuginfo
%define debug_package %{nil}
# suppress auto-Requires from /opt/obsidian and GLIBC symbol-versions
%global __requires_exclude_from ^/opt/obsidian
%global __requires_exclude libc\.so\.6\(GLIBC.*\)

%description
Obsidian is a powerful knowledge-base built on local Markdown files.  This package
unpacks the ARM64 AppImage into /opt/obsidian and provides a system-wide launcher
that applies necessary JavaScript and Wayland flags, plus icons and desktop integration.

%prep
%setup -c -T

%build
# nothing to build

%install
# extract AppImage
mkdir -p %{_builddir}
cp %{SOURCE0} %{_builddir}/
chmod +x %{_builddir}/Obsidian-%{version}-arm64.AppImage
pushd %{_builddir} >/dev/null
./Obsidian-%{version}-arm64.AppImage --appimage-extract
popd >/dev/null

# stage into /opt/obsidian
mkdir -p %{buildroot}/opt/%{name}
cp -a %{_builddir}/squashfs-root/* %{buildroot}/opt/%{name}/
# cleanup redundant icons
rm -f %{buildroot}/opt/%{name}/obsidian.png
rm -rf %{buildroot}/opt/%{name}/usr/share/icons

# create wrapper launcher with JS and Wayland flags
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << 'EOF'
#!/usr/bin/env bash
export ELECTRON_ENABLE_WAYLAND=1
exec /opt/%{name}/obsidian \
    --js-flags="--nodecommit_pooled_pages" \
    --enable-features=UseOzonePlatform \
    --ozone-platform=wayland "$@"
EOF
chmod 755 %{buildroot}%{_bindir}/%{name}

# install and patch desktop file
install -D -m 644 %{buildroot}/opt/%{name}/obsidian.desktop \
    %{buildroot}%{_datadir}/applications/%{name}.desktop
sed -i 's|^Exec=obsidian.*|Exec=%{name} --js-flags="--nodecommit_pooled_pages" --enable-features=UseOzonePlatform --ozone-platform=wayland %U|' \
    %{buildroot}%{_datadir}/applications/%{name}.desktop

# install system icons
mkdir -p %{buildroot}%{_datadir}/icons
cp -a %{_builddir}/squashfs-root/usr/share/icons/hicolor %{buildroot}%{_datadir}/icons/

# document licenses
install -d %{buildroot}%{_docdir}/%{name}
install -m 644 %{buildroot}/opt/%{name}/LICENSE.electron.txt \
    %{buildroot}%{_docdir}/%{name}/
install -m 644 %{buildroot}/opt/%{name}/LICENSES.chromium.html \
    %{buildroot}%{_docdir}/%{name}/

# generate file manifest excluding removed bits
pushd %{buildroot}/opt/%{name} >/dev/null
find . -type f | grep -vE "^\./obsidian.png$|^\./usr/share/icons" | sed 's|^\./|/opt/%{name}/|' > %{_builddir}/filelist.txt
popd >/dev/null

%files -f %{_builddir}/filelist.txt
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%doc %{_docdir}/%{name}/LICENSE.electron.txt
%doc %{_docdir}/%{name}/LICENSES.chromium.html
%dir /opt/%{name}

%changelog
* Sun Jun 08 2025 Lach <lach@example.com> - 1.8.10-2
- add Wayland support flags (ELECTRON_ENABLE_WAYLAND, --enable-features, --ozone-platform)
- update wrapper and desktop Exec lines
