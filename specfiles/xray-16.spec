%global bumpver 9

%global commit 831186f99d22798fdb42c4c058b6e7e6f42a140b
%{?commit:%global shortcommit %(c=%{commit}; echo ${c:0:7})}

Name:       xray-16
Version:    git%{?bumpver:^%{bumpver}.git.%{shortcommit}}
Release:    3%{?dist}
Summary:    Open Source XRay engine for S.T.A.L.K.E.R.

License:    MIT License
URL:        https://github.com/OpenXRay/xray-16
Source0:    https://github.com/OpenXRay/xray-16/archive/%{shortcommit}/xray-16-%{shortcommit}.tar.gz

%{lua:
local externals = {
  { name="AGS_SDK", ref="5d8812d", owner="GPUOpen-LibrariesAndSDKs", path="AGS_SDK", version="6.3.0",  license="AMD" },
  { name="GameSpy", ref="3e43480", owner="OpenXRay", path="GameSpy",  license="IGN" },
  { name="LuaJIT", ref="5a5cd82", owner="OpenXRay", path="LuaJIT", version="2.1",  license="MIT" },
  { name="gli", ref="779b99a", owner="g-truc", path="gli", version="0.8.2.0",  license="MIT" },
  { name="imgui", ref="4fa59df", owner="ocornut", path="imgui", version="v.1.94.5",  license="MIT" },
  { name="luabind-deboostified", ref="8da131b", owner="OpenXRay", path="luabind", version="0.9",  license="MIT" },
  { name="sse2neon", ref="42eee28", owner="DLTcollab", path="sse2neon", version="1.8.0",  license="MIT" },
  { name="sse2rvv", ref="373f788", owner="pattonkan", path="sse2rvv", version="git",  license="MIT" },
  { name="xrLuaFix", ref="0e89050", owner="OpenXRay", path="xrLuaFix", version="git",  license="BSD-3" },
  { name="jenkins-ctest-plugin", ref="63a4a82", owner="rpavlik", path="luabind/test/jenkins-ctest-plugin", version="git",  license="MIT" },
  { name="luafilesystem", ref="314c0d0", owner="OpenXRay", path="xrLuaFix/lfs", version="git",  license="MIT" },
  { name="lua-marshal", ref="983a3bf", owner="OpenXRay", path="xrLuaFix/lua-marshal", version="git",  license="MIT" },
  { name="lua-pack", ref="c1e5a14", owner="OpenXRay", path="xrLuaFix/lua-pack", version="2.0.0",  license="MIT" },
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
    print(string.format("mkdir -p Externals/%s", (s.path or s.name)).."\n")
    print(string.format("tar -xzf %s --strip-components=1 -C Externals/%s", rpm.expand("%{SOURCE"..si.."}"), (s.path or s.name)).."\n")
    ::continue2::
  end
end
}

BuildRequires:  git
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  openal-soft-devel
BuildRequires:  cryptopp-devel
BuildRequires:  openal-soft-devel
BuildRequires:  SDL2-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  mimalloc-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libtheora-devel
BuildRequires:  libogg-devel
BuildRequires:  lzo-devel


%description
Improved version of the X-Ray Engine, the game engine used in the world-famous S.T.A.L.K.E.R. game series by GSC Game World. Join OpenXRay!

%prep
%autosetup -n xray-16-%{commit}

%{lua: print_setup_externals()}


%build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo
%cmake_build


%install
%cmake_install


%files

%license License.txt
%doc README.md

%{_bindir}/xr_3da

%{_datadir}/applications/openxray_*.desktop
%{_datadir}/pixmaps/openxray_*.png
%{_datadir}/icons/hicolor/*/apps/openxray_*.png

%{_datadir}/bash-completion/completions/xr_3da

%{_libdir}/xr*.so

%dir %{_datadir}/openxray
%{_datadir}/openxray/*

%changelog
* Fri Nov 21 2025 Lachlan Marie <lchlnm@pm.me> - git^9.git.831186f-3
- Shortened commit length in xray source URL.

* Thu Nov 06 2025 Lachlan Marie <lchlnm@pm.me> - git^2.git.9f0475d-2
- Updated xray-16 git commit

* Wed Nov 05 2025 Lachlan Marie <lchlnm@pm.me> - git^1.git.0ed27d4-2
- Updated xray-16 git commit

* Wed Nov 05 2025 Lachlan Marie <lchlnm@pm.me> - git^0.git.55a888c-2
- Changed to spec to follow git commits

* Fri Jul 25 2025 Lachlan Marie <lchlnm@pm.me> - git-1
- Initial RPM packaging of OpenXRay
