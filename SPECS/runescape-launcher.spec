%define debug_package %{nil}

Name:           runescape-launcher
Version:        2.2.11
Release:        1%{?dist}
ExclusiveArch:  x86_64
License:        Runescape
Summary:        RuneScape Game Client
Url:            https://www.runescape.com/
Source0:        https://content.runescape.com/downloads/ubuntu/pool/non-free/r/runescape-launcher/runescape-launcher_%{version}_amd64.deb

Requires:       libcurl libGLEW
Requires:       SDL2 gtk2 libpng libvorbis
Requires:       xdotool

BuildRequires:  desktop-file-utils
# For _kde4_* macros:
BuildRequires:  kde-filesystem

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
sed -i 's|PULSE_LATENCY_MSEC=100|PULSE_LATENCY_MSEC=200|' usr/bin/runescape-launcher

%build

%install
install -Dm 0644 runescape-launcher-%{version}/usr/share/doc/runescape-launcher/copyright %{buildroot}%{_docdir}/runescape-launcher/copyright
install -Dm 0644 runescape-launcher-%{version}/usr/share/doc/runescape-launcher/changelog.gz %{buildroot}%{_docdir}/runescape-launcher/changelog.gz
export QA_RPATHS=0x0002
install -Dm 0755 runescape-launcher-%{version}/usr/share/games/runescape-launcher/runescape %{buildroot}%{_datadir}/games/runescape-launcher/runescape
install -Dm 0644 runescape-launcher-%{version}/usr/share/games/runescape-launcher/runescape.png %{buildroot}%{_datadir}/games/runescape-launcher/runescape.png
desktop-file-install runescape-launcher-%{version}/usr/share/applications/runescape-launcher.desktop
install -Dm 0644 runescape-launcher-%{version}/usr/share/kde4/services/rs-launchs.protocol %{buildroot}%{_kde4_sharedir}/kde4/services/rs-launchs.protocol
install -Dm 0644 runescape-launcher-%{version}/usr/share/kde4/services/rs-launch.protocol %{buildroot}%{_kde4_sharedir}/kde4/services/rs-launch.protocol
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/
%__cp -r runescape-launcher-%{version}/usr/share/icons/hicolor/* %{buildroot}%{_datadir}/icons/hicolor/
install -Dm 0755 runescape-launcher-%{version}/usr/bin/runescape-launcher %{buildroot}%{_bindir}/runescape-launcher

%post
if [ $1 -eq 1 ]; then
    touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
fi

%postun
if [ $1 -eq 0 ]; then
    touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
    gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
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


%changelog
* Fri Mar 10 2023 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.11-1
- Updated runescape.deb to 2.2.11

* Sat Nov 12 2022 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.10-1
- Updated runescape.deb to 2.2.10

* Sat Mar 26 2022 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.9-4
- Updated runescape.deb to 2.2.9

* Wed Nov 10 2021 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.9-3
- Updated runescape.deb to 2.2.9

* Thu Jul 29 2021 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.9-2
- Updated runescape.deb to 2.2.9

* Thu Apr 29 2021 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.9-1
- Updated runescape.deb to 2.2.9

* Mon Dec 7 2020 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.8-1
- Updated runescape.deb to 2.2.8

* Tue Oct 13 2020 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.7-4
- Updated runescape.deb

* Sat Jun 6 2020 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.7-3
- Updated runescape.deb
- Removed unneeded private libs

* Fri Jun 5 2020 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.7-2
- Updated runescape.deb

* Wed Apr 29 2020 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.6-1.16
- Runescape deb version 2.2.7

* Sat Feb 01 2020 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.6-1.15
- Runescape binary changed by Jagex 2020-01-03

* Thu Oct 31 2019 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.4-1.14
- Runescape binary changed by Jagex 2019-10-07

* Tue Jun 11 2019 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.4-1.13
- Runescape binary changed by Jagex 2019-05-30
- Updated libpng version

* Mon Apr 29 2019 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.4-1.12
- Runescape binary changed by Jagex 2019-04-17

* Tue Feb 05 2019 Johan Heikkila <johan.heikkila@gmail.com> - 2.2.4-1.11
- Runescape binary changed by Jagex 2019-01-21
- Updated curl version. Added xdotool to hide launch window.

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
