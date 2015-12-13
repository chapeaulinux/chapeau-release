%define release_name Indurain
%define dist_version 22
%define bug_version 22

Summary:        Chapeau release files
Name:           chapeau-release
Version:        22
Release:        2
License:        GPLv2
Group:          System Environment/Base
URL:            http://chapeaulinux.org
Source:         %{name}-%{version}.tar.bz2
Obsoletes:      redhat-release
Obsoletes:      generic-release
Obsoletes:      fedora-release-rawhide < 20-0.5
Obsoletes:      generic-release-rawhide
Obsoletes:      fedora-release
Obsoletes:      fedora-release-cloud
Obsoletes:      fedora-release-server
Obsoletes:      fedora-release-nonproduct
Obsoletes:      fedora-release-workstation

Provides:       redhat-release
Provides:       system-release
Provides:       system-release(%{version})
Provides:       system-release-workstation
Provides:       system-release-workstation(%{version})
Provides:       system-release-product

Requires:       fedora-repos(%{version})
Requires:       chapeau-repos
# needed for captive portal support
Requires:       NetworkManager-config-connectivity-fedora
Requires(post): /usr/bin/glib-compile-schemas
Requires(postun): /usr/bin/glib-compile-schemas

BuildArch:       noarch


%description
Chapeau release files that define the release.

%prep
%setup -q
sed -i 's|@@VERSION@@|%{dist_version}|g' Fedora-Legal-README.txt

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc
echo "Chapeau release %{version} (%{release_name})" > $RPM_BUILD_ROOT/etc/fedora-release
echo "cpe:/o:Chapeau:chapeau:%{version}" > $RPM_BUILD_ROOT/etc/system-release-cpe
cp -p $RPM_BUILD_ROOT/etc/fedora-release $RPM_BUILD_ROOT/etc/issue
echo "Kernel \r on an \m (\l)" >> $RPM_BUILD_ROOT/etc/issue
cp -p $RPM_BUILD_ROOT/etc/issue $RPM_BUILD_ROOT/etc/issue.net
echo >> $RPM_BUILD_ROOT/etc/issue
ln -s fedora-release $RPM_BUILD_ROOT/etc/redhat-release
ln -s fedora-release $RPM_BUILD_ROOT/etc/system-release

cat << EOF >>$RPM_BUILD_ROOT/etc/os-release
NAME=Chapeau
VERSION="%{dist_version} (%{release_name})"
ID=chapeau
VERSION_ID=%{dist_version}
PRETTY_NAME="Chapeau %{dist_version} (%{release_name})"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:Chapeau:chapeau:%{dist_version}"
HOME_URL="http://chapeaulinux.org/"
BUG_REPORT_URL="https://bugzilla.redhat.com/"
REDHAT_BUGZILLA_PRODUCT="Fedora"
REDHAT_BUGZILLA_PRODUCT_VERSION=%{bug_version}
REDHAT_SUPPORT_PRODUCT="Fedora"
REDHAT_SUPPORT_PRODUCT_VERSION=%{bug_version}
EOF

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cat >> $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%fedora                %{dist_version}
%%dist                .fc%{dist_version}
%%fc%{dist_version}                1
EOF

# Override the list of enabled gnome-shell extensions for Workstation
#mkdir -p %{buildroot}%{_datadir}/glib-2.0/schemas/
#install -m 0644 org.gnome.shell.gschema.override %{buildroot}%{_datadir}/glib-2.0/schemas/

%post
sed -i 's|Wayand|Wayland|g' %{_sysconfdir}/gdm/custom.conf

%postun
if [ $1 -eq 0 ] ; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :
fi

%posttrans
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE Fedora-Legal-README.txt
%config %attr(0644,root,root) /etc/os-release
%config %attr(0644,root,root) /etc/fedora-release
/etc/redhat-release
/etc/system-release
%config %attr(0644,root,root) /etc/system-release-cpe
%config(noreplace) %attr(0644,root,root) /etc/issue
%config(noreplace) %attr(0644,root,root) /etc/issue.net
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist

%{!?_licensedir:%global license %%doc}
%license LICENSE
#%{_datadir}/glib-2.0/schemas/org.gnome.shell.gschema.override


%changelog
* Sun Dec 13 2015 Vince Pooley <vince@chapeaulinux.org> - 22.2
- Insert post scriptlet to fix Wayland typo in /etc/gdm/custom.conf

* Sun Mar 08 2015 Vince Pooley <vince@chapeaulinux.org> - 22
- Updated for Chapeau 22

* Sat Jan 03 2015 Vince Pooley <vince@chapeaulinux.org> - 21
- Updated for Chapeau 21 from Fedora 21 workstation release
- package 'fedora-release'

* Tue Jan 14 2014 Vince Pooley <vince@chapeaulinux.org> - 20
- First chapeau-release rpm
- A bit overdue, prior to this Chapeau's release details were
- overwriting the Fedora files in the live image until
- I got more familiar with packaging.

