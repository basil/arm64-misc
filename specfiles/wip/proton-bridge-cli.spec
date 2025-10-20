Name: proton-bridge-cli
Version: 3.21.1
Release: 1%{?dist}
Summary: Proton Mail Bridge application

License: GNU GPL V3
URL: https://github.com/ProtonMail/proton-bridge
Source0: https://github.com/ProtonMail/proton-bridge/archive/refs/tags/v%{version}.tar.gz
Source1: proton-bridge-cli.3.21.1.tar.gz

%global goipath    github.com/ProtonMail/proton-bridge/v3
%global forgeurl   https://github.com/ProtonMail/proton-bridge
%global tag        v%{version}

%gometa -L -f      # generates Go metadata tables

BuildRequires: gcc
BuildRequires: pkgconfig
BuildRequires: cmake
BuildRequires: ninja-build
BuildRequires: libglvnd-devel
BuildRequires: golang
BuildRequires: git
BuildRequires: libsecret-devel
BuildRequires: go-rpm-macros

%description
Proton Mail Bridge is a program that runs in the background, encrypting and decrypting messages as they enter and leave your computer. It lets you add your Proton Mail account to your favorite email client via IMAP/SMTP by creating a local email server on your computer.

%prep
%autosetup -n proton-bridge-%{version} -N -a 1
%goprep github.com/ProtonMail/proton-bridge/v3 %{version}

%build
export GOFLAGS='-mod=vendor -buildvcs=false'
export GOPROXY=off GOSUMDB=off
%gobuild -o %{name} %{goipath}/cmd/Desktop-Bridge
# make build-nogui

%install
install -Dm0755 bridge %{buildroot}%{_bindir}/proton-bridge-cli


%files
%license LICENSE
%doc README.md
%define debug_package %{nil}

%{_bindir}/proton-bridge-cli



%changelog
* Thu Jun 26 2025 Lachlan Marie <lchlnm@pm.me> - 3.21.1-1
- Bumped version to 3.21.1.

* Thu May 29 2025 Lachlan Marie <lchlnm@pm.me> - 3.20.0-1
- Initial RPM packaging of proton-bridge-cli
