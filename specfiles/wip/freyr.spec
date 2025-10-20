Name:     freyr
Version:  0.10.3
Release:  1%{?dist}
Summary:  A tool for downloading songs from music streaming services like Spotify and Apple Music.

License: Apache 2.0
URL:  https://github.com/miraclx/freyr-js
Source0: https://github.com/miraclx/freyr-js/archive/refs/tags/v0.10.3.tar.gz
Source1:  %{name}-%{version}-nm-prod.tgz
Source2:  %{name}-%{version}-nm-dev.tgz
Source3:  %{name}-%{version}-bundled-licenses.txt

# BuildRequires:
# BuildRequires:
# BuildRequires:
# BuildRequires:
# BuildRequires:
# BuildRequires:
# BuildRequires:
# BuildRequires:

%description
A tool for downloading songs from music streaming services like Spotify and Apple Music.

%prep
%autosetup -q -n package        # upstream tarball (npm puts everything in ./package)
cp %{SOURCE3}

%build

%install




%files
%license LICENSE  %{npm_name}-%{version}-bundled-licenses.txt
%{nodejs_sitelib}/%{npm_name}
%doc README.md
%define debug_package %{nil}


%changelog
* Sat Jul 26 2025 Lachlan Marie <lchlnm@pm.me> - 0.10.3-1
- Initial RPM packaging of freyr.
