%global bumpver 0
%global tag 1.3.0
%global _name umu-launcher

%global commit 4ed61d1031ea43d55100ae2ffa3057280ed2540c
%{?commit:%global shortcommit %(c=%{commit}; echo ${c:0:7})}

Name:        umu-launcher-git
Conflicts:   umu-launcher
Provides:    umu-launcher
Version:     %{?bumpver:%{bumpver}.git.%{shortcommit}}
Release:     1%{?dist}
Summary:     A tool for launching non-steam games with proton

# F41 doesn't ship urllib3 >= 2.0 needed
%global urllib3 2.3.0

License:        GPLv3
URL:            https://github.com/Open-Wine-Components/%{_name}
Source0:        %{url}/archive/%{shortcommit}/%{_name}-%{shortcommit}.tar.gz
Source1:        https://github.com/urllib3/urllib3/releases/download/%{urllib3}/urllib3-%{urllib3}.tar.gz
Source2:        umu-launcher-vendor-4ed61d1.tar.zst

BuildArch:      x86_64 aarch64
BuildRequires:  meson >= 0.54.0
BuildRequires:  ninja-build
BuildRequires:  cmake
BuildRequires:  g++
BuildRequires:  gcc-c++
BuildRequires:  scdoc
BuildRequires:  git
BuildRequires:  sed
BuildRequires:  python3-devel
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-hatchling
BuildRequires:  python
BuildRequires:  python3
BuildRequires:  python3-pip
BuildRequires:  libzstd-devel
BuildRequires:  python3-hatch-vcs
BuildRequires:  python3-wheel
BuildRequires:  python3-xlib
BuildRequires:  python3-pyzstd
BuildRequires:  python3-vdf
BuildRequires:  python3-hatch-vcs
BuildRequires:  cargo

# Can't use these yet, F41 doesn't ship urllib3 >= 2.0 needed
#BuildRequires:  python3-urllib3

Requires:	python
Requires:	python3
Requires:	python3-xlib
Requires:	python3-filelock
Requires:	python3-pyzstd

# Can't use these yet, F41 doesn't ship urllib3 >= 2.0 needed
#Requires:  python3-urllib3

Recommends:	python3-cbor2
Recommends:	python3-xxhash
Recommends:	libzstd

# We need this for now to allow umu's builtin urllib3 version to be used.
# Can be removed when python3-urllib3 version is bumped >= 2.0
AutoReqProv: no


%description
%{name} A tool for launching non-steam games with proton

%prep
%autosetup -n %{_name}-%{commit} -p 1 -a 2
if ! find subprojects/urllib3/ -mindepth 1 -maxdepth 1 | read; then
    # Directory is empty, perform action
    mv %{SOURCE1} .
    tar -xf urllib3-%{urllib3}.tar.gz
    rm *.tar.gz
    mv urllib3-%{urllib3}/* subprojects/urllib3/
fi
sed -i 's/cargo build -r --target-dir/cargo build --offline -r --target-dir/g' Makefile.in
mkdir -p .cargo
cat >> .cargo/config.toml << 'EOF'

[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF



%build
# Update this when fedora ships urllib3 >= 2.0
#./configure.sh --prefix=/usr --use-system-pyzstd --use-system-urllib
./configure.sh --prefix=/usr --use-system-pyzstd --use-system-vdf --use-system-urllib
make

%install
make DESTDIR=%{buildroot} PYTHONDIR=%{python3_sitelib} install

%files
%{_bindir}/umu-run
%{_datadir}/man/*
%{python3_sitelib}/umu*

%changelog
* Sun Dec 07 2025 Lachlan Marie <lchlnm@pm.me> - 1.3.0^0.git.4ed61d1-1
 - Adapted specfile from gmanka copr
 - Changed build from project git commits
 - Update to commit 4ed61d1031ea43d55100ae2ffa3057280ed2540c
