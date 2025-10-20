Name:           helvetica-neue
Version:        5.0.0
Release:        1%{?dist}
Summary:        Helvetica Neue font family version %{version}
License:        Proprietary
URL:            https://font.download/dl/font/helvetica-neue-5.zip
Source0:        https://font.download/dl/font/helvetica-neue-5.zip
BuildArch:      noarch
BuildRequires:  fontconfig
Requires(post):    fontconfig
Requires(postun):  fontconfig

%description
Helvetica Neue is a sans-serif typeface. This package installs the full 5.x
family including Roman, Italic, Thin, Thin Italic, UltraLight,
UltraLight Italic, Light, Light Italic, Medium, Medium Italic,
Bold, Bold Italic, Heavy, Heavy Italic, Black, Black Italic.

%prep
# Prepare empty source directory
%setup -q -c -T
# Extract all font files without directory structure
unzip -q -j %{SOURCE0} "*.otf" "*.ttf"

%build
# No build steps required

%install
# Create fonts directory in buildroot
install -d %{buildroot}%{_datadir}/fonts/helvetica-neue
# Install font files
install -m 0644 *.otf *.ttf %{buildroot}%{_datadir}/fonts/helvetica-neue/

%post
# Rebuild font cache
fc-cache -f -v >/dev/null 2>&1

%postun
# Rebuild font cache on uninstall
fc-cache -f -v >/dev/null 2>&1

%files
# Font files
%{_datadir}/fonts/helvetica-neue/*.otf
%{_datadir}/fonts/helvetica-neue/*.ttf

%changelog
* Sun Jun 15 2025 Lachlan Marie <lchlnm@pm.me> - 5.0.0-1
- Added %post/%postun to rebuild font cache
- Added Requires(post)/(postun) for fontconfig
- Cleaned up spec following packaging best practices
