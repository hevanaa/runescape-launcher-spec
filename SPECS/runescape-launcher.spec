%define debug_package %{nil}
%define curlversion 7.53.1
%define glewversion 1.10.0
%define libpngversion 1.2.54
%define privatelibdir /opt/runescape-nxt-libs
Name:           runescape-launcher
Version:        2.2.4
Release:        1.10%{?dist}
ExclusiveArch:  x86_64
License:        Runescape
Summary:        RuneScape Game Client
Url:            https://www.runescape.com/
Source0:        https://content.runescape.com/downloads/ubuntu/pool/non-free/r/runescape-launcher/runescape-launcher_%{version}_amd64.deb
# The client is proprietary and must have two Ubuntu-style libraries.
# Libcurl needs ssl support. We can't just build older rpms of the libraries.
Source1:        https://curl.haxx.se/download/curl-%{curlversion}.tar.gz
Source2:        http://downloads.sourceforge.net/glew/glew-%{glewversion}.tgz
Source3:        https://downloads.sourceforge.net/project/libpng/libpng12/older-releases/%{libpngversion}/libpng-%{libpngversion}.tar.gz

# Patch the client to use also the private libraries
Patch0:         0001-library_path.patch

# Despite providing separate libcurl and libGLEW, require them for their
# other dependencies
Requires:       libcurl libGLEW
Requires:       SDL2 gtk2 libpng12 libvorbis

BuildRequires:  desktop-file-utils
# For _kde4_* macros:
BuildRequires:  kde-filesystem
# for libGLEW
BuildRequires:  libX11-devel libXext-devel libXi-devel libXmu-devel
BuildRequires:  mesa-libGL-devel libGLU-devel
# libcurl
BuildRequires:  openssl-devel
# libpng
BuildRequires:  zlib

# This needs to be explicitely listed to solve rpm installation dependency
Provides:       libcurl.so.4(CURL_OPENSSL_3)(64bit) = %{curlversion}

%description
RuneScape is a massively multiplayer online role-playing game created by Jagex
Ltd.. This client allows you to play the game as never before! By installing
this software you are agreeing to the End User Licence Agreement (see
/usr/share/doc/runescape-launcher/copyright). The client is written in C++ and
uses OpenGL rendering.

%prep
cd %{_builddir}
rm -rf runescape-launcher-%{version}
mkdir runescape-launcher-%{version}
cd runescape-launcher-%{version}
ar x %{SOURCE0}
tar xvf data.tar.xz
%patch0 -p1

cd %{_builddir}
tar xvf %{SOURCE1}

cd %{_builddir}
tar xvf %{SOURCE2}

cd %{_builddir}
tar xvf %{SOURCE3}

%build
cd %{_builddir}/curl-%{curlversion}
./configure --prefix=%{privatelibdir} --libdir=%{privatelibdir} --with-ssl
make

cd %{_builddir}/glew-%{glewversion}
make LIBDIR=%{privatelibdir}

cd %{_builddir}/libpng-%{libpngversion}
./configure --prefix=%{privatelibdir} --libdir=%{privatelibdir}
make

%install
install -Dm 0644 runescape-launcher-%{version}/usr/share/doc/runescape-launcher/copyright %{buildroot}%{_docdir}/runescape-launcher/copyright
install -Dm 0644 runescape-launcher-%{version}/usr/share/doc/runescape-launcher/changelog.gz %{buildroot}%{_docdir}/runescape-launcher/changelog.gz
install -Dm 0755 runescape-launcher-%{version}/usr/share/games/runescape-launcher/runescape %{buildroot}%{_datadir}/games/runescape-launcher/runescape
install -Dm 0644 runescape-launcher-%{version}/usr/share/games/runescape-launcher/runescape.png %{buildroot}%{_datadir}/games/runescape-launcher/runescape.png
desktop-file-install runescape-launcher-%{version}/usr/share/applications/runescape-launcher.desktop
install -Dm 0644 runescape-launcher-%{version}/usr/share/kde4/services/rs-launchs.protocol %{buildroot}%{_kde4_sharedir}/kde4/services/rs-launchs.protocol
install -Dm 0644 runescape-launcher-%{version}/usr/share/kde4/services/rs-launch.protocol %{buildroot}%{_kde4_sharedir}/kde4/services/rs-launch.protocol
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/
%__cp -r runescape-launcher-%{version}/usr/share/icons/hicolor/* %{buildroot}%{_datadir}/icons/hicolor/
install -Dm 0755 runescape-launcher-%{version}/usr/bin/runescape-launcher %{buildroot}%{_bindir}/runescape-launcher

mkdir -p $RPM_BUILD_ROOT%{privatelibdir}/
%__cp %{_builddir}/curl-%{curlversion}/lib/.libs/libcurl.so.4.4.0 $RPM_BUILD_ROOT%{privatelibdir}/
%__cp %{_builddir}/glew-%{glewversion}/lib/libGLEW.so.1.10.0 $RPM_BUILD_ROOT%{privatelibdir}/
%__cp %{_builddir}/libpng-%{libpngversion}/.libs/libpng12.so.0.54.0 $RPM_BUILD_ROOT%{privatelibdir}/
chmod 0755 $RPM_BUILD_ROOT%{privatelibdir}/*.so*

%post
if [ $1 -eq 1 ]; then
    touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
    ln -s %{privatelibdir}/libcurl.so.4.4.0 %{privatelibdir}/libcurl.so.4
    ln -s %{privatelibdir}/libGLEW.so.1.10.0 %{privatelibdir}/libGLEW.so.1.10
    ln -s %{privatelibdir}/libpng12.so.0.54.0 %{privatelibdir}/libpng12.so.0
fi

%postun
if [ $1 -eq 0 ]; then
    touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
    rm -f %{privatelibdir}/libcurl.so.4
    rm -f %{privatelibdir}/libGLEW.so.1.10
    rm -f %{privatelibdir}/libpng12.so.0
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%{_bindir}/runescape-launcher
%{_datadir}/applications/runescape-launcher.desktop
%{_docdir}/runescape-launcher/changelog.gz
%{_docdir}/runescape-launcher/copyright
%license %{_docdir}/runescape-launcher/copyright
%{_datadir}/games/runescape-launcher/runescape
%{_datadir}/games/runescape-launcher/runescape.png
%{_datadir}/icons/hicolor/*/apps/runescape.png
%dir %{_kde4_sharedir}/kde4/
%dir %{_kde4_sharedir}/kde4/services/
%{_kde4_sharedir}/kde4/services/rs-launch.protocol
%{_kde4_sharedir}/kde4/services/rs-launchs.protocol
%dir %{privatelibdir}/
%{privatelibdir}/*

%changelog
* Sat Nov 10 2018 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.4-1.10
- Runescape binary changed by Jagex 2018-10-31
* Mon Apr 23 2018 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.4-1.9
- Runescape binary changed by Jagex 2018-04-19
* Thu Mar 01 2018 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.4-1.8
- Runescape binary changed by Jagex 2018-02-16
- Added libpng12
* Sat Dec 30 2017 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.4-1.7
- Runescape binary changed by Jagex 2017-11-24
* Sat Nov 25 2017 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.4-1.6
- Runescape binary changed by Jagex 2017-11-14
* Sat Oct 28 2017 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.4-1.5
- Runescape binary changed by Jagex 2017-10-13
* Tue Oct 03 2017 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.4-1.4
- Runescape binary changed by Jagex 2017-09-19
* Sat Sep 23 2017 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.4-1.3
- Runescape binary changed by Jagex 2017-09-12
* Sat Sep 16 2017 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.4-1.2
- Runescape binary changed by Jagex 2017-09-01 for unknown reasons
* Wed Aug 09 2017 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.4-1.1
- Removed webkitgtk, added gtk2
* Tue Aug 08 2017 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.4-1.0
- First Fedora package created from Ubuntu package
- Runescape version 2.2.4 release date Jul 10 2017
- Contains separate private libcurl and libGLEW libraries
