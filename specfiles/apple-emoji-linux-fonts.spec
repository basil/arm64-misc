%global fontname apple-emoji-linux
%global fontconf 65-%{fontname}.conf
%global fontdir %{_datadir}/fonts/%{fontname}
%global fontconfig_avail %{_datadir}/fontconfig/conf.avail
%global fontconfig_confdir %{_sysconfdir}/fonts/conf.d

Name:           %{fontname}-fonts
Version:        18.4
Release:        1%{?dist}
Summary:        Apple Color Emoji font for Linux

License:        OFL-1.1 AND Apache-2.0
URL:            https://github.com/samuelngs/%{fontname}
Source0:        https://github.com/samuelngs/%{fontname}/archive/refs/tags/v%{version}.tar.gz
Source1:        %{name}-fontconfig.conf
Source2:        %{fontname}.metainfo.xml

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  fonttools
BuildRequires:  nototools
BuildRequires:  optipng
BuildRequires:  zopfli
BuildRequires:  pngquant
BuildRequires:  ImageMagick
BuildRequires:  libappstream-glib

%description
Apple Color Emoji for Linux is a color emoji font that recreates Apple's
emoji designs for use on Linux desktops and applications. It uses the CBDT/CBLC
color font format and covers the same Unicode emoji repertoire as recent iOS
releases.

%prep
%autosetup -n apple-emoji-linux-%{version}

%build
%make_build

%install
install -m 0755 -d %{buildroot}%{fontdir}
install -m 0644 -p AppleColorEmoji.ttf \
    %{buildroot}%{fontdir}/

install -m 0755 -d %{buildroot}%{fontconfig_avail} \
                   %{buildroot}%{fontconfig_confdir}
install -m 0644 -p %{SOURCE1} \
    %{buildroot}%{fontconfig_avail}/%{fontconf}
ln -s %{fontconfig_avail}/%{fontconf} \
    %{buildroot}%{fontconfig_confdir}/%{fontconf}

install -m 0755 -d %{buildroot}%{_metainfodir}
install -m 0644 -p %{SOURCE2} \
    %{buildroot}%{_metainfodir}/%{fontname}.metainfo.xml

%check
appstream-util validate-relax --nonet \
    %{buildroot}/%{_metainfodir}/%{fontname}.metainfo.xml

%post
if [ -x /usr/bin/fc-cache ]; then
    fc-cache -f %{_datadir}/fonts >/dev/null 2>&1 || :
fi

%postun
if [ $1 -eq 0 ] && [ -x /usr/bin/fc-cache ]; then
    fc-cache -f %{_datadir}/fonts >/dev/null 2>&1 || :
fi

%files
%license LICENSE
%doc README.md
%{fontdir}/AppleColorEmoji.ttf
%{fontconfig_avail}/%{fontconf}
%{fontconfig_confdir}/%{fontconf}
%{_metainfodir}/%{fontname}.metainfo.xml

%changelog
* Sat Nov 23 2025 Lachlan Marie <lchlnm@pm.me> - 18.4-1
- Initial packaging for apple-emoji-linux-fonts
