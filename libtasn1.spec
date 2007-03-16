#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
%bcond_without	static_libs	# don't build static library
#
Summary:	ASN.1 library used in GNUTLS
Summary(pl.UTF-8):	Biblioteka ASN.1 używana w GNUTLS
Name:		libtasn1
Version:	0.3.9
Release:	1
License:	LGPL
Group:		Libraries
Source0:	ftp://ftp.gnutls.org/pub/gnutls/libtasn1/%{name}-%{version}.tar.gz
# Source0-md5:	01e23a6b48a762ce88f178267dbb1458
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/gnutls/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.10
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.4}
BuildRequires:	gtk-doc-automake >= 1.4
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.98
BuildRequires:	texinfo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Library 'libasn1' developed for ASN1 (Abstract Syntax Notation One)
structures management. The main features of this library are:
- on line ASN1 structure management that doesn't require any C code
  file generation.
- off line ASN1 structure management with C code file generation
  containing an array.
- DER (Distinguish Encoding Rules) encoding
- no limits for INTEGER and ENUMERATED values

%description -l pl.UTF-8
Biblioteka libasn1 stworzona do zarządzania strukturami ASN1 (Abstract
Syntax Notation One). Główne cechy biblioteki to:
- zarządzanie strukturami ASN1 w sposób nie wymagający generowania
  plików z kodem w C
- zarządzanie strukturami ASN1 w sposób umożliwiający generowanie
  plików z kodem w C
- kodowanie DER (Distinguish Encoding Rules)
- brak limitów dla wartości INTEGER oraz ENUMERATED

%package devel
Summary:	Header files etc to develop libtasn1 applications
Summary(pl.UTF-8):	Pliki nagłówkowe i inne do libtasn1
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files etc to develop libtasn1 applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe i inne do libtasn1.

%package static
Summary:	Static libtasn1 library
Summary(pl.UTF-8):	Biblioteka statyczna libtasn1
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libtasn1 library.

%description static -l pl.UTF-8
Biblioteka statyczna libtasn1.

%prep
%setup -q
%patch0 -p1

%build
%{?with_apidocs:%{__gtkdocize}}
%{__libtoolize}
%{__aclocal} -I m4 -I gl/m4
%{__automake}
%{__autoheader}
%{__autoconf}

%configure \
	--%{?with_apidocs:en}%{!?with_apidocs:dis}able-gtk-doc \
	%{?with_apidocs:--with-html-dir=%{_gtkdocdir}} \
	--%{?with_static_libs:en}%{!?with_static_libs:dis}able-static \
	--enable-shared

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%postun devel
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS doc/*.html
%attr(755,root,root) %{_bindir}/asn1*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_mandir}/man1/asn1*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/libtasn1-config
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*.h
%{_aclocaldir}/libtasn1.m4
%{_pkgconfigdir}/libtasn1.pc
%{_infodir}/*.info*
%{_mandir}/man3/*.3*
%{?with_apidocs:%{_gtkdocdir}/%{name}}

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
%endif
