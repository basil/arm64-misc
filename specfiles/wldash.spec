%global bumpver 0

%global commit 1156b3503a04780bbdcb6a781cce87281b8bf87d
%{?commit:%global shortcommit %(c=%{commit}; echo ${c:0:7})}

Name:           wldash
Version:        git%{?bumpver:^%{bumpver}.git.%{shortcommit}}
Release:        3%{?dist}
Summary:        Hot corners for Wayland. Create anchors in the corners of your monitors and execute a command of your choice.

License:        GNU GPL v3
URL:            https://git.sr.ht/~kennylevinsen/%{name}
Source0:        https://git.sr.ht/~kennylevinsen/%{name}/archive/%{shortcommit}.tar.gz
Source1:        %{name}-vendor-%{shortcommit}.tar.gz

BuildArch:      %{_target_cpu}
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  pkgconfig
BuildRequires:  wayland-devel
BuildRequires:  fontconfig-devel
BuildRequires:  dbus-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  rust-packaging
BuildRequires:  cargo

%description
Hot corners for Wayland. Create anchors in the corners of your monitors and execute a command of your choice.

%prep
%autosetup -n %{name}-%{shortcommit} -p1 -a1
%cargo_prep -v vendor

%generate_buildrequires

%build
%cargo_vendor_manifest
%cargo_build

%install
%cargo_install

%files
%license LICENSE cargo-vendor.txt
%doc README.md
%{_bindir}/wldash
%define debug_package %{nil}

%changelog
* Sun Jul 06 2025 Lachlan Marie <lchlnm@pm.me> - git^0.git.1156b35-3
- Adjusted spec to build based on git commit.
- Use short commit in source filenames

* Sun Jul 06 2025 Lachlan Marie <lchlnm@pm.me> - 1156b3503a04780bbdcb6a781cce87281b8bf87d-2
- Vendored rust cargo to allow offline building.

* Wed Jun 04 2025 Lachlan Marie <lchlnm@pm.me> - 1156b3503a04780bbdcb6a781cce87281b8bf87d-1
- Initial RPM packaging of wldash
