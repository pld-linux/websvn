# TODO
# - verify %lang codes
# - protect config, cache and tmp dirs (drop the symlinks)
Summary:	WebSVN - web interface of Subversion repositories
Summary(pl.UTF-8):	WebSVN - przeglądarka WWW repozytoriów Subversion
Name:		websvn
Version:	2.3.1
Release:	0.1
License:	GPL
Group:		Development/Tools
Source0:	http://www.tigris.org/files/documents/1380/47525/%{name}-%{version}.tar.gz
# Source0-md5:	9f81a3793d08bde2e425d2c98f923875
Source1:	apache.conf
Source2:	lighttpd.conf
URL:		http://www.websvn.info/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php-zlib
Requires:	subversion
Requires:	webapps
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}
%define		_cachedir	%{_var}/cache/%{name}

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

%prep
%setup -q

mv include/distconfig.php include/config.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir},%{_cachedir}/temp}

cp -a *.php $RPM_BUILD_ROOT%{_appdir}
cp -a lib templates languages include javascript $RPM_BUILD_ROOT%{_appdir}

ln -sf %{_cachedir} $RPM_BUILD_ROOT%{_appdir}/cache

mv $RPM_BUILD_ROOT%{_appdir}/include/config.php $RPM_BUILD_ROOT%{_sysconfdir}/config.php
ln -sf %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_appdir}/include/config.php

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -a $RPM_BUILD_ROOT%{_sysconfdir}/{apache,httpd}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ "$1" = 0 ]; then
	rm -rf %{_cachedir}/*
fi

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc changes.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/cache
%{_appdir}/include
%{_appdir}/javascript
%{_appdir}/lib
%{_appdir}/templates
%dir %{_appdir}/languages
%{_appdir}/languages/languages.php
%{_appdir}/languages/english.php
%lang(de) %{_appdir}/languages/german.php
%lang(es) %{_appdir}/languages/spanish.php
%lang(fr) %{_appdir}/languages/french.php
%lang(ja) %{_appdir}/languages/japanese*.php
%lang(pt) %{_appdir}/languages/portuguese.php
%lang(ru) %{_appdir}/languages/russian.php
%lang(se) %{_appdir}/languages/swedish.php
%lang(ca) %{_appdir}/languages/catalan.php
%lang(zh_CN) %{_appdir}/languages/chinese-simplified.php
%lang(zh_TW) %{_appdir}/languages/chinese-traditional.php
%lang(cz) %{_appdir}/languages/czech.php
%lang(da) %{_appdir}/languages/danish.php
%lang(nl) %{_appdir}/languages/dutch.php
%lang(fi) %{_appdir}/languages/finnish.php
%lang(he) %{_appdir}/languages/hebrew.php
%lang(hi) %{_appdir}/languages/hindi.php
%lang(hu) %{_appdir}/languages/hungarian.php
%lang(id) %{_appdir}/languages/indonesian.php
%lang(it) %{_appdir}/languages/italian.php
%lang(ko) %{_appdir}/languages/korean.php
%lang(ma) %{_appdir}/languages/marathi.php
%lang(nb) %{_appdir}/languages/norwegian.php
%lang(pl) %{_appdir}/languages/polish.php
%lang(pt_BR) %{_appdir}/languages/portuguese-br.php
%lang(sk) %{_appdir}/languages/slovak.php
%lang(sk) %{_appdir}/languages/slovenian.php
%lang(tr) %{_appdir}/languages/turkish.php
%lang(uz) %{_appdir}/languages/uzbek.php

%dir %attr(770,root,http) %{_cachedir}
%dir %attr(770,root,http) %{_cachedir}/temp
