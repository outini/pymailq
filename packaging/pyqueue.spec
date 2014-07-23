# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name:           pyqueue
Version:        0.5.2
Release:        1%{?dist}
Summary:        Simple Postfix queue management

Group:          Development/Languages
License:        GPVLv2
URL:            https://github.com/outini/pyqueue/
Source0:        https://github.com/outini/pyqueue/archive/v0.5.2.tar.gz
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
# For noarch packages: sitelib
%{python_sitelib}/*


%changelog
* Thu May 08 2014 Denis Pompilio <denis.pompilio@gmail.com> - 0.5.2-1
* Fri May 02 2014 Nils Ratusznik <nils.github@anotherhomepage.org> - 0.4-1
- Initial package
