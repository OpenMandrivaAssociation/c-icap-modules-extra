%define epoch 1
%define _disable_libtoolize 1

Summary:	An ICAP module server coded in C

Name:		c-icap-modules-extra
Version:	0.3.2
Release:	1
License:	GPL
Group:		System/Servers
URL:		http://sourceforge.net/projects/c-icap/
Source0:	http://sourceforge.net/projects/c-icap/files/c-icap-modules/0.3.x/c_icap_modules-%{version}.tar.gz
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
%{_datadir}/c_icap/templates/virus_scan/en/*
%{_datadir}/c_icap/templates/srv_url_check/en/*
%{_mandir}/man8/*
%{_bindir}/*




