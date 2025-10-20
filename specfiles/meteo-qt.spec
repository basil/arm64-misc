%define aname meteo_qt

Name:           meteo-qt
Version:        4.2
Release:        %autorelease
Group:          Graphical desktop/Other
Summary:        Weather status system tray application
License:        GPLv3
URL:            https://github.com/dglent/meteo-qt
Source0:        https://github.com/dglent/meteo-qt/archive/refs/tags/v%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-qt5-devel
BuildRequires:  qt5-qttools
BuildRequires:  python3-pyqt6-base
BuildRequires:  qt6-qttools
BuildRequires:  qt5-linguist
BuildRequires:  qt6-linguist


%generate_buildrequires
%pyproject_buildrequires

%description
System tray application for weather status information. Uses the QT toolkit.


%prep
%autosetup
sed -i 's/lrelease-pro-qt6/lrelease-qt6/' setup.py


%build
/usr/lib64/qt6/bin/lrelease meteo_qt/translations/*.ts
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files meteo_qt   # produces %%{pyproject_files}

install -Dm0644 \
  %{buildroot}%{python3_sitelib}/usr/share/applications/meteo-qt.desktop \
  %{buildroot}%{_datadir}/applications/meteo-qt.desktop

install -Dm0644 \
  %{buildroot}%{python3_sitelib}/usr/share/icons/weather-few-clouds.png \
  %{buildroot}%{_datadir}/icons/weather-few-clouds.png

mkdir -p %{buildroot}%{_datadir}/meteo_qt/translations
mv %{buildroot}%{python3_sitelib}/usr/share/meteo_qt/translations/*.qm \
   %{buildroot}%{_datadir}/meteo_qt/translations/

rm -rf %{buildroot}%{python3_sitelib}/usr


%files -f %{pyproject_files}
%license LICENSE
%doc README.md

%{_bindir}/meteo-qt
%{_datadir}/applications/meteo-qt.desktop
%{_datadir}/icons/weather-few-clouds.png

%dir %{_datadir}/meteo_qt
%dir %{_datadir}/meteo_qt/translations
%{_datadir}/meteo_qt/translations/*.qm


%changelog
* Thu Jul 31 2025 Lachlan Marie <lchlnm@pm.me> - 4.2-1
- Initial packaging of meteo-qt.
