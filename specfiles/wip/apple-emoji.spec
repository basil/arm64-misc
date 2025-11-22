%global fontname apple-emoji
%global fontconf 65-%{fontname}.conf

Name:           %{fontname}-fonts
Version:        18.4
Release:        1%{?dist}
Summary:        Apple Color Emoji font

License:        LicenseRef-Apple-Emoji
URL:            https://github.com/samuelngs/apple-emoji-linux
Source0:        https://github.com/samuelngs/apple-emoji-linux/archive/refs/tags/v%{version}.tar.gz
Source1:        %{name}-fontconfig.conf
Source2:        %{fontname}.metainfo.xml

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  python3-pillow
BuildRequires:  fontpackages-devel
BuildRequires:  optipng
BuildRequires:  zopfli
BuildRequires:  pngquant
BuildRequires:  ImageMagick
BuildRequires:  nototools
BuildRequires:  fonttools

%description
Apple-style color emoji font compiled from PNG assets using the
apple-emoji-linux build system. This package ships only the resulting
AppleColorEmoji.ttf, suitable for desktop use.

%prep
%autosetup -n apple-emoji-linux-%{version}

%build
%make_build

%install
rm -rf %{buildroot}

# Install the font
install -m 0755 -d %{buildroot}%{_fontdir}/%{fontname}
install -m 0644 -p AppleColorEmoji.ttf \
    %{buildroot}%{_fontdir}/%{fontname}/AppleColorEmoji.ttf

# fontconfig snippet (Source1)
install -m 0755 -d %{buildroot}%{_datadir}/fontconfig/conf.avail
install -m 0755 -d %{buildroot}%{_datadir}/fontconfig/conf.d
install -m 0644 -p %{SOURCE1} \
    %{buildroot}%{_datadir}/fontconfig/conf.avail/%{fontconf}
ln -s ../conf.avail/%{fontconf} \
    %{buildroot}%{_datadir}/fontconfig/conf.d/%{fontconf}

# AppStream metainfo (Source2)
install -m 0755 -d %{buildroot}%{_metainfodir}
install -m 0644 -p %{SOURCE2} \
    %{buildroot}%{_metainfodir}/%{fontname}.metainfo.xml

%check
appstream-util validate-relax --nonet \
      %{buildroot}/%{_metainfodir}/%{fontname}.metainfo.xml

%files
%doc README.md
%{_metainfodir}/%{fontname}.metainfo.xml
%{_datadir}/fontconfig/conf.avail/%{fontconf}
%{_datadir}/fontconfig/conf.d/%{fontconf}
%{_fontdir}/%{fontname}/AppleColorEmoji.ttf

%changelog
* Sat Nov 22 2025 Lachlan Marie <lchlnm@pm.me> - 18.4-1
- Initial packaging for apple-emoji-fonts
