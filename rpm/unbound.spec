%define _unpackaged_files_terminate_build 0
%{?!with_python2:     %global with_python2     0}
%{?!with_python3:     %global with_python3     1}
%{?!with_munin:       %global with_munin       1}
%bcond_without dnstap
%bcond_with    systemd
%bcond_without doh

%global _hardened_build 1

#%%global extra_version rc1

%if 0%{with_python2}
%global python_primary %{__python2}
%endif

%if 0%{with_python3}
%global python_primary %{__python3}
%endif

%if 0%{?rhel}
%global with_munin   0

%if 0%{?rhel} <= 7
%global with_python3 0
%else
%global with_python2 0
%endif
%endif

Summary: Validating, recursive, and caching DNS(SEC) resolver
Name: unbound
Version: 1.14.0
Release: 1%{?extra_version:.%{extra_version}}%{?dist}
License: BSD
Url: https://nlnetlabs.nl/projects/unbound/
Source: https://nlnetlabs.nl/downloads/%{name}/%{name}-%{version}%{?extra_version}.tar.gz
Source1: unbound.service
Source2: unbound.conf
Source3: unbound.munin
Source4: unbound_munin_
Source5: root.key
Source7: unbound-keygen.service
Source8: tmpfiles-unbound.conf
Source9: example.com.key
Source10: example.com.conf
Source11: block-example.com.conf
Source12: https://data.iana.org/root-anchors/icannbundle.pem
Source13: root.anchor
Source14: unbound.sysconfig
Source15: unbound-anchor.timer
Source16: unbound-munin.README
Source17: unbound-anchor.service
Source18: https://nlnetlabs.nl/downloads/%{name}/%{name}-%{version}%{?extra_version}.tar.gz.asc
# source: https://nlnetlabs.nl/people/
Source19: https://keys.openpgp.org/pks/lookup?op=get&search=0x9F6F1C2D7E045F8D#/wouter.nlnetlabs.nl.key


BuildRequires: gcc, make
BuildRequires: flex, openssl-devel
BuildRequires: libevent-devel expat-devel
BuildRequires: pkgconfig
%if 0%{?fedora}
BuildRequires: gnupg2
%endif
%if 0%{with_python2}
BuildRequires: python2-devel swig
%endif
%if 0%{with_python3}
BuildRequires: python3-devel swig
%endif
%if %{with dnstap}
BuildRequires: fstrm-devel protobuf-c-devel
%endif
%if %{with systemd}
BuildRequires: systemd-devel
%endif
%if %{with doh}
BuildRequires: libnghttp2-devel
%endif
%if 0%{?fedora} >= 30
BuildRequires: systemd-rpm-macros
%else
BuildRequires: systemd
%endif
# Required for SVN versions
# BuildRequires: bison
# BuildRequires: automake autoconf libtool

# Needed because /usr/sbin/unbound links unbound libs staticly
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
Unbound is a validating, recursive, and caching DNS(SEC) resolver.

The C implementation of Unbound is developed and maintained by NLnet
Labs. It is based on ideas and algorithms taken from a java prototype
developed by Verisign labs, Nominet, Kirei and ep.net.

Unbound is designed as a set of modular components, so that also
DNSSEC (secure DNS) validation and stub-resolvers (that do not run
as a server, but are linked into an application) are easily possible.

%if %{with_munin}
%package munin
Summary: Plugin for the munin / munin-node monitoring package
Requires: munin-node
Requires: %{name} = %{version}-%{release}, bc
BuildArch: noarch

%description munin
Plugin for the munin / munin-node monitoring package
%endif

%package devel
Summary: Development package that includes the unbound header files
Requires: %{name}-libs%{?_isa} = %{version}-%{release}, openssl-devel
Requires: pkgconfig

%description devel
The devel package contains the unbound library and the include files

%package libs
Summary: Libraries used by the unbound server and client applications
Requires(pre): shadow-utils
%if ! 0%{with_python2}
# Make explicit conflict with no longer provided python package
Obsoletes: python2-unbound < 1.9.3
%endif

%description libs
Contains libraries used by the unbound server and client applications

%if 0%{with_python2}
%package -n python2-unbound
%{?python_provide:%python_provide python2-unbound}
Summary: Python 2 modules and extensions for unbound
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Provides: unbound-python = %{version}-%{release}
Obsoletes: unbound-python < %{version}-%{release}

%description -n python2-unbound
Python 2 modules and extensions for unbound
%endif

%if 0%{with_python3}
%package -n python3-unbound
Summary: Python 3 modules and extensions for unbound
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%if ! 0%{with_python2}
# Make explicit conflict with no longer provided python package
Conflicts: python2-unbound < 1.9.3
%endif

%description -n python3-unbound
Python 3 modules and extensions for unbound
%endif


%prep
%if 0%{?fedora}
%gpgverify -k 19 -s 18 -d 0
%endif
%global pkgname %{name}-%{version}%{?extra_version}

%if 0%{with_python2} && 0%{with_python3}
%global dir_primary %{pkgname}_python3
%global python_primary %{__python3}
%global dir_secondary %{pkgname}_python2
%global python_secondary %{__python2}
%else
%global dir_primary %{pkgname}
%endif

%autosetup -c -N -n %{pkgname}

pushd %{pkgname}
# patches go here
%autopatch -p1

# only for snapshots
# autoreconf -iv

# copy common doc files - after here, since it may be patched
cp -pr doc pythonmod libunbound ../
popd

%if 0%{with_python2} && 0%{with_python3}
mv %{pkgname} %{dir_primary}
cp -a %{dir_primary} %{dir_secondary}
%endif

%build
# This is needed to rebuild the configure script to support Python 3.x
# autoreconf -iv

# ./configure script common arguments
%global configure_args --with-libevent --with-pthreads --with-ssl \\\
            --disable-rpath --disable-static \\\
            --enable-relro-now --enable-pie \\\
            --enable-subnet --enable-ipsecmod \\\
            --with-conf-file=%{_sysconfdir}/%{name}/unbound.conf \\\
            --with-pidfile=%{_rundir}/%{name}/%{name}.pid \\\
            --enable-sha2 --disable-gost --enable-ecdsa \\\
            --with-rootkey-file=%{_sharedstatedir}/unbound/root.key \\\
            --enable-linux-ip-local-port-range

pushd %{dir_primary}

%configure  \
%if 0%{?python_primary:1}
            --with-pythonmodule --with-pyunbound PYTHON=%{python_primary} \
%endif
%if %{with dnstap}
            --enable-dnstap \
%endif
%if %{with systemd}
            --enable-systemd \
%endif
%if %{with doh}
            --with-libnghttp2 \
%endif
            %{configure_args}

%make_build
%make_build streamtcp

popd

%if 0%{?python_secondary:1}
pushd %{dir_secondary}
%configure  \
            --with-pythonmodule --with-pyunbound PYTHON=%{python_secondary} \
%if %{with dnstap}
            --enable-dnstap \
%endif
%if %{with systemd}
            --enable-systemd \
%endif
            %{configure_args}

%make_build
popd
%endif


%install
install -p -m 0644 %{SOURCE16} .

%if 0%{?python_secondary:1}
# install first secondary build. It will be overwritten by primary
pushd %{dir_secondary}
%make_install unbound-event-install
popd
%endif

pushd %{dir_primary}
%make_install unbound-event-install
install -m 0755 streamtcp %{buildroot}%{_sbindir}/unbound-streamtcp
popd

install -d -m 0755 %{buildroot}%{_unitdir} %{buildroot}%{_sysconfdir}/sysconfig
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/unbound.service
install -p -m 0644 %{SOURCE7} %{buildroot}%{_unitdir}/unbound-keygen.service
install -p -m 0644 %{SOURCE15} %{buildroot}%{_unitdir}/unbound-anchor.timer
install -p -m 0644 %{SOURCE17} %{buildroot}%{_unitdir}/unbound-anchor.service
install -p -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/unbound
install -p -m 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/unbound
install -p -m 0644 %{SOURCE14} %{buildroot}%{_sysconfdir}/sysconfig/unbound
%if %{with_munin}
# Install munin plugin and its softlinks
install -d -m 0755 %{buildroot}%{_sysconfdir}/munin/plugin-conf.d
install -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/munin/plugin-conf.d/unbound
install -d -m 0755 %{buildroot}%{_datadir}/munin/plugins/
install -p -m 0755 %{SOURCE4} %{buildroot}%{_datadir}/munin/plugins/unbound
for plugin in unbound_munin_hits unbound_munin_queue unbound_munin_memory unbound_munin_by_type unbound_munin_by_class unbound_munin_by_opcode unbound_munin_by_rcode unbound_munin_by_flags unbound_munin_histogram; do
    ln -s unbound %{buildroot}%{_datadir}/munin/plugins/$plugin
done
%endif

pushd %{dir_primary}
# install streamtcp man page
install -m 0644 testcode/streamtcp.1 %{buildroot}/%{_mandir}/man1/unbound-streamtcp.1
install -D -m 0644 contrib/libunbound.pc %{buildroot}/%{_libdir}/pkgconfig/libunbound.pc
popd

# Install tmpfiles.d config
install -d -m 0755 %{buildroot}%{_tmpfilesdir} %{buildroot}%{_sharedstatedir}/unbound
install -m 0644 %{SOURCE8} %{buildroot}%{_tmpfilesdir}/unbound.conf

# install root - we keep a copy of the root key in old location,
# in case user has changed the configuration and we wouldn't update it there
install -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/unbound/
install -m 0644 %{SOURCE13} %{buildroot}%{_sharedstatedir}/unbound/root.key

# remove static library from install (fedora packaging guidelines)
rm %{buildroot}%{_libdir}/*.la


%if 0%{with_python2}
rm %{buildroot}%{python2_sitearch}/*.la
%endif

%if 0%{with_python3}
rm %{buildroot}%{python3_sitearch}/*.la
%endif

# create softlink for all functions of libunbound man pages
for mpage in ub_ctx ub_result ub_ctx_create ub_ctx_delete ub_ctx_set_option ub_ctx_get_option ub_ctx_config ub_ctx_set_fwd ub_ctx_resolvconf ub_ctx_hosts ub_ctx_add_ta ub_ctx_add_ta_file ub_ctx_trustedkeys ub_ctx_debugout ub_ctx_debuglevel ub_ctx_async ub_poll ub_wait ub_fd ub_process ub_resolve ub_resolve_async ub_cancel ub_resolve_free ub_strerror ub_ctx_print_local_zones ub_ctx_zone_add ub_ctx_zone_remove ub_ctx_data_add ub_ctx_data_remove;
do
  echo ".so man3/libunbound.3" > %{buildroot}%{_mandir}/man3/$mpage ;
done

mkdir -p %{buildroot}%{_localstatedir}/run/unbound

# Install directories for easier config file drop in

mkdir -p %{buildroot}%{_sysconfdir}/unbound/{keys.d,conf.d,local.d}
install -p %{SOURCE9} %{buildroot}%{_sysconfdir}/unbound/keys.d/
install -p %{SOURCE10} %{buildroot}%{_sysconfdir}/unbound/conf.d/
install -p %{SOURCE11} %{buildroot}%{_sysconfdir}/unbound/local.d/

# Link unbound-control-setup.8 manpage to unbound-control.8
echo ".so man8/unbound-control.8" > %{buildroot}/%{_mandir}/man8/unbound-control-setup.8


%pre libs
getent group unbound >/dev/null || groupadd -r unbound
getent passwd unbound >/dev/null || \
useradd -r -g unbound -d %{_sysconfdir}/unbound -s /sbin/nologin \
-c "Unbound DNS resolver" unbound

%post
%systemd_post unbound.service
%systemd_post unbound-keygen.service

%post libs
%{?ldconfig}
%systemd_post unbound-anchor.timer
# start the timer only if installing the package to prevent starting it, if it was stopped on purpose
if [ "$1" -eq 1 ]; then
    # the Unit is in presets, but would be started after reboot
    /bin/systemctl start unbound-anchor.timer >/dev/null 2>&1 || :
fi

%preun
%systemd_preun unbound.service
%systemd_preun unbound-keygen.service

%preun libs
%systemd_preun unbound-anchor.timer

%postun
%systemd_postun_with_restart unbound.service
%systemd_postun unbound-keygen.service

%postun libs
%{?ldconfig}
%systemd_postun_with_restart unbound-anchor.timer

%check
pushd %{dir_primary}
#pushd pythonmod
#make test
#popd

make check

popd

%if 0%{?python_secondary:1}
pushd %{dir_secondary}
#pushd pythonmod
#make test
#popd
make check
popd
%endif


%files
%doc doc/CREDITS doc/FEATURES
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-keygen.service
%attr(0755,unbound,unbound) %dir %{_localstatedir}/run/%{name}
%attr(0644,root,root) %{_tmpfilesdir}/unbound.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/unbound.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%dir %attr(0755,root,unbound) %{_sysconfdir}/%{name}/keys.d
%attr(0644,root,unbound) %config(noreplace) %{_sysconfdir}/%{name}/keys.d/*.key
%dir %attr(0755,root,unbound) %{_sysconfdir}/%{name}/conf.d
%attr(0644,root,unbound) %config(noreplace) %{_sysconfdir}/%{name}/conf.d/*.conf
%dir %attr(0755,root,unbound) %{_sysconfdir}/%{name}/local.d
%attr(0644,root,unbound) %config(noreplace) %{_sysconfdir}/%{name}/local.d/*.conf
%ghost %attr(0640,root,unbound) %{_sysconfdir}/%{name}/unbound_control.pem
%ghost %attr(0640,root,unbound) %{_sysconfdir}/%{name}/unbound_control.key
%ghost %attr(0640,root,unbound) %{_sysconfdir}/%{name}/unbound_server.pem
%ghost %attr(0640,root,unbound) %{_sysconfdir}/%{name}/unbound_server.key
%{_sbindir}/unbound
%{_sbindir}/unbound-checkconf
%{_sbindir}/unbound-control
%{_sbindir}/unbound-control-setup
%{_sbindir}/unbound-host
%{_sbindir}/unbound-streamtcp
%{_mandir}/man1/*
%{_mandir}/man5/*
%exclude %{_mandir}/man8/unbound-anchor*
%{_mandir}/man8/*

%if 0%{with_python2}
%files -n python2-unbound
%license pythonmod/LICENSE
%{python2_sitearch}/*
%doc libunbound/python/examples/*
%doc pythonmod/examples/*
%endif

%if 0%{with_python3}
%files -n python3-unbound
%license pythonmod/LICENSE
%{python3_sitearch}/*
%doc libunbound/python/examples/*
%doc pythonmod/examples/*
%endif

%if 0%{with_munin}
%files munin
%doc unbound-munin.README
%config(noreplace) %{_sysconfdir}/munin/plugin-conf.d/unbound
%{_datadir}/munin/plugins/unbound*
%endif

%files devel
%{_libdir}/libunbound.so
%{_includedir}/unbound.h
%{_includedir}/unbound-event.h
%{_mandir}/man3/*
%{_libdir}/pkgconfig/*.pc

%files libs
%doc doc/README
%license doc/LICENSE
%attr(0755,root,root) %dir %{_sysconfdir}/%{name}
%{_sbindir}/unbound-anchor
%{_libdir}/libunbound.so.*
%{_mandir}/man8/unbound-anchor*
%{_sysconfdir}/%{name}/icannbundle.pem
%{_unitdir}/unbound-anchor.timer
%{_unitdir}/unbound-anchor.service
%dir %attr(0755,unbound,unbound) %{_sharedstatedir}/%{name}
%attr(0644,unbound,unbound) %config %{_sharedstatedir}/%{name}/root.key
# just left for backwards compat with user changed unbound.conf files - format is different!
%attr(0644,root,root) %config %{_sysconfdir}/%{name}/root.key

%changelog
* Thu Dec 21 2021 Zero <zero@441.surf> - 1.14.0-1
- Respin for EL7

* Thu Aug 12 2021 Paul Wouters <paul.wouters@aiven.io> - 1.13.2-1
- Resolves: rhbz#1992985 unbound-1.13.2 is available
- Use system-wide crypto policies

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 1.13.1-7
- Rebuilt for Python 3.10

* Fri Apr 23 2021 Artem Egorenkov <aegorenk@redhat.com> - 1.13.1-6
- Option --enable-linux-ip-local-port-range added to use system configured port range for libunbound on Linux
- Resolves: rhbz#1935101

* Tue Apr 13 2021 Paul Wouters <pwouters@redhat.com> - 1.13.1-5
- Fix unbound.service to use After=network-online.target

* Tue Apr 06 2021 Artem Egorenkov <aegorenk@redhat.com> - 1.13.1-4
- Don't start unbound-anchor before unbound service if DISABLE_UNBOUND_ANCHOR
  environment variable equals to "yes"

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.13.1-3
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Mon Feb 15 2021 Victor Stinner <vstinner@python.org> - 1.13.1-2
- Fix build on Python 3.10 (rhbz#1889726).

* Wed Feb 10 2021 Paul Wouters <pwouters@redhat.com> - 1.13.1-1
- Resolves rhbz#1860887 unbound-1.13.1 is available
- Fixup unbound.conf

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 10 2020 Petr Menšík <pemensik@redhat.com> - 1.13.0-1
- Update to 1.13.0

* Tue Oct 13 2020 Petr Menšík <pemensik@redhat.com> - 1.12.0-1
- Update to 1.12.0 (#1860887)

* Tue Sep 15 2020 Petr Menšík <pemensik@redhat.com> - 1.10.1-5
- Move command line tools to utils subpackage

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 1.10.1-3
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 1.10.1-2
- Rebuilt for Python 3.9

* Tue May 19 2020 Paul Wouters <pwouters@redhat.com> - 1.10.1-1
- Resolves: rhbz#1837279 unbound-1.10.1 is available
- Resolves: rhbz#1837598 CVE-2020-12662 unbound: insufficient control of network message volume leads to DoS
- Resolves: rhbz#1837609 CVE-2020-12663 unbound: infinite loop via malformed DNS answers received from upstream servers
- Updated unbound.conf for new options in 1.10.1

* Wed Apr 29 2020 Paul Wouters <pwouters@redhat.com> - 1.10.0-3
- Resolves: rhbz#1667742 SELinux is preventing unbound from 'name_bind' accesses on the udp_socket port 61000.

* Thu Apr 16 2020 Artem Egorenkov <aegorenk@redhat.com> - 1.10.0-2
- Resolves: rhbz#1824536 unbound crash

* Thu Mar 19 2020 Petr Menšík <pemensik@redhat.com> - 1.10.0-1
- Update to 1.10.0 (#1805199)

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 13 2019 Paul Wouters <pwouters@redhat.com> - 1.9.6-1
- Resolves: rhbz#1758107 unbound-1.9.5 is available
- Resolves: CVE-2019-18934

* Fri Nov 01 2019 Paul Wouters <pwouters@redhat.com> - 1.9.4-1
- Fix build on rhel/centos systems
- Resolves: rhbz#1767955 (CVE-2019-16866) uninitialized memory accesses leads to crash via a crafted NOTIFY query

* Thu Sep 26 2019 Petr Menšík <pihhan@gmail.com> - 1.9.3-2
- Obsolete no longer provided python2 subpackage (#1749400)

* Tue Aug 27 2019 Paul Wouters <pwouters@redhat.com> - 1.9.3-1
- Updated to 1.9.3
- Resolves: rhbz#1672578 unbound-1.9.2 is available
- Resolves: rhbz#1694831 [/usr/lib/tmpfiles.d/unbound.conf:1] Line references path below legacy directory /var/run/
- Resolves: rhbz# 1667387 [abrt] unbound: memmove(): unbound killed by SIGABRT

* Thu Aug 22 2019 Miro Hrončok <mhroncok@redhat.com> - 1.8.3-8
- Subpackage python2-unbound has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 1.8.3-7
- Rebuilt for Python 3.8

* Mon Aug  5 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.8.3-6
- Drop install-time requirements on systemd (#1723777)

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Paul Wouters <pwouters@redhat.com> - 1.8.3-3
- Remove KSK-2010 from configs - it has been revoked

* Wed Dec 12 2018 Paul Wouters <pwouters@redhat.com> - 1.8.3-2
- Another dns64 fixup

* Wed Dec 12 2018 Paul Wouters <pwouters@redhat.com> - 1.8.3-1
- Updated to 1.8.3 with fixes the dns64 bug and has some other minor fixes

* Mon Dec 10 2018 Paul Wouters <pwouters@redhat.com> - 1.8.2-2
- Fix dns64 allocation in wrong region for returned internal queries.

* Tue Dec 04 2018 Paul Wouters <pwouters@redhat.com> - 1.8.2-1
- Updated to 1.8.2.
- Enabled deny ANY query support and edns-tcp-keepalive
- Set serve-stale timeout to 4h
- Updated unbound.conf for latest options

* Mon Oct 22 2018 Petr Menšík <pemensik@redhat.com> - 1.8.1-2
- Allow group by default to unbound-control (#1640259)

* Mon Oct 08 2018 Petr Menšík <pemensik@redhat.com> - 1.8.1-1
- Update to 1.8.1

* Mon Oct 01 2018 Petr Menšík <pemensik@redhat.com> - 1.8.0-2
- Skip ipv6 forwarders without ipv6 support (#1633874)

* Wed Sep 19 2018 Petr Menšík <pemensik@redhat.com> - 1.8.0-1
- Rebase to 1.8.0

* Tue Aug 14 2018 Paul Wouters <pwouters@redhat.com> - 1.7.3-9
- Fix for restarting unbound service after deleting key/pem files for remote control

* Tue Jul 31 2018 Petr Menšík <pemensik@redhat.com> - 1.7.3-8
- Release memory in unbound-host

* Mon Jul 23 2018 Petr Menšík <pemensik@redhat.com> - 1.7.3-7
- Remove unused Group tag

* Wed Jul 18 2018 Petr Menšík <pemensik@redhat.com> - 1.7.3-6
- Cleanup generated client and server keys (#1601773)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Petr Menšík <pemensik@redhat.com> - 1.7.3-4
- Do not call ldconfig if possible

* Wed Jul 04 2018 Petr Menšík <pemensik@redhat.com> - 1.7.3-3
- Update trust anchors also behind firewall (#1598078)

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1.7.3-2
- Rebuilt for Python 3.7

* Wed Jun 27 2018 Petr Menšík <pemensik@redhat.com> - 1.7.3-1
- Update to 1.7.3 (#1593708)

* Wed Jun 27 2018 Petr Menšík <pemensik@redhat.com> - 1.7.2-3
- Remove last python2 dependency from python3 build

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.7.2-2
- Rebuilt for Python 3.7

* Mon Jun 11 2018 Paul Wouters <pwouters@redhat.com> - 1.7.2-1
- Resolves rhbz#1589807 unbound-1.7.2 is available
- Add patch to fix stub/forward zone not returning ServFail when TTL expires
- Enabled the new root-key-sentinel option

* Wed May 30 2018 Petr Menšík <pemensik@redhat.com> - 1.7.1-1
- Update to 1.7.1 (#1574495)

* Mon Apr 09 2018 Petr Menšík <pemensik@redhat.com> - 1.7.0-5
- Require gcc and make on build
- Remove group, simplify systemd requires
- Simplify building with single python version, make python3 primary

* Mon Apr 09 2018 Paul Wouters <pwouters@redhat.com> - 1.7.0-4
- Patch for prefetching after flushing cache

* Fri Apr 06 2018 Paul Wouters <pwouters@redhat.com> - 1.7.0-3
- Patch for referral with auth-zone: response


* Wed Mar 21 2018 Paul Wouters <pwouters@redhat.com> - 1.7.0-2
- Patch for broken Aggressive NSEC + stub-zone configuration causing NXDOMAIN at TTL expiry

* Thu Mar 15 2018 Paul Wouters <pwouters@redhat.com> - 1.7.0-1
- Updated to 1.7.0 (aggressive nsec, local root support, bugfixes)

* Thu Feb 22 2018 Petr Menšík <pemensik@redhat.com> - 1.6.8-6
- Uncomment again original max-upd-size

* Wed Feb 21 2018 Petr Menšík <pemensik@redhat.com> - 1.6.8-5
- Use default RPM build flags and configure parameters (#1539097)

* Wed Feb 21 2018 Petr Menšík <pemensik@redhat.com> - 1.6.8-4
- Remove group writable bit from some config files (#1528445)

* Wed Feb 14 2018 Filipe Rosset <rosset.filipe@gmail.com> - 1.6.8-3
- rebuilt due new libevent 2.1.8

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.6.8-2
- Escape macros in %%changelog

* Mon Jan 22 2018 Paul Wouters <pwouters@redhat.com> - 1.6.8-1
- Resolves rhbz#1483572 unbound-1.6.8 is available
- Resolves rhbz#1507049 CVE-2017-15105 unbound: Improper validation of wildcard synthesized NSEC records
- Resolves rhbz#1536518 CVE-2017-15105 unbound: Improper validation of wildcard synthesized NSEC records [fedora-all]

* Sun Dec 17 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.6.7-2
- Python 2 binary package renamed to python2-unbound
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Oct 12 2017 Paul Wouters <pwouters@redhat.com> - 1.6.7-1
- Updated to 1.6.7 (minor bugfixes)

* Tue Oct 03 2017 Petr Menšík <pemensik@redhat.com> - 1.6.6-3
- Update icannbundle.pem

* Mon Oct 02 2017 Paul Wouters <pwouters@redhat.com> - 1.6.6-2
- Enable RFC 8145 Trust Anchor Signaling to help the root zone get keytag statistics

* Fri Sep 22 2017 Paul Wouters <pwouters@redhat.com> - 1.6.6-1
- Resolves: rhbz#1483572 unbound-1.6.6 is available
- Resolves: rhbz#1465575 unbound fails to start up, complains about missing ipsecmod-hook (edit) 

* Wed Aug 16 2017 Paul Wouters <pwouters@redhat.com> - 1.6.4-4
- Rebuilt with KSK2017 added to root.key and root.anchor
- Remove noreplace for root key files. We can only improve these files over local copies

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 02 2017 Paul Wouters <pwouters@redhat.com> - 1.6.4-1
- Updated to 1.6.4 full release, patch to allow missing ipsechook
- Resolves rhbz#1465575 unbound fails to start up, complains about missing ipsecmod-hook

* Thu Jun 22 2017 Paul Wouters <pwouters@redhat.com> - 1.6.4-0.rc2
- Update to 1.6.4 (esubnet, ipsecmod support, bugfixes)

* Tue Jun 13 2017 Paul Wouters <pwouters@redhat.com> - 1.6.3-1
- Updated to 1.6.3 (fixes assertion failure when receiving malformed packet with 0x20 enabled)

* Thu Jun 08 2017 Paul Wouters <pwouters@redhat.com> - 1.6.2-2
- Patch for cmd: unbound-control set_option val-permissive-mode: yes

* Wed Apr 26 2017 Paul Wouters <pwouters@redhat.com> - 1.6.2-1
- Update to 1.6.2 (rhbz#1425649)
- Updated unbound.conf with new options

* Wed Mar 22 2017 Paul Wouters <pwouters@redhat.com> - 1.6.0-6
- Call make unbound-event-install to install unbound-event.h

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 18 2017 Paul Wouters <pwouters@redhat.com> - 1.6.0-4
- Remove obsoleted DLV key

* Mon Jan 02 2017 Paul Wouters <pwouters@redhat.com> - 1.6.0-3
- Actually remove dependency because minimum is always satisfied

* Mon Jan 02 2017 Paul Wouters <pwouters@redhat.com> - 1.6.0-2
- Depend on openssl-libs, not opensl

* Wed Dec 21 2016 Kevin Fenzi <kevin@scrye.com> - 1.6.0-1
- Update to 1.6.0

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.5.10-3
- Rebuild for Python 3.6

* Wed Oct 26 2016 Ilya Evseev <evseev.i@cdnnow.ru> - 1.5.10-2
- Bugfix building without python2 and python3
- Fixup streamtcp build (Paul)

* Tue Sep 27 2016 Paul Wouters <pwouters@redhat.com> - 1.5.10-1
- Updated to 1.5.10 (better TCP handling, bugfixes)
- Install pkgconfig file in -devel package
- Updated unbound.conf

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.9-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jul 07 2016 Paul Wouters <pwouters@redhat.com> - 1.5.9-3
- Fix upper port range to 60999 because that's what selinux allows

* Thu Jun 16 2016 Paul Wouters <pwouters@redhat.com> - 1.5.9-2
- Patch for allowing more queries before failure (needed for query minimalization)

* Mon Jun 13 2016 Paul Wouters <pwouters@redhat.com> - 1.5.9-1
- Updated to 1.5.9

* Thu Apr 21 2016 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5.8-2
- Fix streamtcp to link against libpython3.x instead of libpython2.x

* Wed Mar 02 2016 Paul Wouters <pwouters@redhat.com> - 1.5.8-1
- Update to 1.5.8 (rhbz#1313831) which incorporates rhbz#1294339 patch
- Updated unbound.conf with new upstream options
- Enabled ip-transparent: yes (see rhbz#1291449)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Tomas Hozza <thozza@redhat.com> - 1.5.7-2
- Fix escaping of shell chars in unbound-control-setup (#1294339)

* Fri Dec 11 2015 Paul Wouters <pwouters@redhat.com> - 1.5.7-1
- Update to 1.5.7
- Enable query minimalization for enhanced DNS query privacy
- Enable nxdomain hardening to assist with query minimalization and SBLs
- Updated default unbound.conf for new features from upstream.

* Fri Nov 13 2015 Tomas Hozza <thozza@redhat.com> - 1.5.6-1
- Update to 1.5.6 (#1176729)

* Wed Nov 04 2015 Robert Kuska <rkuska@redhat.com> - 1.5.5-2
- Rebuilt for Python3.5 rebuild

* Wed Oct 07 2015 Tomas Hozza <thozza@redhat.com> - 1.5.5-1
- New upstream release 1.5.5 (#1269137)
- Removed the anchor update from %%post section of -libs subpackage (#1269137#c2)

* Tue Sep 15 2015 Tomas Hozza <thozza@redhat.com> - 1.5.4-5
- Removed dependency and ordering on unbound-anchor.service in unbound.service

* Thu Sep 03 2015 Tomas Hozza <thozza@redhat.com> - 1.5.4-4
- Prefer Python3 build over Python2 build for now (#1254566)

* Mon Jul 20 2015 Tomas Hozza <thozza@redhat.com> - 1.5.4-3
- Added ExecReload section to unbound.service (#1195785)
- Removed After syslog.target since it is not needed any more

* Thu Jul 16 2015 Tomas Hozza <thozza@redhat.com> - 1.5.4-2
- Start unbound-anchor.timer only on new installations
- Rename root.anchor to root.key in %%post section

* Tue Jul 14 2015 Paul Wouters <pwouters@redhat.com> - 1.5.4-1
- Update to 1.5.4
- Removed patches merged into upstream

* Tue Jun 16 2015 Tomas Hozza <thozza@redhat.com> - 1.5.3-8
- Revert: Use low maximum negative cache TTL (5 sec) (#1229596)

* Mon Jun 15 2015 Tomas Hozza <thozza@redhat.com> - 1.5.3-7
- Add option for maximum negative cache TTL (#1229599)
- Use low maximum negative cache TTL (5 sec) (#1229596)

* Tue May 26 2015 Tomas Hozza <thozza@redhat.com> - 1.5.3-6
- Removed usage of DLV from the default configuration (#1223363)

* Wed May 13 2015 Tomas Hozza <thozza@redhat.com> - 1.5.3-5
- unbound.service now Wants unbound-anchor.timer
- unbound-anchor man page moved to the unbound-libs

* Mon May 11 2015 Paul Wouters <pwouters@redhat.com> - 1.5.3-4
- Fixup scriptlets causing systemctl: command not found
- Resolves rhbz#1219587 Error in PREIN scriptlet in rpm package unbound-libs

* Mon Apr 27 2015 Tomas Hozza <thozza@redhat.com> - 1.5.3-3
- migrate cronjob to systemd timer unit (#1177285)
- change the period for unbound-anchor from monthly to daily (#1180267)
- Thanks to Tomasz Torcz <ttorcz@fedoraproject.org> for the initial patch

* Thu Apr 16 2015 Tomas Hozza <thozza@redhat.com> - 1.5.3-2
- Fix FTBFS (#1206129)
- Build python3-unbound and python-unbound bindings for Python 3 and 2 (#1188080)

* Mon Mar 16 2015 Paul Wouters <pwouters@redhat.com> - 1.5.3-1
- Updated to 1.5.3 which is a bugfix on 1.5.2 for sighup handling
- Updated to 1.5.2 which fixes DNSSEC validation with different
  trust anchors upstream, local-zone has a new keyword 'inform'

* Mon Feb 02 2015 Paul Wouters <pwouters@redhat.com> - 1.5.1-4
- Build with --enable-ecdsa

* Sun Feb 01 2015 Paul Wouters <pwouters@redhat.com> - 1.5.1-3
- Fix post to create root.anchor, not root.key, to match cron job

* Tue Dec 09 2014 Paul Wouters <pwouters@redhat.com> - 1.5.1-2
- Change systemd-units to systemd
- Use _tmpfilesdir macro, don't mark tmpfiles as config

* Tue Dec 09 2014 Paul Wouters <pwouters@redhat.com> - 1.5.1-1
- Update to 1.5.1 for CVE-2014-8602 (rhbz#1172066)
- Removed unbound-aarch64.patch which was merged upstream
- Don't require autotools for non snapshots or run autoreconf

* Fri Nov 28 2014 Tomas Hozza <thozza@redhat.com> - 1.5.1-0.1.rc1
- update to 1.5.1rc1

* Fri Nov 28 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.5.0-3
- fix build on aarch64

* Wed Nov 26 2014 Tomas Hozza <thozza@redhat.com> - 1.5.0-2
- Fix race condition in arc4random (#1166878)

* Wed Nov 19 2014 Tomas Hozza <thozza@redhat.com> - 1.5.0-1
- update to 1.5.0

* Wed Sep 24 2014 Pavel Šimerda <psimerda@redhat.com> - 1.4.22-6
- Resolves: #1115489 - build with python 3.x for fedora >= 22

* Thu Aug 21 2014 Kevin Fenzi <kevin@scrye.com> - 1.4.22-5
- Rebuild for rpm bug 1131960

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 01 2014 Paul Wouters <pwouters@redhat.com> - 1.4.22-2
- Added flushcache patch (SVN commit 3125)

* Thu Mar 13 2014 Paul Wouters <pwouters@redhat.com> - 1.4.22-1
- Updated to 1.4.22
- No longer requires the ldns library

* Thu Jan 16 2014 Tomas Hozza <thozza@redhat.com> - 1.4.21-3
- Fix segfault on adding insecure forward zone when using only iterator (#1054192)

* Mon Oct 21 2013 Tomas Hozza <thozza@redhat.com> - 1.4.21-2
- run test suite during the build

* Thu Sep 19 2013 Paul Wouters <pwouters@redhat.com> - 1.4.21-1
- Updated to 1.4.21, 
- Enabled new max-udp-size: 3072 (so ANY isc.org won't fit)
- Removed patched merged in by upstream
- Enable statistics-cumulative for munin-plugin
- Added outgoing-port-avoid: 0-32767 conformant to SElinux restrictions
- Updated unbound.conf

* Mon Aug 26 2013 Tomas Hozza <thozza@redhat.com> - 1.4.20-19
- Fix errors found by static analysis of source

* Mon Aug 12 2013 Paul Wouters <pwouters@redhat.com> - 1.4.20-18
- Change unbound.conf to only use ephemeral ports (32768-65535)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.20-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Tomas Hozza <thozza@redhat.com> - 1.4.20-16
- provide man page for unbound-streamtcp

* Mon Jul 08 2013 Paul Wouters <pwouters@redhat.com> - 1.4.20-15
- Re-introduce hardening flags for full relro and pie
- Fixes compilation failure for python module

* Wed Jul 03 2013 Tomas Hozza <thozza@redhat.com> - 1.4.20-14
- remove missing unbound-rootkey.service from post/preun/postun sections
- don't hardcode hardening flags, let hardened build macro handles it

* Sat Jun 01 2013 Paul Wouters <pwouters@redhat.com> - 1.4.20-13
- Run unbound-anchor as user unbound in unbound.service

* Tue May 28 2013 Paul Wouters <pwouters@redhat.com> - 1.4.20-12
- Enable round-robin (with noths() patch)
- Change cron and systemd service to use root.key, not root.anchor

* Sat May 25 2013 Paul Wouters <pwouters@redhat.com> - 1.4.20-10
- Use /var/lib/unbound/root.key (more consistent with other distros)
- Enable minimal responses

* Mon Apr 22 2013 Paul Wouters <pwouters@redhat.com> - 1.4.20-8
- Refix

* Fri Apr 19 2013 Paul Wouters <pwouters@redhat.com> - 1.4.20-7
- Fix runuser call in post.

* Tue Apr 16 2013 Paul Wouters <pwouters@redhat.com> - 1.4.20-6
- /var/lib/unbound should be owned by unbound. group write is not enough

* Fri Apr 12 2013 Paul Wouters <pwouters@redhat.com> - 1.4.20-5
- Fix cron job syntax (rhbz#951725)
- Use install -p to prevent .rpmnew files that are identical to originals

* Mon Apr 8 2013 Paul Wouters <pwouters@redhat.com> - 1.4.20-4
- Updated to 1.4.20
- Build with full RELRO (not use -z,relro but with -z,relo,-z,now)
- Fixup man page for unbound-control-setup
- unbound.service should start before nss-lookup.target (rhbz#919955)
- Removed patch for rhbz#888759 merged in upstream
- Move root.anchor to /var/lib/unbound to make selinux policy easier for updating (rhbz#896599/rhbz#891008)
- Move cronjob for root.anchor from unbound to unbound-libs, require crontabs
- /etc/unbound (and all) should be owned by unbound-libs (rhbz#909691)
- Remove Obsolete/Provides for dnssec-conf which was last seen in f13
- Ensure any unbound-anchor failure in post is ignored

* Tue Mar 05 2013 Adam Tkac <atkac redhat com> - 1.4.19-5
- build with full RELRO
- symlink unbound-control-setup.8 manpage to unbound-control.8

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 12 2012 Paul Wouters <pwouters@redhat.com> - 1.4.19-3
- Updated to 1.4.19 - this integrates all existing patches
- Patch for unbound-anchor (rhbz#888759)

* Fri Nov 09 2012 Paul Wouters <pwouters@redhat.com> - 1.4.18-6
- Patch to ensure stube-zone's aren't lost when using dnssec-triggerd
- added unbound-munin.README file

* Wed Sep 26 2012 Paul Wouters <pwouters@redhat.com> - 1.4.18-5
- Patch to allow wildcards in include: statements
- Add directories /etc/unbound/keys.d,conf.d,local.d with
  example entries
- Added /etc/unbound/root.anchor, maintained by unbound-anchor
  which is installed as monthly cron and PreExec in systemd config
  (root.key is unused, but left installed in case people depend on it)
- Native systemd (simple) and /etc/sysconfig/unbound support
- Run unbound-checkconf in PreExec
- Moved trust anchor related files to unbound-libs, as they can
  be used without the daemon.
- sub packages now depends on base package of same arch
- Build munin package as noarch
- unbound-anchor moved to unbound-libs package. It is needed
  to update the root.anchor key file.

* Tue Sep 04 2012 Paul Wouters <pwouters@redhat.com> - 1.4.18-3
- Fix openssl thread locking bug under high query load

* Thu Aug 23 2012 Paul Wouters <pwouters@redhat.com> - 1.4.18-2
- Use new systemd-rpm macros (rhbz#850351)
- Clean up old obsoleted dnssec-conf from < fedora 15

* Fri Aug 03 2012 Paul Wouters <pwouters@redhat.com> - 1.4.18-1
- Updated to 1.4.18 (FIPS related fixes mostly)
- Removed patches that were merged in upstream
- Added comment to root.key

* Mon Jul 23 2012 Paul Wouters <pwouters@redhat.com> - 1.4.17-5
- Fix for unbound crasher (upstream bug #452)
- Support libunbound functions in man pages and place in -devel

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 Paul Wouters <pwouters@redhat.com> - 1.4.17-3
- unbound FIPS patches for MD5,randomness (rhbz#835106)

* Fri Jun 15 2012 Adam Tkac <atkac redhat com> - 1.4.17-2
- don't build unbound-munin on RHEL

* Thu May 24 2012 Paul Wouters <pwouters@redhat.com> - 1.4.17-1
- Updated to 1.4.17 (which mostly brings in patches we already
  applied from svn trunk)

* Wed Feb 29 2012 Paul Wouters <pwouters@redhat.com> - 1.4.16-3 
- Since the daemon links to the libs staticly, add Requires:
  (this is rhbz#745288)
- Package up streamtcp as unbound-streamtcp (for monitoring)

* Mon Feb 27 2012 Paul Wouters <pwouters@redhat.com> - 1.4.16-2
- Don't ghost the directory (rhbz#788805)
- Patch for unbound to support unbound-control forward_zone
  (needed for openswan in XAUTH mode)

* Thu Feb 02 2012 Paul Wouters <paul@nohats.ca> - 1.4.16-1
- Upgraded to 1.4.16, which was relesed due to the soname
  and some DNSSEC validation failures

* Wed Feb 01 2012 Paul Wouters <paul@nohats.ca> - 1.4.15-2
- Patch for SONAME version (libtool's -version-number vs -version-info)

* Fri Jan 27 2012 Paul Wouters <pwouters@redhat.com> - 1.4.15-1
- Upgraded to 1.4.15
- Updated unbound.conf to show how to configure listening on tls443

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Paul Wouters <paul@cypherpunks.ca> - 1.4.14-1
- Upgraded to 1.4.14 for CVE-2011-4528 / VU#209659
- SSL-wrapped query support for dnssec-trigger
- EDNS handling changes
- Removed integrated EDNS patches
- Disabled use-caps-for-id, GoDaddy domains now break on it
- Enabled new harden-below-nxdomain

* Thu Sep 15 2011 Paul Wouters <paul@xelerance.com> - 1.4.13-1
- Upgraded to 1.4.13
- Removed merged in pythonmod patch
- Added EDNS1480 patch to fix unbound on broken EDNS/UDP networks
- Fix python to go into sitearch instead of sitelib

* Wed Sep 14 2011 Tom Callaway <spot@fedoraproject.org> - 1.4.12-4
- convert to systemd, tmpfiles.d

* Mon Aug 08 2011 Paul Wouters <paul@xelerance.com> - 1.4.12-3
- Added pythonmod docs and examples

* Mon Aug 08 2011 Paul Wouters <paul@xelerance.com> - 1.4.12-2
- Fix for python module load in the server (Tom Hendrikx)
- No longer enable --enable-debug as it causes degraded  performance
  under load.

* Mon Jul 18 2011 Paul Wouters <paul@xelerance.com> - 1.4.12-1
- Updated to 1.4.12

* Sun Jul 03 2011 Paul Wouters <paul@xelerance.com> - 1.4.11-1
- Updated to 1.4.11
- removed integrated CVE patch
- updated stock unbound.conf for new options introduced

* Mon Jun 06 2011 Paul Wouters <paul@xelerance.com> - 1.4.10-1
- Added ghost for /var/run/unbound (bz#656710)

* Mon Jun 06 2011 Paul Wouters <paul@xelerance.com> - 1.4.9-3
- rebuilt

* Wed May 25 2011 Paul Wouters <paul@xelerance.com> - 1.4.9-2
- Applied patch for CVE-2011-1922 DoS vulnerability

* Sun Mar 27 2011 Paul Wouters <paul@xelerance.com> - 1.4.9-1
- Updated to 1.4.9

* Sat Feb 12 2011 Paul Wouters <paul@xelerance.com> - 1.4.8-2
- rebuilt

* Tue Jan 25 2011 Paul Wouters <paul@xelerance.com> - 1.4.8-1
- Updated to 1.4.8
- Enable root key for DNSSEC
- Fix unbound-munin to use proper file (could cause excessive logging)
- Build unbound-python per default
- Disable gost as Fedora/EPEL does not allow ECC and has mangled openssl

* Tue Oct 26 2010 Paul Wouters <paul@xelerance.com> - 1.4.5-4
- Revert last build - it was on the wrong branch

* Tue Oct 26 2010 Paul Wouters <paul@xelerance.com> - 1.4.5-3
- Disable do-ipv6 per default - causes severe degradation on non-ipv6 machines
  (see comments in inbound.conf)

* Tue Jun 15 2010 Paul Wouters <paul@xelerance.com> - 1.4.5-2
- Bump release - forgot to upload the new tar ball.

* Tue Jun 15 2010 Paul Wouters <paul@xelerance.com> - 1.4.5-1
- Upgraded to 1.4.5

* Mon May 31 2010 Paul Wouters <paul@xelerance.com> - 1.4.4-2
- Added accidentally omitted svn patches to cvs 

* Mon May 31 2010 Paul Wouters <paul@xelerance.com> - 1.4.4-1
- Upgraded to 1.4.4 with svn patches
- Obsolete dnssec-conf to ensure it is de-installed

* Thu Mar 11 2010 Paul Wouters <paul@xelerance.com> - 1.4.3-1
- Update to 1.4.3 that fixes 64bit crasher

* Tue Mar 09 2010 Paul Wouters <paul@xelerance.com> - 1.4.2-1
- Updated to 1.4.2 
- Updated unbound.conf with new options
- Enabled pre-fetching DNSKEY records (DNSSEC speedup)
- Enabled re-fetching popular records before they expire
- Enabled logging of DNSSEC validation errors

* Mon Mar 01 2010 Paul Wouters <paul@xelerance.com> - 1.4.1-5
- Overriding -D_GNU_SOURCE is no longer needed. This fixes DSO issues
  with pthreads

* Wed Feb 24 2010 Paul Wouters <paul@xelerance.com> - 1.4.1-3
- Change make/configure lines to attempt to fix -lphtread linking issue

* Thu Feb 18 2010 Paul Wouters <paul@xelerance.com> - 1.4.1-2
- Removed dependancy for dnssec-conf
- Added ISC DLV key (formerly in dnssec-conf)
- Fixup old DLV locations in unbound.conf file via %%post
- Fix parent child disagreement handling and no-ipv6 present [svn r1953]

* Tue Jan 05 2010 Paul Wouters <paul@xelerance.com> - 1.4.1-1
- Updated to 1.4.1
- Changed %%define to %%global

* Thu Oct 08 2009 Paul Wouters <paul@xelerance.com> - 1.3.4-2
- Bump version

* Thu Oct 08 2009 Paul Wouters <paul@xelerance.com> - 1.3.4-1
- Upgraded to 1.3.4. Security fix with validating NSEC3 records

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.3.3-2
- rebuilt with new openssl

* Mon Aug 17 2009 Paul Wouters <paul@xelerance.com> - 1.3.3-1
- Updated to 1.3.3

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 20 2009 Paul Wouters <paul@xelerance.com> - 1.3.0-2
- Added missing glob patch to cvs
- Place python macros within the %%with_python check

* Sat Jun 20 2009 Paul Wouters <paul@xelerance.com> - 1.3.0-1
- Updated to 1.3.0
- Added unbound-python sub package. disabled for now
- Patch from svn to fix DLV lookups
- Patches from svn to detect wrong truncated response from BIND 9.6.1 with
  minimal-responses)
- Added Default-Start and Default-Stop to unbound.init
- Re-enabled --enable-sha2
- Re-enabled glob.patch

* Wed May 20 2009 Paul Wouters <paul@xelerance.com> - 1.2.1-7
- unbound-iterator.patch was not commited

* Wed May 20 2009 Paul Wouters <paul@xelerance.com> - 1.2.1-6
- Fix for https://bugzilla.redhat.com/show_bug.cgi?id=499793

* Tue Mar 17 2009 Paul Wouters <paul@xelerance.com> - 1.2.1-5
- Use --nocheck to avoid giving an error on missing unbound-remote certs/keys

* Tue Mar 10 2009 Adam Tkac <atkac redhat com> - 1.2.1-4
- enable DNSSEC only if it is enabled in sysconfig/dnssec

* Mon Mar 09 2009 Adam Tkac <atkac redhat com> - 1.2.1-3
- add DNSSEC support to initscript and enabled it per default
- add requires dnssec-conf

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Paul Wouters <paul@xelerance.com - 1.2.1-1
- updated to 1.2.1

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.0-2
- rebuild with new openssl

* Wed Jan 14 2009 Paul Wouters <paul@xelerance.com - 1.2.0-1
- Updated to 1.2.0
- Added dependancy on minimum SSL for CVE-2008-5077
- Added dependancy on bc for unbound-munin
- Added minimum requirement of libevent 1.4.5. Crashes with older versions
  (note: libevent is stale in EL-4 and not in EL-5, needs fixing there)
- Removed dependancy on selinux-policy (will get used when available)
- Enable options as per draft-wijngaards-dnsext-resolver-side-mitigation-00.txt
- Enable unwanted-reply-threshold to mitigate against a Kaminsky attack
- Enable val-clean-additional to drop addition unsigned data from signed
  response.
- Removed patches (got merged into upstream)

* Mon Jan  5 2009 Paul Wouters <paul@xelerance.com> - 1.1.1-7
- Modified scandir patch to silently fail when wildcard matches nothing
- Patch to allow unbound-checkconf to find empty wildcard matches

* Mon Jan  5 2009 Paul Wouters <paul@xelerance.com> - 1.1.1-6
- Added scandir patch for trusted-keys-file: option, which
  is used to load multiple dnssec keys in bind file format

* Mon Dec  8 2008 Paul Wouters <paul@xelerance.com> - 1.1.1-4
- Added Requires: for selinux-policy >= 3.5.13-33 for proper SElinux rules.

* Mon Dec  1 2008 Paul Wouters <paul@xelerance.com> - 1.1.1-3
- We did not own the /etc/unbound directory (#474020)
- Fixed cvs anomalies

* Fri Nov 28 2008 Adam Tkac <atkac redhat com> - 1.1.1-2
- removed all obsolete chroot related stuff
- label control certs after generation correctly

* Thu Nov 20 2008 Paul Wouters <paul@xelerance.com> - 1.1.1-1
- Updated to unbound 1.1.1 which fixes a crasher and
  addresses nlnetlabs bug #219

* Wed Nov 19 2008 Paul Wouters <paul@xelerance.com> - 1.1.0-3
- Remove the chroot, obsoleted by SElinux
- Add additional munin plugin links supported by unbound plugin
- Move configuration directory from /var/lib/unbound to /etc/unbound
- Modified unbound.init and unbound.conf to account for chroot changes
- Updated unbound.conf with new available options
- Enabled dns-0x20 protection per default

* Wed Nov 19 2008 Adam Tkac <atkac redhat com> - 1.1.0-2
- unbound-1.1.0-log_open.patch
  - make sure log is opened before chroot call
  - tracked as http://www.nlnetlabs.nl/bugs/show_bug.cgi?id=219
- removed /dev/log and /var/run/unbound and /etc/resolv.conf from
  chroot, not needed
- don't mount files in chroot, it causes problems during updates
- fixed typo in default config file

* Fri Nov 14 2008 Paul Wouters <paul@xelerance.com> - 1.1.0-1
- Updated to version 1.1.0
- Updated unbound.conf's statistics options and remote-control
  to work properly for munin
- Added unbound-munin package
- Generate unbound remote-control  key/certs on first startup
- Required ldns is now 1.4.0

* Wed Oct 22 2008 Paul Wouters <paul@xelerance.com> - 1.0.2-5
- Only call ldconfig in -libs package
- Move configure into build section
- devel subpackage should only depend on libs subpackage

* Tue Oct 21 2008 Paul Wouters <paul@xelerance.com> - 1.0.2-4
- Fix CFLAGS getting lost in build
- Don't enable interface-automatic:yes because that
  causes unbound to listen on 0.0.0.0 instead of 127.0.0.1

* Sun Oct 19 2008 Paul Wouters <paul@xelerance.com> - 1.0.2-3
- Split off unbound-libs, make build verbose 

* Thu Oct  9 2008 Paul Wouters <paul@xelerance.com> - 1.0.2-2
- FSB compliance, chroot fixes, initscript fixes

* Thu Sep 11 2008 Paul Wouters <paul@xelerance.com> - 1.0.2-1
- Upgraded to 1.0.2

* Wed Jul 16 2008 Paul Wouters <paul@xelerance.com> - 1.0.1-1
- upgraded to new release

* Wed May 21 2008 Paul Wouters <paul@xelerance.com> - 1.0.0-2
- Build against ldns-1.3.0

* Wed May 21 2008 Paul Wouters <paul@xelerance.com> - 1.0.0-1
- Split of -devel package, fixed dependancies, make rpmlint happy

* Fri Apr 25 2008 Wouter Wijngaards <wouter@nlnetlabs.nl> - 0.12
- Using parts from ports collection entry by Jaap Akkerhuis.
- Using Fedoraproject wiki guidelines.

* Wed Apr 23 2008 Wouter Wijngaards <wouter@nlnetlabs.nl> - 0.11
- Initial version.
