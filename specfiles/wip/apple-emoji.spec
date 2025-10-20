%global fontname apple-emoji
%global fontconf 65-%{fontname}.conf

Name:           %{fontname}-fonts
Version:        18.4
Release:        1%{?dist}
Summary:        A symbol font

# https://web.archive.org/web/20150625020428/http://users.teilar.gr/~g1951d/
# "in lieu of a licence:
# Fonts and documents in this site are not pieces of property or merchandise
# items; they carry no trademark, copyright, license or other market tags;
# they are free for any use. George Douros"
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
Symbola was created with Mathematics and other technical documents in mind. It
covers many scripts and symbols supported by Unicode.

These include those in Basic Latin, Latin-1 Supplement, Latin Extended-A, IPA
Extensions, Spacing Modifier Letters, Greek and Coptic, Cyrillic, Cyrillic
Supplementary, General Punctuation, Superscripts and Subscripts, and many
others.

It was created by George Douros.

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

%changelog
* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 10.24-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild
