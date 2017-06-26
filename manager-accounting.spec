%define     name manager-accounting
%define     _install_dir opt/%{name}

Name:       %{name}       
Version:    16.2.17
Release:    1%{?dist}
Summary:    Accounting software
Group:      Office/Productivity
License:    Redistributable, no modification permitted
URL:        http://www.manager.io
BuildArch:  noarch
Source0:    http://download.manager.io/manager-accounting.zip
Source1:    LICENSE
Requires:   mono-core mono-web gtk-sharp2 webkitgtk webkit-sharp


%description
Manager is free accounting software. It features an intuitive
and innovative user interface with modules such as cashbook, invoicing,
receivables, payables, taxes and comprehensive financial reports.


%prep
%setup -c -T
unzip -p %{SOURCE0} %{name}_%{version}.tar.gz |tar xvz --strip-components=1
cp -a %{SOURCE1} .


%build
#execute using 'mono' instead of 'cli'
sed -i 's/cli/mono/' %{_install_dir}/%{name}


%install
rm -rf %{buildroot}

%{__install} -d %{buildroot}/%{_install_dir}
%{__install} -p -m0755 %{_install_dir}/%{name} %{buildroot}/%{_install_dir}
%{__install} -p -m0755 %{_install_dir}/*.exe %{buildroot}/%{_install_dir}
%{__install} -p -m0644 %{_install_dir}/*.dll %{buildroot}/%{_install_dir}

%{__install} -d %{buildroot}/%{_bindir}
ln -sf /%{_install_dir}/%{name} %{buildroot}/%{_bindir}/%{name}

%{__install} -d %{buildroot}/%{_datadir}/applications
%{__install} -p -m0644 usr/share/applications/*.desktop %{buildroot}/%{_datadir}/applications/

%{__install} -d %{buildroot}/%{_datadir}/icons
cp -r usr/share/icons/* %{buildroot}/%{_datadir}/icons/


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
