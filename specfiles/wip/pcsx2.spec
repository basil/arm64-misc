Name: pcsx2-qt
Version: 2.5.91
Release: %autorelease
Summary: PCSX2 - The Playstation 2 Emulator

License: GPLv3
URL: https://github.com/PCSX2/pcsx2
Source0: https://github.com/PCSX2/pcsx2/archive/refs/tags/v%{version}.tar.gz

%{lua:
local externals = {
  { name="freetype", ref="42608f7", owner="freetype", path="freetype", version="2.13.3", license="FreeType License" },
  { name="harfbuzz", ref="63cdd74", owner="harfbuzz", path="harfbuzz", version="11.2.0", license="Old MIT" },
  { name="libbacktrace", ref="ad106d5", owner="ianlancetaylor", path="libbacktrace", license="BSD-3-clause" },
  { name="libjpeg-turbo", ref="7723f50", owner="libjpeg-turbo", path="libjpeg-turbo", version="3.1.1", license="IJG+BSD-3-Clause" },
  { name="libpng", ref="2b97891", owner="pnggroup", path="libpng", version="1.6.50", license="PNG Reference Library License version 2" },
  { name="libwebp", ref="a4d7a71", owner="webmproject", path="libwebp", version="1.5.0", license="BSD-3-Clause" },
  { name="lz4", ref="ebb370c", owner="lz4", path="lz4", version="1.10.0", license="BSD-2-Clause+GPLv2+" },
  { name="SDL", ref="68bfcb6", owner="libsdl-org", path="sdl", version="3.2.18", license="Zlib" },
  { name="zstd", ref="f8745da", owner="facebook", path="zstd", version="1.5.7", license="BSD-2-clause" },
  { name="qtbase", ref="2ad23cd", owner="qt", path="qtbase", version="6.9.1", license="*" },
  { name="qtimageformats", ref="71d0613", owner="qt", path="qtimageformats", version="6.9.1", license="*" },
  { name="qtsvg", ref="eac4588", owner="qt", path="qtsvg", version="6.9.1", license="*" },
  { name="qttools", ref="9e8f157", owner="qt", path="qttools", version="6.9.1", license="*" },
  { name="qttranslations", ref="7a90611", owner="qt", path="qttranslations", version="6.9.1", license="*" },
  { name="qtwayland", ref="b54d446", owner="qt", path="qtwayland", version="6.9.1", license="*" },
  { name="shaderc", ref="8c2e602", owner="google", path="shaderc", version="2025.3", license="Apache2" },
  { name="glslang", ref="efd24d7", owner="KhronosGroup", path="shaderc/third_party/glslang", license="BSD-3-clause" },
  { name="SPIRV-Headers", ref="2a611a9", owner="KhronosGroup", path="shaderc/third_party/spirv-headers", version="1.4.321.0", license="MIT" },
  { name="SPIRV-Tools", ref="33e0256", owner="KhronosGroup", path="shaderc/third_party/spirv-tools", version="1.4.321.0", license="Apache2" },
  { name="KDDockWidgets", ref="28d16d0", owner="KDAB", path="KDDockWidgets", version="2.2.3", license="GPLv2" },
  { name="plutovg", ref="1a8412d", owner="sammycage", path="plutovg", version="1.1.0", license="MIT" },
  { name="plutosvg", ref="31f7d26", owner="sammycage", path="plutosvg", version="0.0.7", license="MIT" },
}

for i, s in ipairs(externals) do
  si = 100 + i
  print(string.format("Source%d: https://github.com/%s/%s/archive/%s/%s-%s.tar.gz", si, s.owner, s.name, s.ref, s.name, s.ref).."\n")
  if s.bcond and not rpm.isdefined(string.format("with_%s", s.bcond)) then goto continue1 end
  print(string.format("Provides: bundled(%s) = %s", (s.package or s.name), (s.version or "0")).."\n")
  ::continue1::
end

function print_setup_externals()
  for i, s in ipairs(externals) do
    si = 100 + i
    if s.bcond and not rpm.isdefined(string.format("with_%s", s.bcond)) then goto continue2 end
    print(string.format("mkdir -p deps-build/%s", (s.path or s.name)).."\n")
    print(string.format("tar -xzf %s --strip-components=1 -C deps-build/%s", rpm.expand("%{SOURCE"..si.."}"), (s.path or s.name)).."\n")
    ::continue2::
  end
end
}

BuildRequires: alsa-lib-devel
BuildRequires: brotli-devel
BuildRequires: clang
BuildRequires: cmake
BuildRequires: dbus-devel
BuildRequires: egl-wayland-devel
BuildRequires: extra-cmake-modules
BuildRequires: fontconfig-devel
BuildRequires: gcc-c++
BuildRequires: gtk3-devel
BuildRequires: libaio-devel
BuildRequires: libcurl-devel
BuildRequires: libdecor-devel
BuildRequires: libevdev-devel
BuildRequires: libICE-devel
BuildRequires: libinput-devel
BuildRequires: libpcap-devel
BuildRequires: libSM-devel
BuildRequires: libX11-devel
BuildRequires: libXau-devel
BuildRequires: libxcb-devel
BuildRequires: libXcomposite-devel
BuildRequires: libXcursor-devel
BuildRequires: libXext-devel
BuildRequires: libXfixes-devel
BuildRequires: libXft-devel
BuildRequires: libXi-devel
BuildRequires: libxkbcommon-devel
BuildRequires: libxkbcommon-x11-devel
BuildRequires: libXpresent-devel
BuildRequires: libXrandr-devel
BuildRequires: libXrender-devel
BuildRequires: lld
BuildRequires: llvm
BuildRequires: make
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libGL-devel
BuildRequires: ninja-build
BuildRequires: openssl-devel
BuildRequires: patch
BuildRequires: pcre2-devel
BuildRequires: perl-Digest-SHA
BuildRequires: pipewire-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: systemd-devel
BuildRequires: wayland-devel
BuildRequires: xcb-util-cursor-devel
BuildRequires: xcb-util-devel
BuildRequires: xcb-util-errors-devel
BuildRequires: xcb-util-image-devel
BuildRequires: xcb-util-keysyms-devel
BuildRequires: xcb-util-renderutil-devel
BuildRequires: xcb-util-wm-devel
BuildRequires: xcb-util-xrm-devel
BuildRequires: zlib-devel

%generate_buildrequires


%description
PCSX2 is a free and open-source PlayStation 2 (PS2) emulator. Its purpose is to emulate the PS2's hardware, using a combination of MIPS CPU Interpreters, Recompilers and a Virtual Machine which manages hardware states and PS2 system memory. This allows you to play PS2 games on your PC, with many additional features and benefits.


%prep
%autosetup -n pcsx2-2.5.91

%{lua: print_setup_externals()}


export INSTALLDIR=%{_builddir}/%{buildsubdir}/deps

mkdir -p deps-build
cd deps-build

echo "Building libbacktrace..."
cd "libbacktrace"
./configure --prefix="$INSTALLDIR"
make
make install
cd ..

echo "Building libpng..."
cd "libpng"
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="$INSTALLDIR" -DCMAKE_INSTALL_PREFIX="$INSTALLDIR" -DBUILD_SHARED_LIBS=ON -DBUILD_SHARED_LIBS=ON -DPNG_TESTS=OFF -DPNG_STATIC=OFF -DPNG_SHARED=ON -DPNG_TOOLS=OFF -B build -G Ninja
cmake --build build --parallel
ninja -C build install
cd ..

echo "Building libjpegturbo..."
cd "libjpeg-turbo"
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="$INSTALLDIR" -DCMAKE_INSTALL_PREFIX="$INSTALLDIR" -DENABLE_STATIC=OFF -DENABLE_SHARED=ON -B build -G Ninja
cmake --build build --parallel
ninja -C build install
cd ..

echo "Building LZ4..."
cd "lz4"
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="$INSTALLDIR" -DCMAKE_INSTALL_PREFIX="$INSTALLDIR" -DBUILD_SHARED_LIBS=ON -DLZ4_BUILD_CLI=OFF -DLZ4_BUILD_LEGACY_LZ4C=OFF -B build-dir -G Ninja build/cmake
cmake --build build-dir --parallel
ninja -C build-dir install
cd ..

echo "Building Zstandard..."
cd "zstd"
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="$INSTALLDIR" -DCMAKE_INSTALL_PREFIX="$INSTALLDIR" -DBUILD_SHARED_LIBS=ON -DZSTD_BUILD_SHARED=ON -DZSTD_BUILD_STATIC=OFF -DZSTD_BUILD_PROGRAMS=OFF -B build -G Ninja build/cmake
cmake --build build --parallel
ninja -C build install
cd ..

echo "Building WebP..."
cd "libwebp"
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="$INSTALLDIR" -DCMAKE_INSTALL_PREFIX="$INSTALLDIR" -B build -G Ninja \
  -DWEBP_BUILD_ANIM_UTILS=OFF -DWEBP_BUILD_CWEBP=OFF -DWEBP_BUILD_DWEBP=OFF -DWEBP_BUILD_GIF2WEBP=OFF -DWEBP_BUILD_IMG2WEBP=OFF \
  -DWEBP_BUILD_VWEBP=OFF -DWEBP_BUILD_WEBPINFO=OFF -DWEBP_BUILD_WEBPMUX=OFF -DWEBP_BUILD_EXTRAS=OFF -DBUILD_SHARED_LIBS=ON
cmake --build build --parallel
ninja -C build install
cd ..

echo "Building FreeType without HarfBuzz..."
cd "freetype"
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="$INSTALLDIR" -DCMAKE_INSTALL_PREFIX="$INSTALLDIR" -DBUILD_SHARED_LIBS=ON -DFT_REQUIRE_ZLIB=ON -DFT_REQUIRE_PNG=ON -DFT_DISABLE_BZIP2=TRUE -DFT_DISABLE_BROTLI=TRUE -DFT_DISABLE_HARFBUZZ=TRUE -B build -G Ninja
cmake --build build --parallel
ninja -C build install
cd ..

echo "Building HarfBuzz..."
cd "harfbuzz"
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="$INSTALLDIR" -DCMAKE_INSTALL_PREFIX="$INSTALLDIR" -DBUILD_SHARED_LIBS=ON -DHB_BUILD_UTILS=OFF -DHB_HAVE_FREETYPE=ON -B build -G Ninja
cmake --build build --parallel
ninja -C build install
cd ..

echo "Building FreeType with HarfBuzz..."
cd "freetype"
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="$INSTALLDIR" -DCMAKE_INSTALL_PREFIX="$INSTALLDIR" -DBUILD_SHARED_LIBS=ON -DFT_REQUIRE_ZLIB=ON -DFT_REQUIRE_PNG=ON -DFT_DISABLE_BZIP2=TRUE -DFT_DISABLE_BROTLI=TRUE -DFT_REQUIRE_HARFBUZZ=TRUE -B build -G Ninja
cmake --build build --parallel
ninja -C build install
cd ..

echo "Building SDL..."
cd "sdl"
cmake -B build -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="$INSTALLDIR" -DCMAKE_INSTALL_PREFIX="$INSTALLDIR" -DBUILD_SHARED_LIBS=ON -DSDL_SHARED=ON -DSDL_STATIC=OFF -G Ninja
cmake --build build --parallel
ninja -C build install
cd ..

# Couple notes:
# -fontconfig is needed otherwise Qt Widgets render only boxes.
# -qt-doubleconversion avoids a dependency on libdouble-conversion.
# ICU avoids pulling in a bunch of large libraries, and hopefully we can get away without it.
# OpenGL is needed to render window decorations in Wayland, apparently.
echo "Building Qt Base..."
cd "qtbase"
mkdir build
cd build
../configure -prefix "$INSTALLDIR" -release -dbus-linked -gui -widgets -fontconfig -qt-doubleconversion -ssl -openssl-runtime -opengl desktop -qpa xcb,wayland -xkbcommon -xcb -gtk -- -DFEATURE_dbus=ON -DFEATURE_icu=OFF -DFEATURE_printsupport=OFF -DFEATURE_sql=OFF -DFEATURE_system_png=ON -DFEATURE_system_jpeg=ON -DFEATURE_system_zlib=ON -DFEATURE_system_freetype=ON -DFEATURE_system_harfbuzz=ON
cmake --build . --parallel
ninja install
cd ../../

echo "Building Qt SVG..."
cd "qtsvg"
mkdir build
cd build
"$INSTALLDIR/bin/qt-configure-module" .. -- -DCMAKE_PREFIX_PATH="$INSTALLDIR"
cmake --build . --parallel
ninja install
cd ../../

echo "Building Qt Image Formats..."
cd "qtimageformats"
mkdir build
cd build
"$INSTALLDIR/bin/qt-configure-module" .. -- -DCMAKE_PREFIX_PATH="$INSTALLDIR" -DFEATURE_system_webp=ON
cmake --build . --parallel
ninja install
cd ../../

echo "Building Qt Wayland..."
cd "qtwayland"
mkdir build
cd build
"$INSTALLDIR/bin/qt-configure-module" .. -- -DCMAKE_PREFIX_PATH="$INSTALLDIR"
cmake --build . --parallel
ninja install
cd ../../

echo "Installing Qt Tools..."
cd "qttools"
mkdir build
cd build
"$INSTALLDIR/bin/qt-configure-module" .. -- -DCMAKE_PREFIX_PATH="$INSTALLDIR" -DFEATURE_assistant=OFF -DFEATURE_clang=OFF -DFEATURE_designer=OFF -DFEATURE_kmap2qmap=OFF -DFEATURE_pixeltool=OFF -DFEATURE_pkg_config=OFF -DFEATURE_qev=OFF -DFEATURE_qtattributionsscanner=OFF -DFEATURE_qtdiag=OFF -DFEATURE_qtplugininfo=OFF
cmake --build . --parallel
ninja install
cd ../../

echo "Installing Qt Translations..."
cd "qttranslations"
mkdir build
cd build
"$INSTALLDIR/bin/qt-configure-module" .. -- -DCMAKE_PREFIX_PATH="$INSTALLDIR"
cmake --build . --parallel
ninja install
cd ../../

echo "Building KDDockWidgets..."
cd "KDDockWidgets"
patch -p1 < %{_builddir}/%{buildsubdir}/.github/workflows/scripts/common/kddockwidgets-dodgy-include.patch
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="$INSTALLDIR" -DCMAKE_INSTALL_PREFIX="$INSTALLDIR" -DKDDockWidgets_QT6=true -DKDDockWidgets_EXAMPLES=false -DKDDockWidgets_FRONTENDS=qtwidgets -B build -G Ninja
cmake --build build --parallel
ninja -C build install
cd ..

echo "Building PlutoVG..."
cd "plutovg"
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="$INSTALLDIR" -DCMAKE_INSTALL_PREFIX="$INSTALLDIR" -DBUILD_SHARED_LIBS=ON -DPLUTOVG_BUILD_EXAMPLES=OFF -B build -G Ninja
cmake --build build --parallel
ninja -C build install
cd ..

echo "Building PlutoSVG..."
cd "plutosvg"
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="$INSTALLDIR" -DCMAKE_INSTALL_PREFIX="$INSTALLDIR" -DBUILD_SHARED_LIBS=ON -DPLUTOSVG_ENABLE_FREETYPE=ON -DPLUTOSVG_BUILD_EXAMPLES=OFF -B build -G Ninja
cmake --build build --parallel
ninja -C build install
cd ..

echo "Building shaderc..."
cd "shaderc"
cd third_party
cd ..
patch -p1 < %{_builddir}/%{buildsubdir}/.github/workflows/scripts/common/shaderc-changes.patch
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_PREFIX_PATH="$INSTALLDIR" -DCMAKE_INSTALL_PREFIX="$INSTALLDIR" -DSHADERC_SKIP_TESTS=ON -DSHADERC_SKIP_EXAMPLES=ON -DSHADERC_SKIP_COPYRIGHT_CHECK=ON -B build -G Ninja
cmake --build build --parallel
ninja -C build install
cd ..
cd ..


%build
export CFLAGS="%{optflags}"
export CFLAGS="${CFLAGS//-flto*/}"
export CFLAGS="${CFLAGS//-ffat-lto-objects/}"
export CFLAGS="${CFLAGS} -fPIC"
export CXXFLAGS="$CFLAGS"
export LDFLAGS="-fuse-ld=lld"

cmake -S %{_builddir}/pcsx2-%{version} \
      -B %{_builddir}/pcsx2-%{version}/redhat-linux-build \
      -DCMAKE_C_COMPILER=clang \
      -DCMAKE_CXX_COMPILER=clang++ \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
      -DCMAKE_PREFIX_PATH=%{_builddir}/pcsx2-%{version}/deps \
      -DCMAKE_EXE_LINKER_FLAGS_INIT="-fuse-ld=lld" \
      -DCMAKE_MODULE_LINKER_FLAGS_INIT="-fuse-ld=lld" \
      -DCMAKE_SHARED_LINKER_FLAGS_INIT="-fuse-ld=lld" \
      -GNinja

ninja -C %{_builddir}/pcsx2-%{version}/redhat-linux-build -v



%install
ninja -C %{_builddir}/pcsx2-%{version}/redhat-linux-build install DESTDIR=%{buildroot}

find %{buildroot}%{_libdir} -name '*.a' -delete


%files
%license LICENSE
%doc README.md CHANGELOG.md

# executables
%{_bindir}/pcsx2
%{_bindir}/pcsx2-qt

# shared libraries
%{_libdir}/libpcsx2.so.*
%{_libdir}/libcommon.so
%{_libdir}/liblibchdr.so
%{_libdir}/librcheevos.so

# desktop integration
%{_datadir}/applications/pcsx2-qt.desktop
%{_datadir}/icons/hicolor/*/apps/pcsx2-qt.png
%{_datadir}/metainfo/pcsx2-qt.appdata.xml

# man page
%{_mandir}/man1/pcsx2.1*

# resources shipped under /usr/share/pcsx2-qt/resources
%{_datadir}/pcsx2-qt/resources/

# translations
%{_datadir}/pcsx2-qt/translations/


%changelog
* Thu May 29 2025 Lachlan Marie <lchlnm@pm.me> - 2.5.91-1
- Initial RPM packaging of pcsx2
