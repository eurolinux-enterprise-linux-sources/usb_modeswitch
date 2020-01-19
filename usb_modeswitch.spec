%define source_name	usb-modeswitch

Name:		usb_modeswitch
Version:	2.4.0
Release:	5%{?dist}
Summary:	USB Modeswitch gets mobile broadband cards in operational mode
Summary(de):	USB Modeswitch aktiviert UMTS-Karten
Group:		Applications/System
License:	GPLv2+
URL:		http://www.draisberghof.de/usb_modeswitch/

Source0:	http://www.draisberghof.de/%{name}/%{source_name}-%{version}.tar.bz2
Source1:	http://www.draisberghof.de/usb_modeswitch/device_reference.txt

# http://www.draisberghof.de/usb_modeswitch/bb/viewtopic.php?f=2&t=2546
Patch0: rhbz948451-fix-manual-pages.patch

# http://www.draisberghof.de/usb_modeswitch/bb/viewtopic.php?f=2&t=2556
Patch1: 0001-Fix-crash-on-early-fail.patch

# http://www.draisberghof.de/usb_modeswitch/bb/viewtopic.php?f=2&t=2557
Patch2: 0001-usb_modeswitch-don-t-return-a-value-from-stack.patch

# http://www.draisberghof.de/usb_modeswitch/bb/viewtopic.php?f=2&t=2560
Patch3: 0001-Bring-back-the-module-binding.patch

BuildRequires:	libusbx-devel
BuildRequires:	systemd
Requires:	usb_modeswitch-data >= 20121109
Requires:	systemd

%description
USB Modeswitch brings up your datacard into operational mode. When plugged
in they identify themselves as cdrom and present some non-Linux compatible
installation files. This tool deactivates this cdrom-device and enables
the real communication device. It supports most devices built and
sold by Huawei, T-Mobile, Vodafone, Option, ZTE, Novatel.

%description	-l de
USB Modeswitch deaktiviert die CDROM-Emulation einiger UMTS-Karten.
Dadurch erkennt Linux die Datenkarte und kann damit Internet-
Verbindungen aufbauen. Die gängigen Karten von Huawei, T-Mobile,
Vodafone, Option, ZTE und Novatell werden unterstützt.


%prep
%setup -q -n %{source_name}-%{version}
%patch0 -p1 -b .manpage
%patch1 -p1 -b .libusb_exit
%patch2 -p1 -b .stack
%patch3 -p1 -b .binding

# convert device_reference.txt encoding to UTF-8
iconv --from=ISO-8859-1 --to=UTF-8 %{SOURCE1} >device_reference.txt
touch -r %{SOURCE1} device_reference.txt

# Fix the ppc64le build
cp -f /usr/lib/rpm/redhat/config.guess jim/autosetup/config.guess
cp -f /usr/lib/rpm/redhat/config.sub jim/autosetup/config.sub


%build
CFLAGS="$RPM_OPT_FLAGS" make %{?_smp_mflags} static


%install
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
make install-static \
	DESTDIR=$RPM_BUILD_ROOT \
	SYSDIR=$RPM_BUILD_ROOT%{_unitdir} \
	UDEVDIR=$RPM_BUILD_ROOT%{_prefix}/lib/udev


%files
%{_sbindir}/usb_modeswitch
%{_sbindir}/usb_modeswitch_dispatcher
%{_mandir}/man1/usb_modeswitch.1.gz
%{_mandir}/man1/usb_modeswitch_dispatcher.1.gz
%{_prefix}/lib/udev/usb_modeswitch
%{_unitdir}/usb_modeswitch@.service
%config(noreplace) %{_sysconfdir}/usb_modeswitch.conf
%doc COPYING README ChangeLog device_reference.txt 


%changelog
* Thu Jul 21 2016 Lubomir Rintel <lkundrak@v3.sk> - 2.4.0-5
- Bring back the module binding

* Thu Jul 21 2016 Lubomir Rintel <lkundrak@v3.sk> - 2.4.0-4
- Actually apply the patch for previous issue

* Thu Jul 21 2016 Lubomir Rintel <lkundrak@v3.sk> - 2.4.0-3
- Fix undefined behavior in config parser (rh #1352055)

* Wed Jul 20 2016 Lubomir Rintel <lkundrak@v3.sk> - 2.4.0-2
- Add the previously omitted systemd service file (rh #1352055)
- Fix crash with invalid arguments (rh #1358472)

* Wed Jun 22 2016 Lubomir Rintel <lkundrak@v3.sk> - 2.4.0-1
- New 2.4.0 release

* Fri Jul 11 2014 Dan Winship <danw@redhat.com> - 1.2.7-6
- Fix build on aarch64 (#1061556)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.2.7-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.2.7-4
- Mass rebuild 2013-12-27

* Wed Aug 28 2013 Thomas Haller <thaller@redhat.com> 1.2.7-3
- Add manual page for usb_modeswitch_dispatcher and fix errors in
  manual page of usb_modeswitch (rhbz#948451, rhbz#884203).

* Mon Aug 26 2013 Dan Williams <dcbw@redhat.com> - 1.2.7-2
- Fix udev helper path

* Fri Aug 16 2013 Dan Williams <dcbw@redhat.com> - 1.2.7-1
- New upstream release

* Fri Jul 26 2013 Dan Williams <dcbw@redhat.com> - 1.2.6-2
- Fix udev directories

* Wed Jun 12 2013 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 1.2.6
- New upstream release.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 1.2.5-1
- New upstream release. Resolves rhbz#875832

* Fri Aug 24 2012 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 1.2.4-1
- New upstream release. Resolves rhbz#785539

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 24 2012 Dan Williams <dcbw@redhat.com> 1.2.3-1
- Update to new upstream release
- Build TCL tool as a static binary to remove dependency on TCL itself rhbz#760839

* Wed Jan 25 2012 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1.2.2-2
- Add usb_modeswitch.sh udev script and move Tcl dispatcher script to sbindir,
  resolves rhbz#782614, patch from Dominic Cleal
- Fix bus/device-based search, from deb#656248

* Fri Jan 20 2012 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1.2.2
- New upstream version 1.2.2

* Fri Jan 06 2012 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1.2.1-1
- New upstream version 1.2.1

* Tue Oct 25 2011 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1.2.0-1
- New upstream
- use device_reference.txt from upstream

* Mon Mar 28 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 1.1.7-1
- New upstream release.  Resolves rhbz#625004
- Update spec to match current guidelines
- Fix relevant rpmlint errors and warnings

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 30 2010 Dan Williams <dcbw@redhat.com> 1.1.6-1
- New upstream version

* Tue Aug 24 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1.1.4-1
- New upstream version

* Tue Jun 22 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1.1.3-1
- New upstream

* Fri Apr 23 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 1.1.2-3
- Fix typo in binary location

* Fri Apr 23 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 1.1.2-2
- Move usb_modeswitch binary back to /usr/sbin
- Package /etc/usb_modeswitch.setup for manual mode

* Tue Apr 20 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 1.1.2-1
- New upstream
- Split data and main package

* Mon Mar 8 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> - 1.1.0-6
- Version bump for F-12 build

* Sat Mar 6 2010 Huzaifa Sidhpurwala <huzaifas@redaht.com> - 1.1.0-5
- Fix regression in rhbz #571001
- Version bump

* Thu Mar 4 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1.1.0-3
- Patch usb_modeswitch to use the binary from /usr/bin/
- usb_modeswitch-data needs tcl

* Tue Mar 2 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1.1.0-2
- Reload udev when new rules are installed

* Tue Mar 2 2010 Huzaifa Sidhpurwala <huzaifas@redhat.com> 1.1.0-1
- New upstream 1.1.0 release
- Split package into binary and data part

* Thu Sep 17 2009 Peter Robinson <pbrobinson@gmail.com> 1.0.5-1
- new upstream 1.0.5 release

* Sun Aug 02 2009 Robert M. Albrecht <fedora@romal.de> 1.0.2-1
- new upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 11 2009 Robert M. Albrecht <fedora@romal.de> 0.9.6-1
* new upstream release

* Sat Dec 13 2008 Robert M. Albrecht <fedora@romal.de> 0.9.5-1
* new upstream release

* Sun Jun 22 2008 Robert M. Albrecht <romal@gmx.de> 0.9.4-2
- Fixed some rpmlint errors
- Added german translation

* Sun Jun 22 2008 Robert M. Albrecht <romal@gmx.de> 0.9.4-1
- Update to 0.9.4
- Honor RPM_OPT_FLAGS
  
* Mon May 26 2008 Robert M. Albrecht <romal@gmx.de> 0.9.4-0.1.beta2
- First package Release

