Summary:	WebSVN - web interface of Subversion repositories
Summary(pl.UTF-8):   WebSVN - przeglądarka WWW repozytoriów Subversion
Name:		websvn
Version:	1.40
Release:	0.beta.1
Epoch:		0
License:	GPL
Group:		Development/Tools
Source0:	http://websvn.tigris.org/files/documents/1380/13981/WebSVN_140beta.tar.gz
# Source0-md5:	fced148662b41fcf2a8effdfbc982553
Patch0:		%{name}-ver.patch
URL:		http://websvn.tigris.org/
Requires:	apache
Requires:	php-pear
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

%description -l pl.UTF-8
WebSVN oferuje widok na repozytoria Subversion, zaprojektowany w
sposób odzwierciedlający metodologię Subversion. Można oglądać logi
dowolnego pliku lub katalogu, zobaczyć listę wszystkich zmienionych,
dodanych i usuniętych w danej rewizji plików. Można także oglądać
różnice między 2 wersjami pliku, aby zobaczyć co dokładnie się
zmieniło w danej rewizji.

WebSVN oferuje następujące możliwości:
 - łatwy w użyciu interfejs
 - wysoko konfigurowalny system szablonów
 - przeszukiwanie logów
 - kolorowanie listingów plików
 - szybkie przeglądanie dzięki wewnętrznemu buforowaniu
 - obsługę MultiViews w Apache'u.

Ponieważ WebSVN jest napisany w PHP, jest przenośny i łatwy w
instalacji.

# have mercy and don't move this definition between preamble and descriptions
%define	_websvndir	%{_datadir}/%{name}

%prep
%setup -q -n WebSVN
%patch0 -p1

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
ln -sf	%{_sysconfdir}/websvn.conf		$RPM_BUILD_ROOT%{_websvndir}/include/config.inc
echo 	Alias /websvn /usr/share/websvn >	$RPM_BUILD_ROOT%{_sysconfdir}/httpd/websvn.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*websvn.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
elif [ -d /etc/httpd/httpd.conf ]; then
	mv -f /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
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
rm -fr %{_var}/cache/%{name}

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
%lang(pt) %{_websvndir}/languages/portuguese.inc
%{_websvndir}/temp
%{_websvndir}/templates
%attr(700,http,root) %{_var}/cache/%{name}
