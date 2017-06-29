%global     debug_package %{nil}
%define     name manager-accounting
%define     _install_dir opt/%{name}

# We don't want any bundled libs in these directories to generate Provides
%global __provides_exclude_from %{_install_dir}/.*\\.so
%global private_libs libe_sqlite3
%global __requires_exclude ^(%{private_libs})\\.so

Name:       %{name}
Version:    17.6.52
Release:    2%{?dist}
Summary:    Accounting software
Group:      Office/Productivity
License:    Redistributable, no modification permitted
URL:        http://www.manager.io
BuildArch:  x86_64 armv7hl
Source0:    https://mngr.s3.amazonaws.com/manager-accounting.zip
Source1:    LICENSE
Source2:    SQLitePCL.raw-3.18.2-git41f2c4e.tar.gz
Requires:   mono-core mono-web gtk-sharp2 webkitgtk webkit-sharp


%description
Manager is free accounting software. It features an intuitive
and innovative user interface with modules such as cashbook, invoicing,
receivables, payables, taxes and comprehensive financial reports.


%prep
%setup -c -T -a 2
unzip -p %{SOURCE0} %{name}_%{version}.tar.gz |tar xvz --strip-components=1
cp -a %{SOURCE1} .


%build
# Build libe_sqlite3.so
%ifarch x86_64
gcc -m64 \
%endif
%ifarch armv7hl
gcc \
%endif
-shared -fPIC -O -DNDEBUG -DSQLITE_DEFAULT_FOREIGN_KEYS=1 \
-DSQLITE_ENABLE_FTS3_PARENTHESIS -DSQLITE_ENABLE_FTS4 \
-DSQLITE_ENABLE_COLUMN_METADATA -DSQLITE_ENABLE_JSON1 \
-DSQLITE_ENABLE_RTREE -o %{_install_dir}/libe_sqlite3.so \
SQLitePCL.raw/sqlite3/sqlite3.c

#execute using 'mono' instead of 'cli'
sed -i 's/cli/mono/' %{_install_dir}/%{name}


%install
rm -rf %{buildroot}

%{__install} -d %{buildroot}/%{_install_dir}
%{__install} -p -m0755 %{_install_dir}/%{name} %{buildroot}/%{_install_dir}
%{__install} -p -m0755 %{_install_dir}/*.exe %{buildroot}/%{_install_dir}
%{__install} -p -m0644 %{_install_dir}/*.dll %{buildroot}/%{_install_dir}
%{__install} -p -m0644 %{_install_dir}/*.ttf %{buildroot}/%{_install_dir}
%{__install} -p -m0644 %{_install_dir}/*.so %{buildroot}/%{_install_dir}


%{__install} -d %{buildroot}/%{_bindir}
ln -sf /%{_install_dir}/%{name} %{buildroot}/%{_bindir}/%{name}

%{__install} -d %{buildroot}/%{_datadir}/applications
%{__install} -p -m0644 usr/share/applications/*.desktop %{buildroot}/%{_datadir}/applications/

%{__install} -d %{buildroot}/%{_datadir}/icons
cp -r usr/share/icons/* %{buildroot}/%{_datadir}/icons/


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%clean
rm -rf %{buildroot}
rm -rf %{_builddir}/%{name}*


%files
%defattr(-,root,root,-)
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/*
/%{_install_dir}/*


%changelog
* Mon Jun 26 2017 Vaughan <devel at agrez dot net> - 17.6.52-2
- Build libe_sqlite3.so from source
- Exclude libe_sqlite3.so from Requires & Provides
- Fix build for armv7hl

* Mon Jun 26 2017 Vaughan <devel at agrez dot net> - 17.6.52-1
- Update to 17.6.52 release
- Update Source0 url
- Package missing libe_sqlite3.so library (Source2)
- Package is now x86_64 due to Source2
- Package missing fonts
- Add %%post scripts for updating gtk icon cache
- Disable debug package

* Sun Feb 14 2016 Vaughan <devel at agrez dot net> - 16.2.17-1
- Update to 16.2.17 release
- Add license file

* Tue Oct 20 2015 Vaughan <devel at agrez dot net> - 15.6.1-1
- Update to 15.6.1 release

* Wed Dec 24 2014 Vaughan <devel at agrez dot net> - 14.12.42-1
- Update to 14.12.42 release

* Thu Dec 04 2014 Vaughan <devel at agrez dot net> - 14.12.10-1
- Update to 14.12.10 release

* Wed Nov 05 2014 Vaughan <devel at agrez dot net> - 14.11.7-1
- Update to 14.11.7 release

* Fri Oct 31 2014 Vaughan <devel at agrez dot net> - 14.10.23-1
- Update to 14.10.23 release

* Tue Oct 28 2014 Vaughan <devel at agrez dot net> - 14.10.18-1
- Initial rpm for Fedora
