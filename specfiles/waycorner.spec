Name:           waycorner
Version:        0.2.3
Release:        2%{?dist}
Summary:        Hot corners for Wayland. Create anchors in the corners of your monitors and execute a command of your choice.

License:        MIT
URL:            https://github.com/AndreasBackx/waycorner
Source0:        https://github.com/AndreasBackx/waycorner/archive/refs/tags/%{version}.tar.gz
Source1:        waycorner-vendor-0.2.3.tar.gz

BuildArch:      %{_target_cpu}
BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  pkgconfig
BuildRequires:  wayland-devel
BuildRequires:  rust-packaging

%description
Hot corners for Wayland. Create anchors in the corners of your monitors and execute a command of your choice.

%prep
%autosetup -n %{name}-%{version} -p1 -a1
%cargo_prep -v vendor
# tar -xvf %{SOURCE1}


%generate_buildrequires

%build
%cargo_vendor_manifest
%cargo_build

%install
%cargo_install
# install -Dm0755 target/release/waycorner %{buildroot}%{_bindir}/waycorner
# install -Dm644 LICENSE         %{buildroot}%{_licenses}/LICENSE
# install -Dm644 README.md       %{buildroot}%{_docdir}/%{name}/README.md
# install -Dm644 CHANGELOG.md    %{buildroot}%{_docdir}/%{name}/CHANGELOG.md

%files
%license LICENSE* cargo-vendor.txt
%doc README* CHANGELOG.md
%{_bindir}/waycorner
%define debug_package %{nil}

%changelog
* Sun Jul 06 2025 Lachlan Marie <lchlnm@pm.me> - 0.2.3-2
- Vendored rust cargo to allow offline building.

* Sat May 10 2025 Lachlan Marie <lchlnm@pm.me> - 0.2.3-1
- Initial RPM packaging of waycorner
