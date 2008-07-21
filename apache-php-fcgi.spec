%define		apxs	/usr/sbin/apxs1
Summary:	Support for the PHP via FastCGI protocol for Apache webserver
Name:		apache1-php-fcgi
Version:	5.2.6
Release:	1
License:	GPL
Group:		Applications/WWW
BuildRequires:	apache1-devel >= 1.3.39
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache1-mod_fastcgi
Requires:	php-fcgi >= 4:%{version}
Requires:	php-fcgi-init
Provides:	webserver(php) = %{version}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)
%define		fcgiapp		/usr/bin/php.fcgi

%description
This virtual package provides support for the PHP via FastCGI
protocol.

%prep
%setup -qcT

cat <<'EOF' > apache.conf
# setup via fastcgi to run php5
<IfModule mod_fastcgi.c>
	# the server name is bogus actually, to satisfy mod_fastcgi
	FastCgiExternalServer %{fcgiapp} -socket /var/run/php/fcgi.sock
	ScriptAlias /php-fcgi %{fcgiapp}
	<Location "/php-fcgi">
		SetHandler fastcgi-script
		Allow from all
	</Location>

	Action application/x-httpd-php-fcgi /php-fcgi
</IfModule>

# To register handler for .php in your config context:
#<IfModule mod_fastcgi.c>
#	AddType application/x-httpd-php-fcgi .php
#</IfModule>
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/conf.d
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_php-fcgi.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_php-fcgi.conf
