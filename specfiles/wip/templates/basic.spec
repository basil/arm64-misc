Name:       #[NAME]
Version:    #[VERSION]
Release:    1%{?dist}
Summary:    ##########################################

License:    #####
URL:        https://github.com/##########/%{name}
Source0:    https://github.com/#######/%{name}/#######/####/#####/%{name}-%{version}.tar.gz

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
- Initial RPM packaging of #[NAME]
