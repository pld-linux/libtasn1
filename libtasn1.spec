Summary:	ASN.1 library used in GNUTLS
Summary(pl):	Biblioteka ASN.1 u¿ywana w GNUTLS
Name:		libtasn1
Version:	0.2.4
Release:	1
License:	LGPL
Group:		Libraries
Source0:	ftp://ftp.gnutls.org/pub/gnutls/libtasn1/%{name}-%{version}.tar.gz
URL:		http://www.gnu.org/software/gnutls/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	libtool
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

%description -l pl
Biblioteka libasn1 stworzona do zarz±dzania strukturami ASN1 (Abstract
Syntax Notation One). G³ówne cechy biblioteki to:
- zarz±dzanie strukturami ASN1 w sposób nie wymagaj±cy generowania
  plików z kodem w C
- zarz±dzanie strukturami ASN1 w sposób umo¿liwiaj±cy generowanie
  plików z kodem w C
- kodowanie DER (Distinguish Encoding Rules)
- brak limitów dla warto¶ci INTEGER oraz ENUMERATED

%package devel
Summary:	Header files etc to develop libtasn1 applications
Summary(pl):	Pliki nag³ówkowe i inne do libtasn1
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
Header files etc to develop libtasn1 applications.

%description devel -l pl
Pliki nag³ówkowe i inne do libtasn1.

%package static
Summary:	Static libtasn1 library
Summary(pl):	Biblioteka statyczna libtasn1
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static libtasn1 library.

%description static -l pl
Biblioteka statyczna libtasn1.

%prep
rm -f missing
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README THANKS doc/*.ps
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
