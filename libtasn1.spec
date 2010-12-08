#
# Conditional build:
%bcond_without	apidocs		# disable gtk-doc
%bcond_without	static_libs	# don't build static library
#
Summary:	ASN.1 library used in GNUTLS
Summary(pl.UTF-8):	Biblioteka ASN.1 używana w GNUTLS
Name:		libtasn1
Version:	2.9
Release:	1
License:	LGPL v2.1+ (library), GPL v3+ (tools)
Group:		Libraries
Source0:	ftp://ftp.gnutls.org/pub/gnutls/libtasn1/%{name}-%{version}.tar.gz
# Source0-md5:	f4f4035b84550100ffeb8ad4b261dea9
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/gnutls/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake >= 1:1.10
BuildRequires:	docbook-dtd412-xml
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.4}
BuildRequires:	gtk-doc-automake >= 1.4
BuildRequires:	libtool
BuildRequires:	pkgconfig
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
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files etc to develop libtasn1 applications.

%description devel -l pl.UTF-8
Pliki nagłówkowe i inne do libtasn1.

%package static
Summary:	Static libtasn1 library
Summary(pl.UTF-8):	Biblioteka statyczna libtasn1
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libtasn1 library.

%description static -l pl.UTF-8
Biblioteka statyczna libtasn1.

%package apidocs
Summary:	libtasn1 API documentation
Summary(pl.UTF-8):	Dokumentacja API libtasn1
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libtasn1 API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libtasn1.

%prep
%setup -q
%patch0 -p1

%build
%{?with_apidocs:%{__gtkdocize}}
%{__libtoolize}
%{__aclocal} -I m4 -I gl/m4 -I lib/glm4
%{__automake}
%{__autoheader}
%{__autoconf}

%configure \
	--%{?with_apidocs:en}%{!?with_apidocs:dis}able-gtk-doc \
	--%{?with_static_libs:en}%{!?with_static_libs:dis}able-static \
	%{?with_apidocs:--with-html-dir=%{_gtkdocdir}} \
	--with-packager="PLD/Linux" \
	--with-packager-bug-reports="http://bugs.pld-linux.org/"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS doc/*.html
%attr(755,root,root) %{_bindir}/asn1*
%attr(755,root,root) %{_libdir}/libtasn1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtasn1.so.3
%{_mandir}/man1/asn1*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtasn1.so
%{_libdir}/libtasn1.la
%{_includedir}/libtasn1.h
%{_pkgconfigdir}/libtasn1.pc
%{_infodir}/libtasn1.info*
%{_mandir}/man3/asn1_*.3*
%{_mandir}/man3/libtasn1_*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libtasn1.a
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/%{name}
%endif
