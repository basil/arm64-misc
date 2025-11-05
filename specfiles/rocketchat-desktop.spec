Name: rocketchat-desktop
Version: 4.9.1
Release: %autorelease
Summary: Desktop Client for Rocket.Chat

%global electron_version 37.6.0


License:  MIT
URL:      https://github.com/RocketChat/Rocket.Chat.Electron
Source0:  https://github.com/RocketChat/Rocket.Chat.Electron/archive/refs/tags/%{version}.tar.gz
Source1:  rocketchat-desktop-%{version}-yarn-cache.tar.xz
Source2:  https://github.com/electron/electron/releases/download/v%{electron_version}/electron-v%{electron_version}-linux-arm64.zip

ExclusiveArch:  aarch64

BuildRequires:  gcc-c++
BuildRequires:  yarnpkg
BuildRequires:  chromium
BuildRequires:  vips-devel
BuildRequires:  nodejs-devel
Requires:       nodejs-electron >= %{electron_version}


%description
Desktop client for Rocket.Chat.

%prep
%autosetup -n Rocket.Chat.Electron-%{version} -N -a 1
sed -i '/downloadSupportedVersions()/d' rollup.config.mjs
mkdir -p node_modules/electron
unzip -q %{SOURCE2} -d node_modules/electron/

%build
export ELECTRON_OVERRIDE_DIST_PATH=%{_bindir}/electron
export ELECTRON_SKIP_BINARY_DOWNLOAD=1
export PUPPETEER_SKIP_DOWNLOAD=1
export SHARP_SKIP_DOWNLOAD=1
export npm_config_nodedir=/usr/
export npm_config_build_from_source=true

yarn install --immutable --immutable-cache
yarn postinstall
yarn build

%install
install -d -m 0755 %{buildroot}%{_bindir}

cat << EOF > %{buildroot}%{_bindir}/%{name}
#!/usr/bin/env sh
export NODE_ENV=production

if [ "$XDG_SESSION_TYPE" = "wayland" ] || [ -n "$WAYLAND_DISPLAY" ]; then
  export ELECTRON_OZONE_PLATFORM_HINT=wayland
else
  export ELECTRON_OZONE_PLATFORM_HINT=x11
fi

exec /usr/bin/electron /usr/libexec/rocketchat-desktop "$@"
EOF

chmod +x %{buildroot}%{_bindir}/%{name}

for i in 16 32 48 64 128 256 512; do
    install -d -m 0755 %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/
    install -pm 0644 build/icons/${i}x${i}.png %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

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

mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -p package.json %{buildroot}%{_libexecdir}/%{name}/package.json
cp -pr node_modules %{buildroot}%{_libexecdir}/%{name}/node_modules
cp -pr app          %{buildroot}%{_libexecdir}/%{name}/app

rm -fr  %{buildroot}%{_libexecdir}/%{name}/node_modules/7zip-bin/linux/arm/7za
rm -fr  %{buildroot}%{_libexecdir}/%{name}/node_modules/7zip-bin/linux/ia32/7za
rm -fr  %{buildroot}%{_libexecdir}/%{name}/node_modules/7zip-bin/linux/x64/7za
rm -fr  %{buildroot}%{_libexecdir}/%{name}/node_modules/bare-fs/prebuilds/linux-x64/bare-fs.bare
rm -fr  %{buildroot}%{_libexecdir}/%{name}/node_modules/bare-os/prebuilds/linux-x64/bare-os.bare


cd %{buildroot}%{_libexecdir}/%{name}

rm -rf %{buildroot}%{_libexecdir}/%{name}/node_modules/{app-builder-bin,electron,electron-builder,@electron/rebuild,@electron/get,puppeteer,playwright,ts-node,typescript,@typescript-eslint,eslint*,prettier,jest*,@jest,vitest,mocha,chai,nyc,rollup,webpack*,parcel*,node-gyp,prebuild-install,patch-package,lint-*,stylelint*,conventional-*,commitlint*,husky,vercel,es-abstract,app-builder-lib,builder-util,builder-util-runtime,dmg-builder,electron-devtools-installer,@octokit,babel-jest,babel-preset-jest,babel-plugin-istanbul,babel-plugin-jest-hoist,@istanbuljs,istanbul-lib-*,istanbul-reports,v8-to-istanbul,test-exclude,ts-jest,@types,tsutils,@tsconfig,tsconfig-paths,@eslint,@eslint-community,jsx-ast-utils,espree,esprima,doctrine,git-raw-commits,git-semver-tags,xvfb-maybe,electron-notarize,electron-publish,devtools-protocol,chromium-bidi,puppeteer-core,@puppeteer,7zip-bin,uglify-js,@rollup,rollup-plugin-copy,@actions}

find -name '*.map' -type f -print -delete
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

find -name nan -print0 |xargs -r0 -- rm -rvf --
find -name node-addon-api -print0 |xargs -r0 -- rm -rvf --
find -name test*.node -type f -print -delete

rm -rfv node_modules/@indutny/simple-windows-notifications/build/Release

find -name '*.markdown' -type f -print -delete
find -name '*.bnf' -type f -print -delete
find -name '*.mli' -type f -print -delete
find -name CHANGES -type f -print -delete
find -name TODO -type f -print -delete
find -name docs -print0 |xargs -r0 -- rm -rvf --
find -name usage.txt -type f -print -delete

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

find %{buildroot}%{_libexecdir}/%{name}/node_modules \
  -type d \
  \( -name test -o -name tests -o -name __tests__ -o -name example -o -name examples \
     -o -name docs -o -name doc -o -name coverage -o -name benchmark -o -name benchmarks \
     -o -name demo -o -name demos -o -name mac -o -name win \) \
  -prune -exec rm -rf {} +

find %{buildroot}%{_libexecdir}/%{name}/node_modules -type f \
  \( -name '*.map' -o -name '*.d.ts' -o -name '*.d.mts' -o -name '*.tsbuildinfo' \) -delete

find %{buildroot}%{_libexecdir}/%{name}/node_modules/sharp -type d -path '*/vendor/*' \
  -not -path '*/vendor/8.*/linux-arm64*' -exec rm -rf {} + 2>/dev/null || true

find %{buildroot}%{_libexecdir}/%{name}/node_modules -type d -path '*/prebuilds/*' \
  -not -path '*/prebuilds/linux-arm64*' -exec rm -rf {} + 2>/dev/null || true

find %{buildroot}%{_libexecdir}/%{name}/node_modules -type f -name '*.node' -print0 \
  | xargs -0 -r file | grep -Ev 'ELF 64-bit.*aarch64' | cut -d: -f1 | xargs -r rm -f

rm -rf %{buildroot}%{_libexecdir}/%{name}/node_modules/**/node_gyp_bins 2>/dev/null || true

rm -rf %{buildroot}%{_libexecdir}/%{name}/app/images/tray/{darwin,win32} \
       %{buildroot}%{_libexecdir}/%{name}/app/images/icon.ico


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
%autochangelog
