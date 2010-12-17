
%define plugin	graphtft
%define name	vdr-plugin-%plugin
%define version	0.3.2
%define prever	rc2
%define rel	5

Summary:	VDR plugin: VDR OSD on TFT
Name:		%name
Version:	%version
%if %prever
Release:	%mkrel 0.%prever.%rel
%else
Release:	%mkrel %rel
%endif
Group:		Video
License:	GPL+
URL:		http://www.jwendel.de/vdr/
%if %prever
Source:		http://www.jwendel.de/vdr/vdr-graphtft-%version-%prever.tar.bz2
%else
Source:		http://www.jwendel.de/vdr/vdr-graphtft-%version.tar.bz2
%endif
Patch1:		graphtft-includes.patch
Patch2:		graphtft-const-char-gcc4.4.patch
# ffmpeg fixes (from e-tobi)
Patch0:		graphtft-ffmpeg.patch
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	vdr-devel >= 1.6.0
BuildRequires:	ffmpeg-devel
BuildRequires:	imlib2-devel
BuildRequires:	imagemagick-devel
BuildRequires:	directfb-devel
BuildRequires:	libgtop2.0-devel
Requires:	vdr-abi = %vdr_abi
# not necessarily needed anymore, but still referenced in code:
Suggests:	fonts-ttf-bitstream-vera

%description
Display VDR status information on a smallish framebuffer or directfb
device. Touchscreens are also supported.

You also need at least one theme (not included in this package). Install
themes under %{_vdr_plugin_cfgdir}/graphTFT/themes/.

%prep
%if %prever
%setup -q -n %plugin-%version-%prever
%else
%setup -q -n %plugin-%version
%endif
%patch0 -p1
%patch1 -p1
%patch2 -p1
%vdr_plugin_prep

rm documents/*~
chmod 0644 documents/{README,HOWTO*}
for file in documents/{README,HOWTO*,CONTRIBUTORS} TODO; do
	iconv -f ISO-8859-15 -t UTF-8 -o $file.new $file
	mv -f $file.new $file
done

%vdr_plugin_params_begin %plugin
# graphTFT output device (default: autodetect)
var=DEVICE
param="-d DEVICE"
%vdr_plugin_params_end

cat > README.install.urpmi <<EOF
You also need at least one theme if you want to use the features of
graphtft plugin. Themes are not included in this package. Install themes
under %{_vdr_plugin_cfgdir}/graphTFT/themes/.

%build
export VDR_PLUGIN_EXTRA_FLAGS="-D__STDC_CONSTANT_MACROS"
%vdr_plugin_build
%make -C graphtft-fe LFLAGS="%{?ldflags}" CXX="g++ %{optflags}"

%install
rm -rf %{buildroot}
%vdr_plugin_install

install -d -m755 %{buildroot}%{_vdr_plugin_cfgdir}/graphTFT/{fonts,themes}
# referenced in code, possibly not needed anymore anyway:
ln -s %{_datadir}/fonts/TTF/Vera.ttf %{buildroot}%{_vdr_plugin_cfgdir}/graphTFT/fonts/Vera.ttf

install -d -m755 %{buildroot}%{_bindir}
install -m755 graphtft-fe/graphtft-fe %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}

%post
%vdr_plugin_post %plugin

%postun
%vdr_plugin_postun %plugin

%files -f %plugin.vdr
%defattr(-,root,root)
%doc TODO documents/README documents/CONTRIBUTORS documents/HISTORY documents/HOWTO* README*
%{_bindir}/graphtft-fe
%dir %{_vdr_plugin_cfgdir}/graphTFT
%dir %{_vdr_plugin_cfgdir}/graphTFT/themes
%dir %{_vdr_plugin_cfgdir}/graphTFT/fonts
%{_vdr_plugin_cfgdir}/graphTFT/fonts/Vera.ttf


