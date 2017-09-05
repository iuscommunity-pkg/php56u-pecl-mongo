%global pecl_name mongo
%global php_base php56u
# After 40-json
%global ini_name    50-%{pecl_name}.ini
%global with_zts 0%{?__ztsphp:1}

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{php_ztsextdir}/.*\.so$}
%{?filter_setup}


Summary:      PHP MongoDB database driver
Name:         %{php_base}-pecl-mongo
Version:      1.6.16
Release:      1.ius%{?dist}
License:      ASL 2.0
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{pecl_name}
Source0:      http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source1:      %{pecl_name}.ini
BuildRequires: %{php_base}-devel
BuildRequires: %{php_base}-pear
BuildRequires: cyrus-sasl-devel
BuildRequires: openssl-devel

Requires(post): %{php_base}-pear
Requires(postun): %{php_base}-pear

Requires:     %{php_base}(zend-abi) = %{php_zend_api}
Requires:     %{php_base}(api) = %{php_core_api}

# provide the stock name
Provides:     php-pecl-%{pecl_name} = %{version}
Provides:     php-pecl-%{pecl_name}%{?_isa} = %{version}

# provide the stock and IUS names without pecl
Provides:     php-%{pecl_name} = %{version}
Provides:     php-%{pecl_name}%{?_isa} = %{version}
Provides:     %{php_base}-%{pecl_name} = %{version}
Provides:     %{php_base}-%{pecl_name}%{?_isa} = %{version}

# provide the stock and IUS names in pecl() format
Provides:     php-pecl(%{pecl_name}) = %{version}
Provides:     php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:     %{php_base}-pecl(%{pecl_name}) = %{version}
Provides:     %{php_base}-pecl(%{pecl_name})%{?_isa} = %{version}

# conflict with the stock name
Conflicts:    php-pecl-%{pecl_name} < %{version}


%description
This package provides an interface for communicating with the MongoDB database
in PHP.


%prep
%setup -c -q
mv %{pecl_name}-%{version} NTS

%if %{with_zts}
cp -pr NTS ZTS
%endif


%build
pushd NTS
%{_bindir}/phpize
%configure  \
  --with-mongo-sasl \
  --with-php-config=%{_bindir}/php-config
%{__make} %{?_smp_mflags}
popd

%if %{with_zts}
pushd ZTS
%{_bindir}/zts-phpize
%configure  \
  --with-mongo-sasl \
  --with-php-config=%{_bindir}/zts-php-config
%{__make} %{?_smp_mflags}
popd
%endif


%install
%{__make} -C NTS install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
%{__install} -Dm0644 %{SOURCE1} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
%{__install} -Dm0644 package.xml %{buildroot}%{pecl_xmldir}/%{pecl_name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
%{__install} -Dm0644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do %{__install} -Dpm0644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%post
%{pecl_install} %{pecl_xmldir}/%{pecl_name}.xml >/dev/null || :


%postun
if [ "$1" -eq "0" ]; then
   %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%check
: Minimal load test for NTS extension
%{__php} -n \
    -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    -i | grep "MongoDB Support => enabled"

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} -n \
    -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    -i | grep "MongoDB Support => enabled"
%endif


%files
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{pecl_name}.xml
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so
%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Tue Sep 05 2017 Ben Harper <ben.harper@rackspace.com> - 1.6.16-1.ius
- Latest upstream

* Thu Jun 16 2016 Ben Harper <ben.harper@rackspace.com> - 1.6.14-2.ius
- update filters to include zts

* Wed Apr 27 2016 Ben Harper <ben.harper@rackspace.com> - 1.6.14-1.ius
- Latest upstream

* Tue Mar 22 2016 Carl George <carl.george@rackspace.com> - 1.6.13-1.ius
- Latest upstream

* Tue Mar 15 2016 Carl George <carl.george@rackspace.com> - 1.6.12-2.ius
- Clean up provides
- ZTS clean up
- Install package.xml as %%{pecl_name}.xml, not %%{name}.xml

* Mon Nov 30 2015 Ben Harper <ben.harper@rackspace.com> - 1.6.12-1.ius
- Latest upstream

* Wed Aug 26 2015 Carl George <carl.george@rackspace.com> - 1.6.11-1.ius
- Latest upstream

* Tue Jul 07 2015 Ben Harper <ben.harper@rackspace.com> - 1.6.10-1.ius
- Latest upstream

* Wed Jun 10 2015 Carl George <carl.george@rackspace.com> - 1.6.9-1.ius
- Latest upstream

* Thu May 14 2015 Ben Harper <ben.harper@rackspace.com> - 1.6.8-1.ius
- Latest upstream

* Wed Apr 29 2015 Carl George <carl.george@rackspace.com> - 1.6.7-1.ius
- Latest upstream

* Mon Mar 30 2015 Carl George <carl.george@rackspace.com> - 1.6.6-1.ius
- Latest upstream

* Tue Mar 17 2015 Carl George <carl.george@rackspace.com> - 1.6.5-1.ius
- Latest upstream
- Add build dependency on openssl-devel

* Tue Mar 10 2015 Ben Harper <ben.harper@rackspace.com> - 1.6.3-2.ius
- Rebuilding against php56u-5.6.6-2.ius as it is now using bundled PCRE.

* Mon Mar 02 2015 Ben Harper <ben.harper@rackspace.com> - 1.6.3-1.ius
- Latest upstream

* Wed Feb 11 2015 Carl George <carl.george@rackspace.com> - 1.6.2-1.ius
- Latest upstream

* Thu Feb 05 2015 Ben Harper <ben.harper@rackspace.com> - 1.6.1-1.ius
- Latest sources from upstream

* Mon Feb 02 2015 Ben Harper <ben.harper@rackspace.com> - 1.6.0-2.ius
- porting from php55u-pecl-mongo

* Thu Jan 29 2015 Ben Harper <ben.harper@rackspace.com> - 1.6.0-1.ius
- Latest sources from upstream

* Tue Nov 11 2014 Ben Harper <ben.harper@rackspace.com> - 1.5.8-1.ius
- Latest sources from upstream

* Fri Oct 10 2014 Carl George <carl.george@rackspace.com> - 1.5.7-2.ius
- Add numerical prefix to extension configuration file
- Enable SASL support
- Install doc in pecl doc_dir
- Build ZTS extension
- Conflict with stock package
- Use same provides as stock package
- Directly require the correct pear package, not /usr/bin/pecl

* Tue Sep 16 2014 Carl George <carl.george@rackspace.com> - 1.5.7-1.ius
- Latest sources from upstream
- Move config from a here doc to separate source file

* Thu Jul 31 2014 Carl George <carl.george@rackspace.com> - 1.5.5-1.ius
- Latest sources from upstream

* Wed Jun 18 2014 Carl George <carl.george@rackspace.com> - 1.5.4-1.ius
- Latest sources from upstream

* Fri Jun 06 2014 Ben Harper <ben.harper@rackspace.com> - 1.5.3-1.ius
- Latest sources from upstream

* Wed May 07 2014 Carl George <carl.george@rackspace.com> - 1.5.2-1.ius
- Latest sources from upstream

* Mon Apr 07 2014 Ben Harper <ben.harper@rackspace.com> - 1.5.1-1.ius
- Latest sources from upstream

* Fri Apr 04 2014 Ben Harper <ben.harper@rackspace.com> - 1.5.0-1.ius
- Latest sources from upstream

* Fri Jan 24 2014 Ben Harper <ben.harper@rackspace.com> - 1.4.5-1
- porting from php54-pecl-mongo and updating to latest release

* Wed Nov 06 2013 Ben Harper <ben.harper@rackspace.com> - 1.3.2-2
- adding provides per LP bug 1248285

* Mon Dec 31 2012 Ben Harper <ben.harper@rackspace.com> - 1.3.2-1
- porting from EPEL
- upsteam 1.3.2 

* Sat Jul 28 2012 Christof Damian <christof@damian.net> - 1.2.12-1
- upstream 1.2.12

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May  9 2012 Christof Damian <christof@damian.net> - 1.2.10-1
- upstream 1.2.10

* Sat Mar  3 2012 Christof Damian <christof@damian.net> - 1.2.9-1
- upstream 1.2.9

* Thu Jan 19 2012 Remi Collet <remi@fedoraproject.org> - 1.2.7-1
- update to 1.2.7 for php 5.4
- fix filters

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 17 2011 Christof Damian <christof@damian.net> - 1.2.1-1
- upstream 1.2.1

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 25 2010 Christof Damian <christof@damian.net> - 1.0.10-4
- added link to option docs

* Sat Oct 23 2010 Christof Damian <christof@damian.net> - 1.0.10-3
- fix post
- add example config with sensible defaults
- add conditionals for EPEL + fix for check

* Fri Oct 22 2010 Christof Damian <christof@damian.net> - 1.0.10-2
- fixes for package review: requires and warnings

* Wed Oct 20 2010 Christof Damian <christof@damian.net> - 1.0.10-1
- Initial RPM
