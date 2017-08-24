%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           pymailq
Version:        0.6.0
Release:        1%{?dist}
Summary:        Simple Postfix queue management

Group:          Development/Languages
License:        GPVLv2
URL:            https://github.com/outini/pymailq/
Source0:        https://github.com/outini/pymailq/archive/v%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel

%description


%prep
%setup -q


%build
# Remove CFLAGS=... for noarch packages (unneeded)
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc
%{python_sitelib}/*
/usr/bin/pqshell
/usr/share/doc/pymailq/LICENSE
/usr/share/doc/pymailq/README.rst
/usr/share/doc/pymailq/CHANGES
/usr/share/doc/pymailq/examples/pymailq.ini
/usr/share/man/man1/pqshell.1.gz


%changelog
* Thu Aug 24 2017 Denis Pompilio <denis.pompilio@gmail.com> - 0.7.0-1
- Support of configuration file
* Thu Aug 24 2017 Denis Pompilio <denis.pompilio@gmail.com> - 0.6.0-2
- Added CHANGES file and examples to package
* Wed Aug 16 2017 Denis Pompilio <denis.pompilio@gmail.com> - 0.6.0-1
- Pqshell now have usage and options
- Pqshell can now show pymailq package version
- Pqshell can now be started in debug mode
- Improved shell completion with suggests and modifiers
- Implementation of the "mails by date" selector
- Reworked postsuper commands handling
- Better pep8 support
- Unit testing for python2.7 and python3
- Using code coverage
* Mon Oct 27 2014 Nils Ratusznik <nils.github@anotherhomepage.org> - 0.5.3-2
- Automated version update for Source0
- renamed pyqueue.spec to pymailq.spec
- corrected errors in files packaging
- corrected errors and warnings displayed by rpmlint
* Sun Oct 19 2014 Denis Pompilio <denis.pompilio@gmail.com> - 0.5.3-1
- 0.5.3 update
* Thu May 08 2014 Denis Pompilio <denis.pompilio@gmail.com> - 0.5.2-1
- 0.5.2 update
* Fri May 02 2014 Nils Ratusznik <nils.github@anotherhomepage.org> - 0.4-1
- Initial package
