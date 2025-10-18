Name: monero-gui
Version: 0.18.4.2
Release: 1%{?dist}
Summary: Monero: the secure, private, untraceable cryptocurrency

License: Monero Project
URL: https://github.com/monero-project/monero-gui
Source0: https://github.com/monero-project/monero-gui/archive/refs/tags/v%{version}.tar.gz

%{lua:
local externals = {
  { name="monero",        ref="d87edf5", owner="monero-project", path="", version="0.18.4.2", license="BSD-3-Clause" },
  { name="quirc",         ref="7e7ab59", owner="dlbeer", path="../external/quirc", license="ISC License" },
  { name="miniupnp",      ref="544e6fc", owner="miniupnp", path="external/miniupnp", version="2.2.1", license="BSD-3-Clause" },
  { name="RandomX",       ref="102f8ac", owner="tevador", path="external/randomx", version="1.2.1", license="BSD-3-Clause" },
  { name="rapidjson",     ref="129d19b", owner="Tencent", path="external/rapidjson", version="1.1.0", license="MIT" },
  { name="supercop",      ref="633500a", owner="monero-project", path="external/supercop" },
  { name="trezor-common", ref="bff7fdf", owner="trezor", path="external/trezor-common", license="LGPLv3" },
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
    print(string.format("mkdir -p monero/%s", (s.path or s.name)).."\n")
    print(string.format("tar -xzf %s --strip-components=1 -C monero/%s", rpm.expand("%{SOURCE"..si.."}"), (s.path or s.name)).."\n")
    ::continue2::
  end
end
}

BuildRequires:  make
BuildRequires:  automake
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  boost-devel
BuildRequires:  miniupnpc-devel
BuildRequires:  graphviz
BuildRequires:  doxygen
BuildRequires:  unbound-devel
BuildRequires:  libunwind-devel
BuildRequires:  pkgconfig
BuildRequires:  openssl-devel
BuildRequires:  libcurl-devel
BuildRequires:  hidapi-devel
BuildRequires:  zeromq-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  git
BuildRequires:  libX11-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  libXv-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  ccache
BuildRequires:  readline-devel
BuildRequires:  protobuf-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-linguist

Requires:   systemd
Requires:   qt5-qtquickcontrols
Requires:   qt5-qtquickcontrols2
Requires:   qt5-qtxmlpatterns

%description
Monero is a private, secure, untraceable, decentralised digital currency. You are your bank, you control your funds, and nobody can trace your transfers unless you allow them to do so.

%prep
%autosetup

# Unpack bundled libraries
%{lua: print_setup_externals()}


%build
mkdir -p build
cd build
cmake \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
  -D CMAKE_BUILD_TYPE=Release \
  -D CMAKE_INSTALL_PREFIX=%{_prefix} \
  -DUSE_CCACHE=ON \
  -Wno-dev \
  -D CMAKE_POLICY_DEFAULT_CMP0077=NEW \
  -D CMAKE_POLICY_DEFAULT_CMP0148=OLD \
  -D CMAKE_POLICY_DEFAULT_CMP0167=NEW \
  ..
make %{?_smp_mflags}


%install
cd build
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}
mkdir -p %{buildroot}%{_datadir}/applications

cd ..
mv %{buildroot}/usr/lib %{buildroot}/usr/lib64
install -Dm0644 share/org.getmonero.Monero.desktop \
        %{buildroot}%{_datadir}/applications/


%files
%license LICENSE*
%doc    README*

%{_bindir}/monero*
%{_datadir}/applications/*

%{_includedir}/wallet/api/*.h
%{_libdir}/libepee.a
%{_libdir}/libepee_readline.a
%{_libdir}/libeasylogging.a
%{_libdir}/liblmdb.a


%changelog
* Mon Aug 11 2025 Lachlan Marie <lchlnm@pm.me> - 0.18.4.1-1
- Increased version to 0.18.4.1, updated source gathering process.

* Mon Jun 23 2025 Lachlan Marie <lchlnm@pm.me> - 0.18.4.0-1
- Initial RPM packaging of monero-gui
