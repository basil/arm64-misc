Name:           rpcs3
Version:        0.0.37
Release:        %autorelease
Summary:        PlayStation 3 emulator and debugger

License: GPLv2
URL:      https://github.com/RPCS3/rpcs3
Source0:  https://github.com/RPCS3/rpcs3/archive/refs/tags/v%{version}.tar.gz

%{lua:
local externals = {
 { name="7zip", ref="e5431fa", owner="ip7z", path="7zip/7zip", version="24.09",  license="GNU-LGPL" },
 { name="FAudio", ref="6077ea7", owner="FNA-XNA", path="FAudio", version="25.05",  license="zlib" },
 { name="VulkanMemoryAllocator", ref="1d8f600", owner="GPUOpen-LibrariesAndSDKs", path="GPUOpen/VulkanMemoryAllocator", version="3.3.0",  license="MIT" },
 { name="openal-soft", ref="dc7d705", owner="kcat", path="OpenAL/openal-soft", version="1.24.3",  license="PFFFT" },
 { name="soundtouch", ref="3982730", owner="RPCS3", path="SoundTouch/soundtouch/", version="2.4.0",  license="LGPLv2.1" },
 { name="asmjit", ref="416f735", owner="asmjit", path="asmjit/asmjit/", license="zlib" },
 { name="cubeb", ref="70b4e3d", owner="mozilla", path="cubeb/cubeb", license="ISC" },
 { name="curl", ref="4dacb79", owner="curl", path="curl/curl", version="8.14.0",  license="MIT" },
 { name="discord-rpc", ref="3dc2c32", owner="Vestrel", path="discord-rpc/discord-rpc", license="MIT" },
 { name="ffmpeg-core", ref="ec6367d", owner="RPCS3", path="ffmpeg", license="LGPLv2.1" },
 { name="flatbuffers", ref="595bf00", owner="google", path="flatbuffers", version="24.3.25",  license="Apache-v2" },
 { name="Fusion", ref="066d4a6", owner="xioTechnologies", path="fusion/fusion", version="1.2.8",  license="MIT" },
 { name="glslang", ref="fc9889c", owner="KhronosGroup", path="glslang/glslang", version="15.3.0",  license="BSD-3-Clause" },
 { name="hidapi", ref="f424236", owner="RPCS3", path="hidapi/hidapi", version="0.15.0",  license="GPLv3, BSD" },
 { name="libpng", ref="ea12796", owner="pnggroup", path="libpng/libpng", version="1.6.48",  license="PNGRLLv2" },
 { name="SDL", ref="945eb6d", owner="libsdl-org", path="libsdl-org/SDL", version="3.2.14",  license="zlib" },
 { name="libusb", ref="a61afe5", owner="libusb", path="libusb/libusb", version="1.0.28",  license="LGPLv2.1" },
 { name="llvm-project", ref="cd70802", owner="llvm", path="llvm/llvm", version="19.1.7",  license="Apache-v2" },
 { name="miniupnp", ref="d66872e", owner="miniupnp", path="miniupnp/miniupnp", version="2.3.9",  license="BSD-3-Clause" },
 { name="opencv_minimal", ref="f76628f", owner="Megamouse", path="opencv/opencv", version="4.10.0" },
 { name="pugixml", ref="ee86beb", owner="zeux", path="pugixml", version="1.15",  license="MIT" },
 { name="rtmidi", ref="1e5b499", owner="thestk", path="rtmidi", version="6.0.0",  license="MIT" },
 { name="stb", ref="013ac3b", owner="nothings", path="stblib/stb", license="MIT" },
 { name="wolfssl", ref="b077c81", owner="wolfSSL", path="wolfssl/wolfssl", version="5.8.0",  license="GPLv3" },
 { name="yaml-cpp", ref="456c68f", owner="RPCS3", path="yaml-cpp/yaml-cpp", version="0.5.3",  license="MIT" },
 { name="zlib", ref="51b7f2a", owner="madler", path="zlib/zlib", version="1.3.1",  license="zlib" },
 { name="zstd", ref="f8745da", owner="facebook", path="zstd/zstd", version="1.5.7",  license="GPLv2" },
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
    print(string.format("mkdir -p 3rdparty/%s", (s.path or s.name)).."\n")
    print(string.format("tar -xzf %s --strip-components=1 -C 3rdparty/%s", rpm.expand("%{SOURCE"..si.."}"), (s.path or s.name)).."\n")
    ::continue2::
  end
end
}


# Core build tools
BuildRequires:  cmake
BuildRequires:  git
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  gcc
BuildRequires:  gcc-c++

# System FFmpeg (shared) replaces RPCS3’s “download prebuilt” logic
BuildRequires:  ffmpeg-free-devel

# Qt6 for the GUI
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qttools-devel

# X11 / Windowing
BuildRequires:  libX11-devel
BuildRequires:  libXrandr-devel
BuildRequires:  glew-devel

# Vulkan
BuildRequires:  vulkan-devel

# USB / HID / Controller support
BuildRequires:  libudev-devel
BuildRequires:  libusb1-devel

# Audio backends
#  - PulseAudio
BuildRequires:  pulseaudio-libs-devel
#  - OpenAL
BuildRequires:  openal-soft-devel

# Optional: Wayland client development (skip if you only need EGL/GL backend)
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  egl-wayland-devel
BuildRequires:  libwayland-egl

BuildRequires:  libcurl-devel
BuildRequires:  opencv-devel
BuildRequires:  libzstd-devel
BuildRequires:  git-all

BuildRequires:  rtmidi-devel


BuildRequires: alsa-lib-devel
BuildRequires: cmake
BuildRequires: ninja-build
BuildRequires: glew
BuildRequires: glew-devel
BuildRequires: libatomic
BuildRequires: libevdev-devel
BuildRequires: libudev-devel
BuildRequires: openal-soft-devel
# BuildRequires: openal-devel
BuildRequires: qt6-qtbase-devel
BuildRequires: qt6-qtbase-private-devel
BuildRequires: vulkan-devel
BuildRequires: pipewire-jack-audio-connection-kit-devel
# BuildRequires: jack-audio-connection-kit-devel
BuildRequires: qt6-qtmultimedia-devel
BuildRequires: qt6-qtsvg-devel
BuildRequires: llvm-devel
BuildRequires: SDL3-devel
BuildRequires: doxygen

%description
PlayStation 3 emulator and debugger

%prep
%autosetup

# Unpack bundled libraries
%{lua: print_setup_externals()}

# find 3rdparty/rtmidi -type f -name 'CMakeLists.txt' -exec sed -i '/add_custom_target(uninstall/d' {} +
# find 3rdparty/rtmidi -type f -name CMakeLists.txt -exec sed -i '/add_custom_target(uninstall/d' {} +
# find 3rdparty -type f -name CMakeLists.txt -exec sed -i '/add_custom_target(uninstall/d' {} +
sed -i "/^set(RTMIDI_TARGETNAME_UNINSTALL \"uninstall\" CACHE STRING \"Name of 'uninstall' build target\")\$/d" \
    3rdparty/rtmidi/CMakeLists.txt

# Silence old-style-cast warnings in just sse2neon.h
sed -i '1i#pragma GCC diagnostic push\n#pragma GCC diagnostic ignored "-Wold-style-cast"' \
      rpcs3/Emu/CPU/sse2neon.h
echo '#pragma GCC diagnostic pop' \
      >> rpcs3/Emu/CPU/sse2neon.h


%build
export CXXFLAGS="$CXXFLAGS -Wno-error=old-style-cast -Wno-old-style-cast"

%if %{with clang}
export CC=clang
export CXX=clang++
export LINKER=ld.lld
%else
export CC=gcc
export CXX=g++
export LINKER=gold
%endif
export LINKER_FLAG="-fuse-ld=${LINKER}"

cmake -B build \
      -Wno-dev \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_CXX_FLAGS="$CXXFLAGS" \
      -DLLVM_TARGETS_TO_BUILD=AArch64 \
      -DCMAKE_EXE_LINKER_FLAGS="${LINKER_FLAG}" \
      -DCMAKE_MODULE_LINKER_FLAGS="${LINKER_FLAG}" \
      -DCMAKE_SHARED_LINKER_FLAGS="${LINKER_FLAG}" \
      -DUSE_PRECOMPILED_HEADERS=OFF \
      -DBUILD_RPCS3_TESTS=OFF \
      -DRUN_RPCS3_TESTS=OFF \
      -DUSE_SDL=ON \
      -DUSE_SYSTEM_SDL=ON \
      -DUSE_SYSTEM_FFMPEG=ON \
      -DUSE_NATIVE_INSTRUCTIONS=OFF \
      -DUSE_SYSTEM_CURL=ON \
      -DUSE_SYSTEM_ZSTD=ON \
      -DUSE_SYSTEM_RTMIDI=ON \
      -DUSE_DISCORD_RPC=ON \
      -DUSE_SYSTEM_OPENCV=ON \
      -DCURL_USE_SYSTEM=ON \
      -DDISABLE_LTO=TRUE \
      -DUSE_SYSTEM_OPENCV=ON \
      -DOpenGL_GL_PREFERENCE=LEGACY \
      -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DCMAKE_INSTALL_LIBDIR=%{_lib} \
      -DCMAKE_EXE_LINKER_FLAGS="-L/usr/lib64/pipewire-0.3/jack" \
      -DSTATIC_LINK_LLVM=ON \
      -G Ninja
cd build
ninja


%install
cd build
DESTDIR=%{buildroot} ninja install


%files
%license LICENSE
%doc    README.md
%define debug_package %{nil}

%{_bindir}/rpcs3
%{_datadir}/applications/rpcs3.desktop
%{_datadir}/metainfo/rpcs3.metainfo.xml
%{_datadir}/icons/hicolor/48x48/apps/rpcs3.png
%{_datadir}/icons/hicolor/scalable/apps/rpcs3.svg
%{_datadir}/rpcs3


%changelog
* Mon Aug 11 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.37-2
- Updated how sources are organised and extracted.

* Sun Jun 08 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.37-1
- Initial RPM packaging of rpcs3
