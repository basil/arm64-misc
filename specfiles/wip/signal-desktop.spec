#
# spec file for package signal-desktop
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


%global signal_env production
%global pkg_name Signal-Desktop

%global signal_ringrtc_req_version 2.59.4
%global libsignal_req_version 0.83.0
%global sqlcipher_req_version 2.4.4

%global nodejs_includedir %{_includedir}/electron

%global electron_req_version 25~
%global electron_includedir %{_include8dir}/electron

# Do not check for npm requires or provides in app.asar
%global __provides_exclude ^npm(.*)|^nodejs(.*)
%global __requires_exclude ^npm(.*)|^nodejs(.*)



#Both electron and webrtc require SSE2 on the x86 port. So we can require SSE2 on all other code, too.
%ifarch %ix86
ExclusiveArch:  i586 i686
BuildArch:      i686
%{expand:%%global optflags %(echo "%optflags") -march=pentium4 -mtune=generic}
%{expand:%%global build_rustflags %(echo "%build_rustflags") -C target-cpu=pentium4 -Z tune-cpu=generic}
%endif

#Whether to apply fixes so that libsignal_tokenizer gets compiled with LTO.
# On Leap the system LLVM is too old.
%if 0%{?suse_version} >= 1550 || 0%{?sle_version} >= 150700 || (0%{?fedora} && 0%{?fedora} != 41)
# FC41: “Expected at most one ThinLTO module per bitcode file” (bsc#1229988)
%bcond_without llvm_lto
%else
%bcond_with llvm_lto
%endif


Name:           signal-desktop
Version:        7.79.0
Release:        0
Summary:        Fast, simple and secure messaging app from your desktop
License:        AGPL-3.0-only and MIT and (MIT or CC0-1.0) and Apache-2.0 and BSD-3-Clause and ISC and SUSE-Public-Domain
Group:          Productivity/Networking/Instant Messenger
Url:            https://github.com/signalapp/Signal-Desktop/
#
Source0:        https://github.com/signalapp/Signal-Desktop/archive/v%{version}/%{pkg_name}-%{version}.tar.gz
Source1:        vendor.tar.zst
Source2:        %{name}.desktop

# PATCHES for distro-specific things (compiler flags, paths, etc.)
Patch0:         sqlcipher-install.patch
# Do not try to patch the electron executable
Patch9:         remove-fuses.patch
Patch29:        no-comments-pretty-printing-and-sourcemaps.patch
Patch32:        mocha-increase-timeout.patch
Patch33:        test-mock-flaky.patch
Patch34:        7za-path.patch
Patch35:        AttachmentBackupManager_test-skip.patch
Patch36:        resolveCanonicalLocales_test-skip.patch
Patch37:        migration_1100_test-flaky.patch
Patch38:        locale-isPackaged.patch
Patch39:        electron-winstaller-install.patch
Patch40:        electron-builder-no-pnpm.patch
Patch41:        shut-up-lightningcss.patch
Patch43:        messages_test-skip.patch

#PATCHES that remove code we don't want
# Remove HEIC support from main.js
Patch502:         signal-desktop-remove-heif-support.patch
# Do not distribute bogus dev tool in package
# Code loaded in renderer process is webpecked, but the one in main process unfortunately isnt.
# This means we ship the same code twice. Ouch. (Probably some files in ts/ are also not needed, which means we could slim this further)
Patch505:         Remove-build-time-dependencies.patch

# PATCHES to use system libs
# Inter font is available on both SUSE and Fedora
Patch1006:        system-fonts.patch
Patch1020:        ringrtc-no-download.patch

#PATCHES that fix interaction with other software
Patch2000:        scrollUtil_test-disable.patch

# PATCHES that can be submitted upstream verbatim or near-verbatim
# Workaround for https://github.com/signalapp/Signal-Desktop/issues/5616
Patch3003:        0001-ts-log-Avoid-log-spam-for-ResizeObserver-loop-limit-.patch
Patch3004:        tailwindcss-oxide-requireNative.patch


# PATCHES that correct upstream hostility (DRM etc.) or force-disabled features
# There's no sense in submitting them but they may be reused as-is by other distros.
Patch5007:        esbuild_version.patch
Patch5021:        system-esbuild.patch




#

#
BuildRequires:  app-builder

 #There are major API breaks between 0.16 and 0.17.
BuildRequires:  esbuild >= 0.17
BuildRequires:  fdupes
%if 0%{?suse_version} > 1500 || 0%{?fedora_version}
BuildRequires:  gcc-c++ >= 11
%else
BuildRequires:  gcc13-PIE
BuildRequires:  gcc13-c++
%endif
BuildRequires:  hicolor-icon-theme
BuildRequires:  jq
BuildRequires:  make
BuildRequires:  nodejs-packaging
BuildRequires:  nodejs-electron-devel >= %{electron_req_version}


BuildRequires:  signal-libringrtc = %{signal_ringrtc_req_version}
BuildRequires:  libsignal = %{libsignal_req_version}
BuildRequires:  signal-sqlcipher = %{sqlcipher_req_version}
%if 0%{?fedora} >= 37
BuildRequires:  nodejs-npm
%else
BuildRequires:  npm
%endif
%if 0%{?suse_version}

%if 0%{?suse_version} >= 1550 || 0%{?sle_version} >= 150700
BuildRequires:  python3-base
%else
BuildRequires:  python311-base
%endif
BuildRequires:  update-desktop-files
%else
BuildRequires:  python3
%endif

BuildRequires: tailwind-oxide

BuildRequires: fontpackages-devel
%if 0%{?fedora_version}
%define _ttfontsdir %{_datadir}/fonts/truetype
%endif

#for tests
%ifnarch riscv64 aarch64 %ix86
%if 0%{?fedora}
BuildRequires:  Xvfb
%else
BuildRequires:  xvfb-run
%endif
%endif

BuildRequires:  zstd

#
Requires: nodejs-electron%{_isa}
Requires:       signal-libringrtc%{_isa} = %{signal_ringrtc_req_version}
Requires:       libsignal%{_isa} = %{libsignal_req_version}
Requires:       signal-sqlcipher%{_isa} = %{sqlcipher_req_version}
Requires:       (font(inter) or inter-fonts)


#Support upgrading from old RPM versions which had separate langpacks.
#We cannot do that anymore as signal now aborts when the langpack is missing instead of gracefully falling back to english.

%define lang_subpkg() \
Provides:  signal-desktop-langpack-%{1} = %{version}\
Obsoletes: signal-desktop-langpack-%{1} < %{version}

%lang_subpkg af af-ZA Afrikaans
%lang_subpkg ar ar    Arabic
%lang_subpkg az az-AZ Azerbaijani
%lang_subpkg bg bg-BG Bulgarian
%lang_subpkg bn bn-BD Bengali
%lang_subpkg bs bs-BA Bosnian
%lang_subpkg ca ca    Catalan
%lang_subpkg cs cs    Czech
%lang_subpkg da da    Danish
%lang_subpkg de de    German
%lang_subpkg el el    Greek
%lang_subpkg es es    Spanish
%lang_subpkg et et-EE Estonian
%lang_subpkg eu eu    Basque
%lang_subpkg fa fa-IR Persian
%lang_subpkg fi fi    Finnish
%lang_subpkg fr fr    French
%lang_subpkg ga ga-IE Irish
%lang_subpkg gl gl-ES Galician
%lang_subpkg gu gu-IN Gujarati
%lang_subpkg he he    Hebrew
%lang_subpkg hi hi-IN Hindi
%lang_subpkg hr hr-HR Croatian
%lang_subpkg hu hu    Hungarian
%lang_subpkg id id    Indonesian
%lang_subpkg it it    Italian
%lang_subpkg ja ja    Japanese
%lang_subpkg ka ka-GE Georgian
%lang_subpkg kk kk-KZ Kazakh
%lang_subpkg km km-KH Khmer
%lang_subpkg kn kn-IN Kannada
%lang_subpkg ko ko    Korean
%lang_subpkg ky ky-KG Kirghiz
%lang_subpkg lt lt-LT Lithuanian
%lang_subpkg lv lv-LV Latvian
%lang_subpkg mk mk-MK Macedonian
%lang_subpkg ml ml-IN Malayalam
%lang_subpkg mr mr-IN Marathi
%lang_subpkg ms ms    Malay
%lang_subpkg my my    Burmese
%lang_subpkg nb nb    %{quote:Norwegian Bokmal}
%lang_subpkg nl nl    Dutch
%lang_subpkg pa pa-IN Panjabi
%lang_subpkg pl pl    Polish
%lang_subpkg pt_BR pt-BR %{quote:Brazilian Portuguese}
%lang_subpkg pt_PT pt-PT %{quote:European Portuguese}
%lang_subpkg ro ro-RO Romanian
%lang_subpkg ru ru    Russian
%lang_subpkg sk sk-SK Slovak
%lang_subpkg sl sl-SI Slovenian
%lang_subpkg sq sq-AL Albanian
%lang_subpkg sr sr-RS Serbian
%lang_subpkg sv sv    Swedish
%lang_subpkg sw sw    Swahili
%lang_subpkg ta ta-IN Tamil
%lang_subpkg te te-IN Telugu
%lang_subpkg th th    Thai
%lang_subpkg tl tl-PH Tagalog
%lang_subpkg tr tr    Turkish
%lang_subpkg ug ug    Uighur
%lang_subpkg uk uk-UA Ukrainian
%lang_subpkg ur ur    Urdu
%lang_subpkg vi vi    Vietnamese
%lang_subpkg yue yue  Cantonese
%lang_subpkg zh_CN zh-CN %{quote:Simplified Chinese}
%lang_subpkg zh_HK zh-HK %{quote:Chinese (Hong Kong)}
Obsoletes:      signal-desktop-langpack-cy < %version
Obsoletes:      signal-desktop-langpack-eo < %version
Obsoletes:      signal-desktop-langpack-fil < %version
Obsoletes:      signal-desktop-langpack-gd < %version
Obsoletes:      signal-desktop-langpack-is < %version
Obsoletes:      signal-desktop-langpack-ku < %version
Obsoletes:      signal-desktop-langpack-lo < %version
Obsoletes:      signal-desktop-langpack-nn < %version
Obsoletes:      signal-desktop-langpack-no < %version
Obsoletes:      signal-desktop-langpack-ps < %version
Obsoletes:      signal-desktop-langpack-ug < %version
Obsoletes:      signal-desktop-langpack-yue < %version
Obsoletes:      signal-desktop-langpack-zh_TW < %version





#
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Signal Desktop is an Electron application that links with your Signal Android
or Signal iOS app.

%prep
%autosetup -p1 -n %{pkg_name}-%{version} -a 1


#Remove second libsignal copy we don't have control over. It is only used in tests
rm -rf node_modules/@signalapp/mock-server/node_modules/@signalapp/libsignal-client

#Sanity check that we've declared the correct version in header
test $(jq -cj '.version' node_modules/@signalapp/libsignal-client/package.json) = %{libsignal_req_version}
test $(jq -cj '.version' node_modules/@signalapp/ringrtc/package.json) = %{signal_ringrtc_req_version}
test $(jq -cj '.version' node_modules/@signalapp/sqlcipher/package.json) = %{sqlcipher_req_version}

# Remove HEIC releated files. We don't have heic-convert.
rm -f ts/heic-convert.d.ts
rm -f ts/workers/heicConverterMain.ts
rm -f ts/workers/heicConverterWorker.ts

#Remove vendored font, we use the system copy
rm -rf fonts/inter-v3.19

#Do not install font privately
mv -v fonts/signal-symbols/SignalSymbolsVariable.woff2 %{_builddir}
rmdir -v fonts/signal-symbols

mkdir -pv %{_builddir}/path
%if 0%{?suse_version} >= 1550 || 0%{?sle_version} >= 150700 || 0%{?fedora}
#ok, system python is new enough
%else
ln -svT %{_bindir}/python3.11 %{_builddir}/path/python3
%endif
#pnpm is required for vendoring, but no need to bring it in for building
cat <<"EOF" > %{_builddir}/path/pnpm
#!/bin/sh
exec npm "$1" "$2" -- "${@:3}"
EOF


chmod +x %{_builddir}/path/pnpm


%build
export PATH="%{_builddir}/path:$PATH"
export CC=gcc
export CXX=g++
export AR=gcc-ar
export NM=gcc-nm
export RANLIB=gcc-ranlib

%if 0%{?suse_version} && 0%{?suse_version} <= 1500
export CC=gcc-13
export CXX=g++-13
export AR=gcc-ar-13
export NM=gcc-nm-13
export RANLIB=gcc-ranlib-13
%endif

#work around bsc#1216691
export SOURCE_DATE_EPOCH="$(stat --printf=%Y LICENSE)"



export CFLAGS="%{optflags} -fpic -fno-semantic-interposition -fno-fat-lto-objects -fvisibility=hidden"
export CXXFLAGS="%{optflags} -fpic -fno-semantic-interposition -fno-fat-lto-objects -fvisibility=hidden"
export MAKEFLAGS="%{_smp_mflags}"





export LDFLAGS="%{?build_ldflags} -Wl,--gc-sections -Wl,-O2 "


export ELECTRON_CACHE=$(pwd)/vendor/cache/electron
export ELECTRON_BUILDER_CACHE=$(pwd)/vendor/cache/electron-builder
export SIGNAL_ENV=%{signal_env}

# node_modules/playwright
export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1
export ELECTRON_SKIP_BINARY_DOWNLOAD=1

export ESBUILD_BINARY_PATH=%{_bindir}/esbuild
export USE_SYSTEM_APP_BUILDER=true

export ELECTRON_OVERRIDE_DIST_PATH=%{_bindir}

export NAPI_RS_NATIVE_LIBRARY_PATH=%{_libdir}/tailwind_oxide.node

# Fix package.json
cp package.json package.json.orig
sed 's#"postinstall": .*##' -i package.json

# Use the system electron for building
electron_version="$(< %{_libdir}/electron/version)"

# Passing `--universal` as the architecture makes the output path predictable.
# Node-gyp rebuild inside electron-builder fails with Node ≥17 (Fedora)
# But we do not need to rebuild anything, since the initial `npm rebuild` is done against Electron in the first place!
sed -i -r 's#("build:electron": ").*"#\1electron-builder --config.extraMetadata.environment=$SIGNAL_ENV --linux dir --universal -c.electronDist=%{_libdir}/electron -c.electronVersion=${electron_version} -c.asar=false -c.nodeGypRebuild=false -c.npmRebuild=false"#' package.json


# Remove HEIF/HEIC support
sed -i '/"heic-convert": .*/d' package.json
sed -i '/".*heicConverter.bundle.js".*/d' package.json

diff -u package.json.orig package.json || true

export npm_config_nodedir="%{nodejs_includedir}"
export npm_config_build_from_source=true



### Rebuild node modules from source



# Copy libringrtc from signal-ringrtc package
mkdir -pv  node_modules/@signalapp/ringrtc/build/linux/
cp -pv %{_libexecdir}/signal-desktop/node_modules/@signalapp/ringrtc/build/linux/*.node -t node_modules/@signalapp/ringrtc/build/linux/
# Copy libsignal-client from libsignal package
mkdir -pv  node_modules/@signalapp/libsignal-client/build/Release/
cp -pv %{_libexecdir}/signal-desktop/node_modules/@signalapp/libsignal-client/build/Release/*.node -t node_modules/@signalapp/libsignal-client/build/Release/
#Copy sqlcipher from package
mkdir -pv node_modules/@signalapp/sqlcipher/build/Release/
cp -pv %{_libexecdir}/signal-desktop/node_modules/@signalapp/sqlcipher/build/Release/*.node -t node_modules/@signalapp/sqlcipher/build/Release/


%electron_rebuild


### Create prerequisites

#compile sticker creator
pushd sticker-creator
npm rebuild --verbose --foreground-scripts
npm run build
popd



npm run generate


### Build

# Create preload cache
# DISABLED THIS: v8 bytecode is not reproducible: https://github.com/signalapp/Signal-Desktop/issues/7028
# xvfb-run -a npm run build:preload-cache
# Run electron-builder
npm run build:release



%install


install -d -m 0755 %{buildroot}%{_bindir}

cat << EOF > %{buildroot}%{_bindir}/signal-desktop
#!/bin/sh
export NODE_ENV=production

exec electron %{_libexecdir}/%{name} "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/signal-desktop

# icons
for i in 16 24 32 48 64 128 256 512 1024; do
    install -d -m 0755 %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/
    install -pm 0644 build/icons/png/${i}x${i}.png %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

# desktop file
install -d -m 0755 %{buildroot}%{_datadir}/applications/
install -pm 0644 %{SOURCE2} %{buildroot}%{_datadir}/applications/%{name}.desktop

#icon font
install -pvDm0644 %{_builddir}/SignalSymbolsVariable.woff2 -t%{buildroot}%{_ttfontsdir}

# Copy the app itself
mkdir -pv %{buildroot}%{_libexecdir}
cp -plr release/linux-universal-unpacked/resources/app %{buildroot}%{_libexecdir}/%{name}

# Copy the native modules that were ignored by electron-builder
find -type f -name '*.node' -print -exec install -pvDm755 {} "%{buildroot}%{_libexecdir}/%{name}/{}" \;





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
find -name '*.mm' -type f -print -delete
find -name '*.ts' -type f -print -delete
find -name '*.cts' -type f -print -delete
find -name '*.mts' -type f -print -delete
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

# this library is shipped by another package we depend on
rm -rf node_modules/@signalapp/{ringrtc,libsignal-client,sqlcipher}/build

# Filter out garbage node_modules leftover from upstream's removal of react-aria etc.
# `npm ls` needs to be called in a loop because extraneous nodules' transitive deps
# aren't marked themselves as extraneous.
while : ; do
extraneous_nodules=$(npm ls --all --omit=dev --parseable --long | grep ':EXTRANEOUS$' | sed 's/:.*//')
if [[ -z "$extraneous_nodules" ]]; then
break
fi
rm -rf $extraneous_nodules
done



# Remove empty directories
find . -type d -empty -print -delete

#Fix file mode
find . -type f -exec chmod 644 {} \;
find . -name '*.node' -exec chmod 755 {} \;

%fdupes %{buildroot}%{_libexecdir}/%{name}


%if 0%{?suse_version}
%suse_update_desktop_file %{name}
%reconfigure_fonts_scriptlets
%endif

%check
%electron_check_native


#rust tests
export PATH="%{_builddir}/path:$PATH"
export CC=gcc
export CXX=g++
export AR=gcc-ar
export NM=gcc-nm
export RANLIB=gcc-ranlib
%if 0%{?suse_version} && 0%{?suse_version} <= 1500
export CC=gcc-13
export CXX=g++-13
export AR=gcc-ar-13
export NM=gcc-nm-13
export RANLIB=gcc-ranlib-13
%endif
export CFLAGS="%{optflags} -fpic -fno-semantic-interposition -fno-fat-lto-objects -fvisibility=hidden"
export CXXFLAGS="%{optflags} -fpic -fno-semantic-interposition -fno-fat-lto-objects -fvisibility=hidden"
export MAKEFLAGS="%{_smp_mflags}"

export LDFLAGS="%{?build_ldflags} -Wl,--gc-sections -Wl,-O2 "

export ELECTRON_OVERRIDE_DIST_PATH=%{_bindir}
export XDG_CONFIG_HOME=$(mktemp -d)
echo --no-sandbox  >> $XDG_CONFIG_HOME/electron-flags.conf
echo --disable-gpu  >> $XDG_CONFIG_HOME/electron-flags.conf
#disable antialias to fix screenshot nondeterminism
mkdir -p $XDG_CONFIG_HOME/fontconfig
cat <<"EOF" >$XDG_CONFIG_HOME/fontconfig/fonts.conf
  <match target="font">
    <edit name="antialias" mode="assign">
      <bool>false</bool>
    </edit>
  </match>
EOF

#Copy values.json back to the worktree to work around locales-app.isPackaged.patch
pushd release/linux-universal-unpacked/resources/app/_locales
find -type f -name values.json -print -exec ln -svfr {} ../../../../../_locales/{} \;
find -type f -name keys.json -print -exec ln -svfr {} ../../../../../_locales/{} \;

popd


#uncomment the below if you wish to debug test failures locally
#export ARTIFACTS_DIR=$(mktemp -d)
%ifnarch %arm riscv64 aarch64 %ix86
#This LONG test actually runs Signal and clicks around the window.
#In general it matters it only passes on one OS/arch since we assume the JS code is identical everywhere.
#It crashes (armv6) or “GPU process isn't usable. Goodbye.” (riscv)
#It timeouts because the machines are slow (aarch64, armv7)

#It works again, but is horribly flaky. Not running this on OBS.
#xvfb-run -a npm run test-mock
%endif

#see "test" in package.json. splitting this to allow individual disabling.
%ifnarch riscv64 aarch64 %ix86
xvfb-run -a npm run test-node
%endif
%ifnarch riscv64 aarch64 %ix86
#hang on armv7, “GPU process isn't usable. Goodbye.” on riscv
xvfb-run -a npm run test-electron
%endif
%ifnarch riscv64 aarch64 %ix86
PATH="%{_libexecdir}/electron-node:$PATH" npm run test-lint-intl
PATH="%{_libexecdir}/electron-node:$PATH" npm run test-eslint
%endif




%ifnarch riscv64 aarch64 %ix86
pushd sticker-creator
PATH="%{_libexecdir}/electron-node:$PATH" npx --offline vitest run
popd
%endif



%files
%defattr(-,root,root)
%doc README.md
%license LICENSE ACKNOWLEDGMENTS.md
%{_bindir}/%{name}

%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/_locales
%{_libexecdir}/%{name}/app
%dir %{_libexecdir}/%{name}/build
%{_libexecdir}/%{name}/build/available-locales.json
%{_libexecdir}/%{name}/build/country-display-names.json
%{_libexecdir}/%{name}/build/dns-fallback.json
%{_libexecdir}/%{name}/build/jumbomoji.json
%{_libexecdir}/%{name}/build/locale-display-names.json
%{_libexecdir}/%{name}/build/optional-resources.json
%{_libexecdir}/%{name}/bundles
%{_libexecdir}/%{name}/config
%{_libexecdir}/%{name}/fonts
%{_libexecdir}/%{name}/images
%{_libexecdir}/%{name}/js
%{_libexecdir}/%{name}/node_modules
%{_libexecdir}/%{name}/sounds
%dir %{_libexecdir}/%{name}/sticker-creator
%{_libexecdir}/%{name}/sticker-creator/dist
%{_libexecdir}/%{name}/stylesheets
%{_libexecdir}/%{name}/ts
%{_libexecdir}/%{name}/package.json
%{_libexecdir}/%{name}/*.bundle.js
#%{_libexecdir}/%{name}/preload.bundle.cache
%{_libexecdir}/%{name}/preload.wrapper.js
%{_libexecdir}/%{name}/*.html

%dir %{_datadir}/icons/hicolor/1024x1024
%dir %{_datadir}/icons/hicolor/1024x1024/apps
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%{_datadir}/applications/%{name}.desktop

%{_ttfontsdir}/

%changelog
