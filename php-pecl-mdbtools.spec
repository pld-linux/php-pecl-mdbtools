%define		_modname	mdbtools
%define		_status		stable
Summary:	%{_modname} - MDB data file access library
Summary(pl.UTF-8):	%{_modname} - biblioteka dostępu do plików MDB
Name:		php-pecl-%{_modname}
Version:	1.0.0
Release:	4
License:	LGPL
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	758f844257c50dbd07c2b9a67a83954b
Patch0:		%{name}-paths.patch
URL:		http://pecl.php.net/package/mdbtools/
BuildRequires:	mdbtools-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mdbtools provides read access to MDB data files as used by Microsoft
Access and its underlying JetEngine.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
mdbtools udostępnia możliwość odczytu danych zapisanych w plikach MDB,
z których korzysta baza danych Microsoft Access oraz zwązany z tą
aplikacją silnik JetEngine.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c
%patch0 -p1

%build
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	-C %{_modname}-%{version} \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}

cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
