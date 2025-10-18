%global appname        standard-notes
%global appdir         /opt/Standard-Notes

# Disable automatic debuginfo/debugsource sub‑packages (Electron binaries have no useful symbols)
%undefine _debuginfo_subpackages   # rpm ≥ 4.18
%undefine _debugsource_packages    # rpm ≥ 4.17
%global  debug_package %{nil}

Name:           standard-notes
Version:        3.196.8
Release:        1%{?dist}
Summary:        End‑to‑end encrypted notes application (desktop client)

License:        MIT
URL:            https://github.com/standardnotes/app
Source0:        https://github.com/standardnotes/app/archive/refs/tags/@standardnotes/desktop@%{version}.tar.gz

# ── build dependencies ────────────────────────────────────────────────────────
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  nodejs
BuildRequires:  yarnpkg
BuildRequires:  npm
BuildRequires:  pkgconfig
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libXtst-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXext-devel
BuildRequires:  libnotify-devel
BuildRequires:  nss-devel
BuildRequires:  xdg-utils
BuildRequires:  chromium
BuildRequires:  git
BuildRequires:  ruby

# The Electron runtime needs these at run time as well
Requires:       gtk3
Requires:       libnotify
Requires:       nss
Requires:       libXScrnSaver
Requires:       libXtst
Requires:       xdg-utils
Requires:       at-spi2-core
Requires:       libuuid

# ── description ───────────────────────────────────────────────────────────────
%description
Standard Notes is a simple and private notes app that features end‑to‑end
encryption and an extension ecosystem. This package ships the official
Electron‑based desktop client.

# ── prep phase ────────────────────────────────────────────────────────────────
%prep
%setup -qn app--standardnotes-desktop-%{version}

# Install fpm into an isolated GEM_HOME so electron‑builder can invoke it
gem install fpm

# ── build phase ───────────────────────────────────────────────────────────────
%build
ulimit -n 4096  # Electron needs a high descriptor limit
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

export CC=gcc
export CXX=g++

yarn install --frozen-lockfile
yarn build:desktop

# Upstream productName → FHS‑compliant hyphenated form
sed -i 's/"Standard Notes"/"standard-notes"/g' packages/desktop/app/package.json

pushd packages/desktop
export PATH="/usr/bin:$PATH"
export PATH="/builddir/bin:$PATH"
export USE_SYSTEM_FPM=true
yarn run electron-builder --linux rpm --publish never


# ── install phase ─────────────────────────────────────────────────────────────
%install
rm -rf %{buildroot}
aunpack packages/desktop/dist/standard-notes-3.108.192-linux-aarch64.rpm
mkdir -p %{buildroot}/opt
mkdir -p %{buildroot}/usr
cp -a %{name}-3.108.192-linux-aarch64/opt %{buildroot}
cp -a %{name}-3.108.192-linux-aarch64/usr %{buildroot}


# Wrapper script instead of an absolute symlink
install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{appname} << 'EOF'
#!/bin/sh
exec /opt/Standard-Notes/standard-notes "$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/%{appname}

# Desktop entry & icon
install -Dm0644 standard-notes-3.108.192-linux-aarch64/usr/share/icons/hicolor/512x512/apps/%{appname}.png \
        %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{appname}.png
install -Dm0644 standard-notes-3.108.192-linux-aarch64/usr/share/applications/%{appname}.desktop \
        %{buildroot}%{_datadir}/applications/%{appname}.desktop

# ── file list ────────────────────────────────────────────────────────────────
%files
# Licences first (see Fedora packaging guidelines)
%license %{appdir}/LICENSE.electron.txt
%license %{appdir}/LICENSES.chromium.html

# Avoid duplication with wildcard below
%exclude %{appdir}/LICENSE.electron.txt
%exclude %{appdir}/LICENSES.chromium.html

# Entire application tree
%dir %{appdir}
%{appdir}/*

# Launcher & desktop integration
%{_bindir}/%{appname}
%{_datadir}/applications/%{appname}.desktop
%{_datadir}/icons/hicolor/512x512/apps/%{appname}.png

# ── changelog ────────────────────────────────────────────────────────────────
%changelog
* Mon Jun 23 2025 Lachlan Marie <lchlnm@pm.me> - 3.196.8-1
- Initial Fedora packaging
- Replaced absolute symlink with wrapper script
- Disabled debugsource/debuginfo sub‑packages
- Prevent duplicate licence entries in %files
