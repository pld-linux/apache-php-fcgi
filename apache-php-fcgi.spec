%define		apxs	/usr/sbin/apxs
Summary:	Support for the PHP via FastCGI protocol for Apache webserver
Name:		apache-php-fcgi
Version:	5.6
Release:	1
License:	GPL
Group:		Applications/WWW
Source0:	apache.conf
BuildRequires:	apache-devel >= 1.3.39
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache-mod_fastcgi
Requires:	php(fcgi)
Requires:	php-fcgi-init
Provides:	webserver(php) = %{version}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This virtual package provides support for the PHP via FastCGI
protocol.

%prep
%setup -qcT

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/conf.d
cp -p %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_php-fcgi.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_php-fcgi.conf
