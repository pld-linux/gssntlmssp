# TODO:
# - implement mech.d in heimdal (e.g. by cat /etc/gss/mech.d/*.conf > /etc/gss/mech in %post scripts)
# - apidocs (doxygen config missing)
#
# Conditional build:
%bcond_with	apidocs	# API documentation (doxygen config missing in sources)
#
Summary:	GSSAPI NTLMSSP mechanism
Summary(pl.UTF-8):	Mechanizm GSSAPI NTLMSSP
Name:		gssntlmssp
Version:	0.8.0
Release:	1
License:	LGPL v3+
Group:		Libraries
# also https://github.com/simo5/gss-ntlmssp but no releases there
Source0:	https://releases.pagure.org/gssntlmssp/%{name}-%{version}.tar.gz
# Source0-md5:	69b3b66519b8e2ce945675862029f816
Patch0:		%{name}-heimdal.patch
URL:		https://pagure.io/gssntlmssp
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.11
BuildRequires:	docbook-style-xsl-nons
BuildRequires:	doxygen
BuildRequires:	gettext-tools
BuildRequires:	heimdal-devel
# pkgconfig(wbclient)
BuildRequires:	libsmbclient-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libunistring-devel
BuildRequires:	libxslt-progs
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig >= 1:0.9.0
BuildRequires:	po4a
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A GSSAPI Mechanism that implements NTLMSSP.

%description -l pl.UTF-8
Mechanizm GSSAPI implementujący NTLMSSP.

%package devel
Summary:	Header file for GSSAPI NTLMSSP extensions
Summary(pl.UTF-8):	Plik nagłówkowy rozszerzeń GSSAPI NTLMSSP
Group:		Development/Libraries
Requires:	heimdal-devel

%description devel
Header file with definition for custom GSSAPI extensions for NTLMSSP.

%description devel -l pl.UTF-8
Plik nagłówkowy z definicjami rozszerzeń GSSAPI dla NTLMSSP.

%prep
%setup -q
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4 -I .
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules
%{__make}

%if %{with apidocs}
%{__make} docs
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# loadable module
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gssntlmssp/*.la

install -d $RPM_BUILD_ROOT/etc/gss/mech.d
cp -p examples/mech.ntlmssp $RPM_BUILD_ROOT/etc/gss/mech.d/ntlmssp.conf

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%if 0
# TODO: needs support in heimdal.spec
# (/etc/gss/mech as ghost, move current content with appropriate comment to /etc/gss/mech.d/00_init.conf)
%post
umask 022
cat /etc/gss/mech.d/*.conf >$RPM_BUILD_ROOT/etc/gss/mech

%postun
umask 022
if [ "$1" = "0" ]; then
	cat /etc/gss/mech.d/*.conf >$RPM_BUILD_ROOT/etc/gss/mech
fi
%endif

%files -f %{name}.lang
%defattr(644,root,root,755)
%dir %{_libdir}/gssntlmssp
%attr(755,root,root) %{_libdir}/gssntlmssp/gssntlmssp.so
# TODO: needs to be owned by heimdal.spec?
%dir /etc/gss
%dir /etc/gss/mech.d
/etc/gss/mech.d/ntlmssp.conf
%{_mandir}/man8/gssntlmssp.8*

%files devel
%defattr(644,root,root,755)
%{_includedir}/gssapi/gssapi_ntlmssp.h
