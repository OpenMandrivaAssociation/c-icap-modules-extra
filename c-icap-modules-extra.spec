%define epoch 1
%define _disable_libtoolize 1

Summary:	An ICAP module server coded in C
Name:		c-icap-modules-extra
Version:	0.2.4
Release:	1
License:	GPL
Group:		System/Servers
URL:		http://sourceforge.net/projects/c-icap/
Source0:	http://sourceforge.net/projects/c-icap/files/c-icap-modules/0.2.x/c_icap_modules-%{version}.tar.gz
BuildRequires:	clamav-devel
BuildRequires:  c-icap-devel
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  dos2unix
BuildRequires:	db-devel 
Requires:	c-icap-server

Epoch:		%{epoch}

%description
An ICAP modules server coded in C


%prep

%setup -q -n c_icap_modules-%{version}

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find -type f | grep -v "\.gif" | grep -v "\.png" | grep -v "\.jpg" | xargs dos2unix

chmod 644 AUTHORS COPYING 


%build
export WANT_AUTOCONF_2_5=1
libtoolize --copy --force; aclocal; autoconf; automake --foreign --add-missing --copy

export LIBS="-lpthread -ldl"

%configure2_5x \
    --disable-static \
    --enable-shared \
    --with-clamav=%{_prefix} \
    --with-c-icap=%{_prefix} \
    --with-bdb

perl -pi -e 's|(srv_clamav_la_LIBADD =  -L)/usr/lib|$1%{_libdir}|;'    \
        services/clamav/Makefile

%make

%install
%{__mkdir_p} %{buildroot}/%{_sysconfdir}/icapd
%makeinstall_std CONFIGDIR=/etc/icapd


# cleanup
rm -f %{buildroot}%{_libdir}/c_icap/*.*a
rm -f %{buildroot}%{_libdir}/*.*a

%files 
%doc AUTHORS COPYING 
%dir %{_libdir}/c_icap
%dir %{_sysconfdir}/icapd
%attr(0755,root,root) %{_libdir}/c_icap/*.so
%config(noreplace) %{_sysconfdir}/icapd/*.conf
%{_sysconfdir}/icapd/*.conf.default
%{_datadir}/с_icap/templates/virus_scan/en/*
%{_datadir}/c_icap/templates/srv_url_check/en/*
%{_mandir}/man8/*
%{_bindir}/*



%changelog
* Tue May 08 2012 Crispin Boylan <crisb@mandriva.org> 1:0.1.6-5
+ Revision: 797504
- Rebuild

* Mon Jul 25 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1:0.1.6-4
+ Revision: 691611
- Trying to make a single RPM compatible with both distros, anyway it helps me to maintain both

* Sat May 28 2011 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1:0.1.6-3
+ Revision: 681328
- 0.1.6
- bump
- Do not overwrite conf
- Do not overwrite conf
- Squidguard support
- no libtoolize
- 0.1.5

* Sun Dec 26 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1:0.1.3-1mdv2011.0
+ Revision: 625257
- 0.1.3
  Lest upse current automake,autoconf not the 1.7

* Sat Oct 16 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1:0.1.2-1mdv2011.0
+ Revision: 585950
- 0.1.2

* Sat Jul 24 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1:0.1.1-3mdv2011.0
+ Revision: 557343
- perl rebuild

* Sun Jul 04 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1:0.1.1-2mdv2011.0
+ Revision: 549779
- bumprelease

* Sat Jul 03 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1:0.1.1-1mdv2010.1
+ Revision: 549767
- 0.1.1

* Fri Apr 30 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1:0.1.1-0.pre2.2mdv2010.1
+ Revision: 541151
- We move all configuration into /etc/icapd

* Thu Apr 29 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1:0.1.1-0.pre2.1mdv2010.1
+ Revision: 540862
- New pre2

* Thu Apr 29 2010 Luis Daniel Lucio Quiroz <dlucio@mandriva.org> 1:0.1.1-0.pre1.1mdv2010.1
+ Revision: 540725
- import c-icap-modules-extra


