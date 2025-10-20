Name: bluebubbles
Version: 1.15.4
Release: %autorelease
Summary: Messaging client for iMessage

License: Apache v2
URL: https://github.com/BlueBubblesApp/bluebubbles-app
Source0: https://github.com/BlueBubblesApp/bluebubbles-app/releases/download/v1.15.4%2B73-desktop/bluebubbles-linux-aarch64.tar

Requires: #######

%description
A cross-platform app ecosystem, bringing iMessage to Android, PC (Windows, Linux, & even macOS), and Web!

%prep
%setup -qn bluebubbles-linux-aarch64

%build
tar -xf %{SOURCE0}

%install
#############


%files
%license LICENSE
%doc README.md
%define debug_package %{nil}

%{_bindir}/bluebubbles
%{_libdir}/bluebubbles/*
%{_datadir}/data/*


%changelog
* Thu May 29 2025 Lachlan Marie <lchlnm@pm.me> - #######
- Initial RPM packaging of ########
