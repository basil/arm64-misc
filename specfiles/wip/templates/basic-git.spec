%global bumpver 0

%global commit fcff16b6f711ae7263f883d8efc18a3a3d33e227
%{?commit:%global shortcommit %(c=%{commit}; echo ${c:0:7})}

Name:        #[NAME]-git
Conflicts:   #[NAME]
Provides:    #[NAME]
Version:     #####%{?bumpver:^%{bumpver}.git.%{shortcommit}}
Release:     1%{?dist}
Summary:     ##########################################

License:     #####
URL:         https://github.com/##########/%{name}
Source0:     https://github.com/#######/%{name}/archive/%{shortcommit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  #######
BuildRequires:  #######
BuildRequires:  #######

Requires:       #######
Requires:       #######
Requires:       #######

%description
######################################################################

%prep
%autosetup -qn %{name}-%{version}

%build
#####################

%install
#############


%files
%license LICENSE
%doc README.md
%define debug_package %{nil}

%{_bindir}/#############
%{_bindir}/###############
%{_bindir}/############
%{_bindir}/#############


%changelog
* Sun Nov 23 2025 Lachlan Marie <lchlnm@pm.me> - #[VERSION]-1
- Initial RPM packaging of #[NAME]-git
