%global bumpver 27

%global commit e3f5f2d14e44a44eec9f8c0f79f53893ff04fdbc
%{?commit:%global shortcommit %(c=%{commit}; echo ${c:0:7})}

Name:       rpcs3-git
Version:    0.0.38%{?bumpver:^%{bumpver}.git.%{shortcommit}}
Release:    1%{dist}
Summary:    PlayStation 3 emulator and debugger

Conflicts:      rpcs3
Provides:       rpcs3

License:  GPLv2
URL:      https://github.com/RPCS3/rpcs3
Source0:  https://github.com/RPCS3/rpcs3/archive/%{shortcommit}/rpcs3-%{shortcommit}.tar.gz

%{lua:
local externals = {
 { name="7zip", ref="5e96a82", owner="ip7z", path="7zip/7zip", version="25.01",  license="GNU-LGPL" },
 { name="FAudio", ref="4ea8afe", owner="FNA-XNA", path="FAudio", version="25.12",  license="zlib" },
 { name="VulkanMemoryAllocator", ref="1d8f600", owner="GPUOpen-LibrariesAndSDKs", path="GPUOpen/VulkanMemoryAllocator", version="3.3.0",  license="MIT" },
 { name="openal-soft", ref="0e5e98e", owner="kcat", path="OpenAL/openal-soft", version="1.24.3",  license="PFFFT" },
 { name="soundtouch", ref="3982730", owner="RPCS3", path="SoundTouch/soundtouch/", version="2.4.0",  license="LGPLv2.1" },
 { name="asmjit", ref="416f735", owner="asmjit", path="asmjit/asmjit/", license="zlib" },
 { name="cubeb", ref="e495bee", owner="mozilla", path="cubeb/cubeb", license="ISC" },
 { name="curl", ref="400fffa", owner="curl", path="curl/curl", version="8.17.0",  license="MIT" },
 { name="discord-rpc", ref="3dc2c32", owner="Vestrel", path="discord-rpc/discord-rpc", license="MIT" },
 { name="gamemode", ref="c54d6d4", owner="FeralInteractive", path="feralinteractive/feralinteractive", version="1.8.2", license="BSD-3-Clause" },
 { name="ffmpeg-core", ref="ec6367d", owner="RPCS3", path="ffmpeg", license="LGPLv2.1" },
 { name="flatbuffers", ref="595bf00", owner="google", path="flatbuffers", version="24.3.25",  license="Apache-v2" },
 { name="Fusion", ref="759ac5d", owner="xioTechnologies", path="fusion/fusion", version="1.2.9",  license="MIT" },
 { name="glslang", ref="fc9889c", owner="KhronosGroup", path="glslang/glslang", version="15.3.0",  license="BSD-3-Clause" },
 { name="hidapi", ref="f424236", owner="RPCS3", path="hidapi/hidapi", version="0.15.0",  license="GPLv3, BSD" },
 { name="libpng", ref="49363ad", owner="pnggroup", path="libpng/libpng", version="1.6.51",  license="PNGRLLv2" },
 { name="SDL", ref="7f3ae3d", owner="libsdl-org", path="libsdl-org/SDL", version="3.2.28",  license="zlib" },
 { name="libusb", ref="15a7ebb", owner="libusb", path="libusb/libusb", version="1.0.29",  license="LGPLv2.1" },
 { name="llvm-project", ref="cd70802", owner="llvm", path="llvm/llvm", version="19.1.7",  license="Apache-v2" },
 { name="miniupnp", ref="d66872e", owner="miniupnp", path="miniupnp/miniupnp", version="2.3.9",  license="BSD-3-Clause" },
 { name="opencv_minimal", ref="67f53c2", owner="Megamouse", path="opencv/opencv", version="4.12.0" },
 { name="pugixml", ref="ee86beb", owner="zeux", path="pugixml", version="1.15",  license="MIT" },
 { name="rtmidi", ref="1e5b499", owner="thestk", path="rtmidi", version="6.0.0",  license="MIT" },
 { name="stb", ref="013ac3b", owner="nothings", path="stblib/stb", license="MIT" },
 { name="wolfssl", ref="b077c81", owner="wolfSSL", path="wolfssl/wolfssl", version="5.8.2",  license="GPLv3" },
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


BuildRequires:  cmake
BuildRequires:  git
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ffmpeg-free-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qttools-devel
BuildRequires:  libX11-devel
BuildRequires:  libXrandr-devel
BuildRequires:  glew-devel
BuildRequires:  vulkan-devel
BuildRequires:  libudev-devel
BuildRequires:  libusb1-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  openal-soft-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  egl-wayland-devel
BuildRequires:  libwayland-egl
BuildRequires:  libcurl-devel
BuildRequires:  opencv-devel
BuildRequires:  libzstd-devel
BuildRequires:  git-all
BuildRequires:  rtmidi-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  glew
BuildRequires:  glew-devel
BuildRequires:  libatomic
BuildRequires:  libevdev-devel
BuildRequires:  libudev-devel
BuildRequires:  openal-soft-devel
# BuildRequires:  openal-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  vulkan-devel
BuildRequires:  pipewire-jack-audio-connection-kit-devel
# BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  qt6-qtmultimedia-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  llvm-devel
BuildRequires:  SDL3-devel
BuildRequires:  doxygen

%description
PlayStation 3 emulator and debugger

%prep
%autosetup -n rpcs3-%{commit}

%{lua: print_setup_externals()}

sed -i "/^set(RTMIDI_TARGETNAME_UNINSTALL \"uninstall\" CACHE STRING \"Name of 'uninstall' build target\")\$/d" \
    3rdparty/rtmidi/CMakeLists.txt

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
* Thu Dec 04 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^27.git.e3f5f2d-1
 - Update to commit e3f5f2d14e44a44eec9f8c0f79f53893ff04fdbc

* Wed Dec 03 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^26.git.b86b4d1-1
 - Update to commit b86b4d15c638644e3ef42ea6fe915733adb7a1bc

* Wed Dec 03 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^25.git.613d428-1
 - Update to commit 613d428ced78c345fd5c0077b0e72d484bce10d5

* Tue Dec 02 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^24.git.3c747b3-1
 - Update to commit 3c747b377f8e7112cfe85ed3b2a8147a9946ca39

* Tue Dec 02 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^23.git.6dd37cb-1
 - Update to commit 6dd37cb2d5db99c7188246df05678b532fff041a

* Tue Dec 02 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^22.git.7e8ed5e-1
 - Update to commit 7e8ed5ecc102609fa0fc80d6a5ffe78d5c21e61e

* Mon Dec 01 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^21.git.25badf9-1
 - Update to commit 25badf9534440e7a723aa14a0f16ddd5aa24b793

* Mon Dec 01 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^20.git.4bda2f9-1
 - Update to commit 4bda2f9b0f81557386ff935c944a596e3c5c1ae1

* Sun Nov 30 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^19.git.c80aba2-1
 - Update to commit c80aba2342a95a84d44cc5559276bf4609924c72

* Sun Nov 30 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^18.git.e938b93-1
 - Update to commit e938b93f487532200d68d75d2bf15af6730e1a08

* Sat Nov 29 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^17.git.d625c1d-1
 - Update to commit d625c1d00416815880183c2edd9173a719c0e4c6

* Fri Nov 28 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^16.git.d9f9130-1
 - Update to commit d9f913016cbbdc32ce43ac02f4e0ef6a8ffd1ae4

* Thu Nov 27 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^15.git.a442cb9-1
 - Update to commit a442cb91a101bf19b1b0912db7fb071d62360369

* Tue Nov 25 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^14.git.5a9083e-1
 - Update to commit 5a9083e4fc0bfb73b09c4c436d8f5e78f8c2702a

* Mon Nov 24 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^13.git.6a398f9-1
 - Update to commit 6a398f994793d6d74d649ec7989d621627e547e1

* Mon Nov 24 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^12.git.89a13b7-1
 - Update to commit 89a13b75f70815f5018c1168b3f5b80ff49d0005

* Sun Nov 23 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^11.git.fcff16b-1
 - Update to commit fcff16b6f711ae7263f883d8efc18a3a3d33e227

* Sun Nov 23 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^10.git.a3f7c0d-1
 - Update to commit a3f7c0d67f7b2aee900201952793fabd15d17903

* Sat Nov 22 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38^9.git.7f68427-1
 - Update to commit 7f6842705ce376587c6062d1471118b7b75ffa76

* Wed Nov 12 2025 Lachlan Marie <lchlnm@pm.me> - git
- Converted to build for git commits

* Mon Aug 11 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.38-1
- Updated to 0.0.38, increased versions of several sources

* Mon Aug 11 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.37-2
- Updated how sources are organised and extracted.

* Sun Jun 08 2025 Lachlan Marie <lchlnm@pm.me> - 0.0.37-1
- Initial RPM packaging of rpcs3
