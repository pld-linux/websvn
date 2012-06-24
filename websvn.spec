Summary:	WebSVN - web interface of Subversion repositories
Summary(pl):	WebSVN - przegl�darka WWW repozytori�w Subversion
Name:		websvn
Version:	1.61
Release:	0.1
Epoch:		0
License:	GPL
Group:		Development/Tools
Source0:	http://websvn.tigris.org/files/documents/1380/14334/WebSVN_161.tar.gz
# Source0-md5:	9f81a3793d08bde2e425d2c98f923875
URL:		http://websvn.tigris.org/
Requires:	apache
Requires:	php-pear
Requires:	php-zlib
Requires:	subversion
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
WebSVN offers a view onto your subversion repositories that's been
designed to reflect the Subversion methodology. You can view the log
of any file or directory and see a list of all the files changed,
added or deleted in any given revision. You can also view the
differences between 2 versions of a file so as to see exactly what was
changed in a particular revision.

WebSVN offers the following features:
 - Easy to use interface
 - Highly customisable templating system
 - Log message searching
 - Colourisation of file listings
 - Fast browsing thanks to internal caching feature
 - Apache MultiViews support

Since it's written using PHP, WebSVN is also very portable and easy to
install.

%description -l pl
WebSVN oferuje widok na repozytoria Subversion, zaprojektowany w
spos�b odzwierciedlaj�cy metodologi� Subversion. Mo�na ogl�da� logi
dowolnego pliku lub katalogu, zobaczy� list� wszystkich zmienionych,
dodanych i usuni�tych w danej rewizji plik�w. Mo�na tak�e ogl�da�
r�nice mi�dzy 2 wersjami pliku, aby zobaczy� co dok�adnie si�
zmieni�o w danej rewizji.

WebSVN oferuje nast�puj�ce mo�liwo�ci:
 - �atwy w u�yciu interfejs
 - wysoko konfigurowalny system szablon�w
 - przeszukiwanie log�w
 - kolorowanie listing�w plik�w
 - szybkie przegl�danie dzi�ki wewn�trznemu buforowaniu
 - obs�ug� MultiViews w Apache'u.

Poniewa� WebSVN jest napisany w PHP, jest przeno�ny i �atwy w
instalacji.

# have mercy and don't move this definition between preamble and descriptions
%define	_websvndir	%{_datadir}/%{name}

%prep
%setup -q -n WebSVN

%install
rm -rf $RPM_BUILD_ROOT

install -d \
	$RPM_BUILD_ROOT{%{_sysconfdir}/httpd,%{_var}/cache/%{name}/temp} \
	$RPM_BUILD_ROOT%{_websvndir}/{include,languages,templates/{BlueGrey,Standard}}

install *.php					$RPM_BUILD_ROOT%{_websvndir}
mv -f	include/distconfig.inc			$RPM_BUILD_ROOT%{_sysconfdir}/websvn.conf
install include/*				$RPM_BUILD_ROOT%{_websvndir}/include
install languages/*				$RPM_BUILD_ROOT%{_websvndir}/languages
install	templates/BlueGrey/*			$RPM_BUILD_ROOT%{_websvndir}/templates/BlueGrey
install	templates/Standard/*			$RPM_BUILD_ROOT%{_websvndir}/templates/Standard
rm -fr	cache temp
ln -sf	%{_var}/cache/%{name}/temp		$RPM_BUILD_ROOT%{_websvndir}/temp
ln -sf	%{_var}/cache/%{name}			$RPM_BUILD_ROOT%{_websvndir}/cache
ln -sf	%{_sysconfdir}/%{name}.conf		$RPM_BUILD_ROOT%{_websvndir}/include/config.inc
echo 	Alias "/%{name}" "%{_websvndir}" >	$RPM_BUILD_ROOT%{_sysconfdir}/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*websvn.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
elif [ -d /etc/httpd/httpd.conf ]; then
	ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*websvn.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
		if [ -f /var/lock/subsys/httpd ]; then
			/usr/sbin/apachectl restart 1>&2
		fi
	fi
fi
%postun
rm -fr %{_var}/cache/%{name}/*

%files
%defattr(644,root,root,755)
%doc changes.txt install.txt templates.txt
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/%{name}.conf
%{_sysconfdir}/httpd/*
%dir %{_websvndir}
%{_websvndir}/*.php
%{_websvndir}/cache
%{_websvndir}/include
%dir %{_websvndir}/languages
%{_websvndir}/languages/english.inc
%lang(de) %{_websvndir}/languages/german.inc
%lang(fr) %{_websvndir}/languages/french.inc
%lang(ja) %{_websvndir}/languages/japanese*.inc
%lang(ko) %{_websvndir}/languages/korean-euc.inc
%lang(ko) %{_websvndir}/languages/korean-utf8.inc
%lang(pt) %{_websvndir}/languages/portuguese.inc
%lang(ru) %{_websvndir}/languages/russian.inc
%lang(es) %{_websvndir}/languages/spanish.inc
%lang(se) %{_websvndir}/languages/swedish.inc
%lang(zh_TW) %{_websvndir}/languages/tchinese-utf8.inc
%lang(zh_TW) %{_websvndir}/languages/tchinese.inc

%{_websvndir}/temp
%{_websvndir}/templates
%attr(700,http,root) %{_var}/cache/%{name}
