Name: rocketchat-desktop
Version: 4.6.0
Release: 1%{?dist}
Summary: Desktop Client for Rocket.Chat

License:  MIT
URL:      https://github.com/RocketChat/Rocket.Chat.Electron
Source0:  https://github.com/RocketChat/Rocket.Chat.Electron/archive/refs/tags/%{version}.tar.gz
Source1:  rocketchat-desktop-4.6.0-yarn-cache.tar.xz
Source2:  https://github.com/electron/electron/releases/download/v34.0.2/electron-v34.0.2-linux-arm64.zip
Source3:  https://github.com/electron/electron/releases/download/v35.5.1/electron-v35.5.1-linux-arm64.zip


BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  gtk3-devel
BuildRequires:  libX11-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXext-devel
BuildRequires:  libXtst-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libnotify-devel
BuildRequires:  nss-devel
BuildRequires:  rpm-build
BuildRequires:  nodejs
BuildRequires:  yarnpkg
BuildRequires:  pkgconfig
BuildRequires:  xdg-utils
BuildRequires:  npm
BuildRequires:  chromium
BuildRequires:  xorg-x11-server-Xvfb
BuildRequires:  vips
BuildRequires:  vips-devel
BuildRequires:  python3-devel
BuildRequires:  nodejs-devel
BuildRequires:  unzip
# BuildRequires:  nodejs-electron
# BuildRequires:  nodejs-electron-devel

BuildRequires:  vips-devel
BuildRequires:  vips-doc
BuildRequires:  vips-heif
BuildRequires:  vips-jxl
BuildRequires:  vips-magick
BuildRequires:  vips-openslide
BuildRequires:  vips-poppler
BuildRequires:  vips-tools





Requires:       vips
Requires:       python3


%description
Desktop client for Rocket.Chat.

%prep
%autosetup -n Rocket.Chat.Electron-%{version} -N -a 1
sed -i '/downloadSupportedVersions()/d' rollup.config.mjs
cp -p %{SOURCE2} electron-v34.0.2-linux-arm64.zip
cp -p %{SOURCE3} electron.zip
mkdir -p node_modules/electron
unzip -q electron-v34.0.2-linux-arm64.zip -d node_modules/electron/
unzip electron.zip
rm electron.zip

%build
# Don't reach the Internet
export ELECTRON_OVERRIDE_DIST_PATH=%{_bindir}/electron
export ELECTRON_SKIP_BINARY_DOWNLOAD=1
export PUPPETEER_SKIP_DOWNLOAD=1
export SHARP_SKIP_DOWNLOAD=1
export npm_config_nodedir=/usr/
export npm_config_build_from_source=true

yarn install --immutable --immutable-cache
# optional: throw away dev deps to shrink the buildroot
# yarn workspaces focus -A --production
yarn postinstall

yarn build

rm electron-v34.0.2-linux-arm64.zip
%install
install -d -m 0755 %{buildroot}%{_bindir}

cat << EOF > %{buildroot}%{_bindir}/%{name}
#!/bin/sh
export NODE_ENV=production

exec electron %{_libexecdir}/%{name} "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}


#icons
for i in 16 32 48 64 128 256 512; do
    install -d -m 0755 %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/
    install -pm 0644 build/icons/${i}x${i}.png %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

# desktop file
install -d -m 0755 %{buildroot}%{_datadir}/applications/
cat << EOF > %{buildroot}%{_datadir}/applications/%{name}.desktop
[Desktop Entry]
Name=Rocket.Chat
Exec=/usr/bin/rocketchat-desktop %U
Terminal=false
Type=Application
Icon=rocketchat-desktop
StartupWMClass=Rocket.Chat
MimeType=x-scheme-handler/rocketchat;
Comment=Official OSX, Windows, and Linux Desktop Clients for Rocket.Chat
Categories=GNOME;GTK;Network;InstantMessaging;
EOF
chmod +x %{buildroot}%{_datadir}/applications/%{name}.desktop

mkdir -pv %{buildroot}%{_libexecdir}
cp -pr . %{buildroot}%{_libexecdir}/%{name}


#Remove development garbage
cd %{buildroot}%{_libexecdir}/%{name}
#JS debugging symbols
find -name '*.map' -type f -print -delete
#Source code
rm -rf node_modules/@signalapp/libsignal-client/{bin,false,java,rust,swift,vendor,node,ts}
rm -vf  node_modules/@signalapp/libsignal-client/build_node_bridge.py

find -name '*.c' -type f -print -delete
find -name '*.cpp' -type f -print -delete
find -name '*.h' -type f -print -delete
find -name '*.m' -type f -print -delete
find -name '*.ts' -type f -print -delete
find -name '*.tsx' -type f -print -delete
find -name '*.gyp' -type f -print -delete
find -name '*.gypi' -type f -print -delete
find -name tsconfig.json -type f -print -delete
find -name Cargo.lock -type f -print -delete
find -name Cargo.toml -type f -print -delete
find -name '.babel*' -type f -print -delete
find -name '*.flow' -type f -print -delete
find -name bower.json -type f -print -delete
find -name composer.json -type f -print -delete
find -name component.json -type f -print -delete
find -name '*.patch' -type f -print -delete
#Compile-time-only dependencies
find -name nan -print0 |xargs -r0 -- rm -rvf --
find -name node-addon-api -print0 |xargs -r0 -- rm -rvf --
find -name test*.node -type f -print -delete
#Bogus (empty) DLLs which cannot be loaded by node
rm -rfv node_modules/@indutny/simple-windows-notifications/build/Release
#Documentation
find -name '*.markdown' -type f -print -delete
find -name '*.bnf' -type f -print -delete
find -name '*.mli' -type f -print -delete
find -name CHANGES -type f -print -delete
find -name TODO -type f -print -delete
find -name docs -print0 |xargs -r0 -- rm -rvf --
find -name usage.txt -type f -print -delete
#Other garbage
rm -rf build/icons
rm -rf protos
rm -rf release
find -name .cargo -print0 |xargs -r0 -- rm -rvf --
find -name .github -print0 |xargs -r0 -- rm -rvf --
find -name .husky -print0 |xargs -r0 -- rm -rvf --
find -name obj.target -print0 |xargs -r0 -- rm -rvf --
find -name etc -print0 |xargs -r0 -- rm -rvf --
find -name '.eslint*' -type f -print -delete
find -name .editorconfig -type f -print -delete
find -name '.git*' -type f -print -delete
find -name .lint -type f -print -delete
find -name '.jscs*' -type f -print -delete
find -name '.prettier*' -type f -print -delete
find -name '.grenrc*' -type f -print -delete
find -name .airtap.yml -type f -print -delete
find -name .npmrc -type f -print -delete
find -name .nojekyll -type f -print -delete
find -name .nycrc -type f -print -delete
find -name '.taprc*' -type f -print -delete
find -name .testignore -type f -print -delete
find -name '.taplo*' -type f -print -delete
find -name '.nvm*' -type f -print -delete
find -name '.rustfmt*' -type f -print -delete
find -name .flake8 -type f -print -delete
find -name .clippy.toml -type f -print -delete
find -name .bithoundrc -type f -print -delete
find -name '.swift*' -type f -print -delete
find -name .testem.json -type f -print -delete
find -name '*travis*.yml' -type f -print -delete
find -name rust-toolchain -type f -print -delete
find -name '*.podspec' -type f -print -delete
find -name '*~' -type f -print -delete
find -name '*.bak' -type f -print -delete
find -name sri-history.json -type f -print -delete
find -name Dockerfile -type f -print -delete
find -name docker-prebuildify.sh -type f -print -delete
find -name justfile -type f -print -delete

#Remove tests
rm -rf ts/test-{both,electron,mock,node}


%files
%define debug_package %{nil}

%defattr(-,root,root)
%doc README.md
%license LICENSE
%{_bindir}/%{name}

%{_libexecdir}/%{name}

%dir %{_datadir}/icons/hicolor/512x512
%dir %{_datadir}/icons/hicolor/512x512/apps
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%{_datadir}/applications/%{name}.desktop




%changelog
* Thu Jun 26 2025 Lachlan Marie <lchlnm@pm.me> - 4.6.0-1
- Bumped version to 4.6.0

* Sun Jun 08 2025 Lachlan Marie <lchlnm@pm.me> - 4.1.2-2
- Restructured packaging process

* Wed Jun 04 2025 Lachlan Marie <lchlnm@pm.me> - 4.1.2-1
- Create /usr/bin before symlink
- Sync Version/Changelog to 4.1.2
