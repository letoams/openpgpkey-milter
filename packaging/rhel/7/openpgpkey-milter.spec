Name: openpgpkey-milter
Version: 0.4
Release: 1%{?dist}
BuildArch: noarch
Summary: OPENPGPKEY basd automatic encryption of emails using the milter API
Group: System Environment/Daemons
License: GPLv3+
URL: ftp://ftp.nohats.ca/openpgpkey-milter
Source0: ftp://ftp.nohats.ca/%{name}/%{name}-%{version}.tar.gz
Requires: %{_sbindir}/sendmail python-gnupg unbound-python python-pymilter python-setproctitle

BuildRequires: systemd-units
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
The openpgpkey-milter package provides a milter plugin for sendmail or postfix
that will automatically encrypt plaintext emails if the target recipient is
publishing an OPENPGPKEY record protected with DNSSEC. This is currently an
IETF draft (draft-wouters-dane-openpgp)

%prep
%setup -q

%build

%install
install -p -m 0644 -D packaging/rhel/7/tmpfiles-%{name}.conf %{buildroot}%{_sysconfdir}/tmpfiles.d/%{name}.conf

mkdir -p %{buildroot}%{_localstatedir}/spool/%{name}

install -p -m 755 -D /dev/null %{buildroot}%{_localstatedir}/run/%{name}/%{name}.sock

mkdir -p %{buildroot}%{_sbindir}
install -p -D openpgpkey-milter %{buildroot}%{_sbindir}/openpgpkey-milter

install -p -m 0644 -D packaging/rhel/7/%{name}.service  %{buildroot}%{_unitdir}/%{name}.service

%preun
%systemd_preun openpgpkey-milter.service

%post
%systemd_post openpgpkey-milter.service

%postun
%systemd_postun_with_restart openpgpkey-milter.service 

%files
%doc README LICENSE 
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%{_unitdir}/%{name}.service
%dir %attr(750,root,mail) %{_localstatedir}/run/%{name}
%dir %attr(770,root,mail) %{_localstatedir}/spool/%{name}
%ghost %{_localstatedir}/run/%{name}/%{name}.sock
%attr(755,root,root)%{_sbindir}/openpgpkey-milter

%changelog
* Thu Apr 17 2014 Paul Wouters <pwouters@redhat.com> - 0.4-1
- Updated to 0.4

* Sat Jan 18 2014 Paul Wouters <pwouters@redhat.com> - 0.2-1
- Updated to 0.2, which uses draft-wouters-dane-openpgpkey-02

* Tue Dec 31 2013 Paul Wouters <pwouters@redhat.com> - 0.1-1
- Initial package
