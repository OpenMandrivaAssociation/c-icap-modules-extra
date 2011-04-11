%define epoch 1
%define _disable_libtoolize 1

Summary:	An ICAP module server coded in C
Name:		c-icap-modules-extra
Version:	0.1.5
Release:	%mkrel 2
License:	GPL
Group:		System/Servers
URL:		http://sourceforge.net/projects/c-icap/
Source0:	http://prdownloads.sourceforge.net/c-icap/c_icap_modules-%{version}.tar.gz
BuildRequires:	clamav-devel
BuildRequires:  c-icap-devel
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  dos2unix
Requires:	c-icap-server

Epoch:		%{epoch}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
find -type f | grep -v "\.gif" | grep -v "\.png" | grep -v "\.jpg" | xargs dos2unix -U

chmod 644 AUTHORS COPYING 


%build
export WANT_AUTOCONF_2_5=1
libtoolize --copy --force; aclocal; autoconf; automake --foreign --add-missing --copy

export LIBS="-lpthread -ldl"

%configure2_5x \
    --disable-static \
    --enable-shared \
    --with-clamav=%{_prefix} \
    --with-c-icap=%{_prefix}

%make

%install
rm -rf %{buildroot}

%{__mkdir_p} %{buildroot}/%{_sysconfdir}/icapd
%makeinstall_std CONFIGDIR=/etc/icapd


# cleanup
rm -f %{buildroot}%{_libdir}/c_icap/*.*a
rm -f %{buildroot}%{_libdir}/*.*a

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun  -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc AUTHORS COPYING 
%dir %{_libdir}/c_icap
%dir %{_sysconfdir}
%dir %{_sysconfdir}/icapd
%attr(0755,root,root) %{_libdir}/c_icap/*.so
%{_sysconfdir}/icapd/srv_clamav.conf
%{_sysconfdir}/icapd/srv_url_check.conf
%{_sysconfdir}/icapd/srv_clamav.conf.default
%{_sysconfdir}/icapd/srv_url_check.conf.default
