%global fontname apple-emoji
%global fontconf 65-%{fontname}.conf

Name:           %{fontname}-fonts
Version:        18.4
Release:        1%{?dist}
Summary:        A symbol font

License:        LicenseRef-Fedora-UltraPermissive
URL:            https://github.com/samuelngs/apple-emoji-linux
Source0:        https://github.com/samuelngs/apple-emoji-linux/archive/refs/tags/v%{version}.tar.gz
Source1:        %{name}-fontconfig.conf
Source2:        %{fontname}.metainfo.xml

BuildArch:      noarch
BuildRequires:  fontpackages-devel
BuildRequires:  libappstream-glib
Requires:       fontpackages-filesystem

%description

%prep
%setup -q -c

%build

%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p Symbola.ttf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}
ln -s %{_fontconfig_templatedir}/%{fontconf} \
      %{buildroot}%{_fontconfig_confdir}/%{fontconf}

install -Dm 0644 -p %{SOURCE2} \
        %{buildroot}%{_datadir}/metainfo/%{fontname}.metainfo.xml

%check
appstream-util validate-relax --nonet \
      %{buildroot}/%{_datadir}/metainfo/%{fontname}.metainfo.xml


%_font_pkg -f %{fontconf} Symbola.ttf
%{_datadir}/metainfo/%{fontname}.metainfo.xml
%doc Symbola.pdf Symbola.odt

%autochangelog
