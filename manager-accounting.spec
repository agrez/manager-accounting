%global     debug_package %{nil}
%global     name manager-accounting
%global     inst_dir opt/%{name}
%global     commit_sql f03e65e0f968818b4d03c97a922ac351b1c61714

# We don't want any bundled libs in these directories to generate Provides
%global     __provides_exclude_from %{inst_dir}/.*\\.so
%global     private_libs libe_sqlite3
%global     __requires_exclude ^(%{private_libs})\\.so


Name:       %{name}
Version:    18.7.3
Release:    1%{?dist}
Summary:    Accounting software
Group:      Office/Productivity
License:    Redistributable, no modification permitted
URL:        http://www.manager.io
Source0:    https://mngr.s3.amazonaws.com/%{version}/manager-accounting.zip
Source1:    LICENSE
Source2:    https://raw.githubusercontent.com/ericsink/SQLitePCL.raw/%{commit_sql}/sqlite3/sqlite3.c
Source3:    https://raw.githubusercontent.com/ericsink/SQLitePCL.raw/%{commit_sql}/LICENSE.TXT
Source4:    manager-accounting.appdata.xml
BuildRequires: libappstream-glib
Requires:   mono-core
Requires:   gtk-sharp3
Requires:   webkitgtk4
Provides:   bundled(libe_sqlite3) = 3.22.0

%description
Manager is free accounting software. It features an intuitive
and innovative user interface with modules such as cashbook, invoicing,
receivables, payables, taxes and comprehensive financial reports.


%prep
%setup -c -T
unzip -p %{SOURCE0} %{name}_%{version}.tar.xz |tar xvJ --strip-components=1
cp -a %{SOURCE1} .
cp -a %{SOURCE2} .
cp -a %{SOURCE3} ./LICENSE.SQLitePCL.raw.txt


%build
# Build libe_sqlite3.so
CFLAGS="-shared -fPIC -DNDEBUG -DSQLITE_DEFAULT_FOREIGN_KEYS=1 \
-DSQLITE_ENABLE_FTS3_PARENTHESIS -DSQLITE_ENABLE_FTS4 \
-DSQLITE_ENABLE_COLUMN_METADATA -DSQLITE_ENABLE_JSON1 \
-DSQLITE_ENABLE_RTREE"

%__cc %{optflags} $CFLAGS -o %{inst_dir}/libe_sqlite3.so sqlite3.c

#execute using 'mono' instead of 'cli'
sed -i 's/cli/mono/' %{inst_dir}/%{name}


%install
rm -rf %{buildroot}

%{__install} -d %{buildroot}/%{inst_dir}
mv -f %{inst_dir}/*.html .
%{__install} -p %{inst_dir}/* %{buildroot}/%{inst_dir}

%{__install} -d %{buildroot}/%{_bindir}
ln -sf /%{inst_dir}/%{name} %{buildroot}/%{_bindir}/%{name}

%{__install} -d %{buildroot}/%{_datadir}/applications
%{__install} -p -m0644 usr/share/applications/*.desktop %{buildroot}/%{_datadir}/applications/

%{__install} -d %{buildroot}/%{_datadir}/appdata
%{__install} -p -m0644 %{SOURCE4} %{buildroot}/%{_datadir}/appdata/
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/*.appdata.xml

%{__install} -d %{buildroot}/%{_datadir}/icons
cp -r usr/share/icons/* %{buildroot}/%{_datadir}/icons/


%files
%defattr(-,root,root,-)
%license LICENSE LICENSE.SQLitePCL.raw.txt
%doc Support.html Users.html
%{_bindir}/%{name}
%{_datadir}/applications/*
%{_datadir}/appdata/*
%{_datadir}/icons/*
%dir /%{inst_dir}
%attr(0755,root,root) /%{inst_dir}/%name
%attr(0755,root,root) /%{inst_dir}/*.exe
/%{inst_dir}/*.dll
/%{inst_dir}/*.ttf
/%{inst_dir}/*.so
/%{inst_dir}/*.json
/%{inst_dir}/*.ico


%changelog
* Wed Jul 04 2018 Vaughan <devel at agrez dot net> - 18.7.3-1
- Update to latest release
- Update spec

* Fri Apr 06 2018 Vaughan <devel at agrez dot net> - 18.4.1-1
- Update to latest release
- Update libe_sqlite3 to 3.22.0
- Remove %%post scripts (no longer required in Fedora releases >= 26)

* Wed Jan 31 2018 Vaughan <devel at agrez dot net> - 18.1.39-1
- Update to latest release

* Thu Dec 21 2017 Vaughan <devel at agrez dot net> - 17.12.34-1
- Update to latest release
- Add initial .appdata.xml file

* Sat Nov 25 2017 Vaughan <devel at agrez dot net> - 17.11.29-1
- Update to latest release

* Sat Aug 12 2017 Vaughan <devel at agrez dot net> - 17.7.80-1
- Update to new release
- Don't use version.txt file to get latest version number
  (seems its not necessarily the latest)
- Modify SOURCE0 url
- Use %%__cc rpm macro instead

* Sat Aug 12 2017 Vaughan <devel at agrez dot net> - 17.7.67-1
- Update to new release
- Use cpp rpm macro to build sqlite
- Obtain version number automatically
- Fix unzipping of source (main file is now .xz)

* Thu Jul 13 2017 Vaughan <devel at agrez dot net> - 17.7.8-1
- New release 17.7.8
- Package Guides.json

* Thu Jun 29 2017 Vaughan <devel at agrez dot net> - 17.6.62-1
- New release 17.6.62
- Update Sources2 name
- Drop BuildArch resitrictions
- Build libe_sqlite3.so using %%optflags
- Update %%install & %%files
- Add Provides bundled(libe_sqlite3)

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
