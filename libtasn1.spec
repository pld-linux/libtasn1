#
# Conditional build:
%bcond_without	apidocs		# gtk-doc based API documentation
%bcond_without	static_libs	# static library

Summary:	ASN.1 library used in GNUTLS
Summary(pl.UTF-8):	Biblioteka ASN.1 używana w GNUTLS
Name:		libtasn1
Version:	4.20.0
Release:	1
License:	LGPL v2.1+ (library), GPL v3+ (tools)
Group:		Libraries
Source0:	https://ftp.gnu.org/gnu/libtasn1/%{name}-%{version}.tar.gz
# Source0-md5:	930f71d788cf37505a0327c1b84741be
Patch0:		%{name}-info.patch
URL:		http://www.gnu.org/software/libtasn1/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	docbook-dtd412-xml
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.4}
BuildRequires:	gtk-doc-automake >= 1.4
BuildRequires:	help2man
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
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
Conflicts:	libtasn1-devel < 0.3.9-2
BuildArch:	noarch

%description apidocs
libtasn1 API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libtasn1.

%prep
%setup -q
%patch -P0 -p1

%build
%{?with_apidocs:%{__gtkdocize}}
%{__libtoolize}
%{__aclocal} -I m4 -I src/gl/m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gtk-doc%{!?with_apidocs:=no} \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
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
%doc AUTHORS ChangeLog NEWS README.md THANKS
%attr(755,root,root) %{_bindir}/asn1*
%attr(755,root,root) %{_libdir}/libtasn1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtasn1.so.6
%{_mandir}/man1/asn1*.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtasn1.so
%{_libdir}/libtasn1.la
%{_includedir}/libtasn1.h
%{_pkgconfigdir}/libtasn1.pc
%{_infodir}/libtasn1.info*
%{_mandir}/man3/asn1_*.3*

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
