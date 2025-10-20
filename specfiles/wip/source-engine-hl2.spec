Name:       source-engine-hl2
Version:    git
Release:    1%{?dist}
Summary:    2017 Source Engine compiled for Half Life 2

License:    MIT License
URL:        https://github.com/nillerusr/source-engine
Source0:    https://github.com/nillerusr/source-engine/archive/2998568.tar.gz

# Bundled dependencies managed as git submodules upstream
# These are too entangled with the build system to unbundle for now
%{lua:
local externals = {
  { name="source-physics", ref="4753347", owner="nillerusr", path="ivp", version="git",  license="SOURCE 1 SDK" },
  { name="source-engine-libs", ref="86a66ee", owner="nillerusr", path="lib", version="git", license="SOURCE 1 SDK" },
  { name="source-thirdparty", ref="c5b901e", owner="nillerusr", path="thirdparty", version="git",  license="SOURCE 1 SDK" },
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
    print(string.format("mkdir -p %s", (s.path or s.name)).."\n")
    print(string.format("tar -xzf %s --strip-components=1 -C %s", rpm.expand("%{SOURCE"..si.."}"), (s.path or s.name)).."\n")
    ::continue2::
  end
end
}

BuildRequires:  git
BuildRequires:  python
BuildRequires:  gcc
BuildRequires:  SDL2_gfx-devel
BuildRequires:  ghc-gi-freetype2-devel
BuildRequires:  fontconfig-devel
BuildRequires:  zlib-ng-devel
BuildRequires:  bzip2-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libcurl-devel
BuildRequires:  opus-devel
BuildRequires:  openal-soft-devel

%description
2017 Source Engine compiled for Half Life 2

%prep
%autosetup -n source-engine-29985681a18508e78dc79ad863952f830be237b6


# Unpack bundled libraries
%{lua: print_setup_externals()}


%build
./waf configure -T release \
  --prefix=%{_prefix}         \
  --datadir=%{_datadir}       \
  --build-games=hl1           \
  --disable-warns
./waf build -p -v


%install
./waf install --destdir=%{buildroot}

%files
%license LICENSE
%doc README.md

%changelog
* Fri Jul 25 2025 Lachlan Marie <lchlnm@pm.me> - git-1
- Initial RPM packaging of Source Engine
