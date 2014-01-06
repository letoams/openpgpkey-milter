Name: openpgpkey-milter
Version: 0.1
Release: 1%{?dist}
Summary: OPENPGPKEY basd automatic encryption of emails using the milter API
Group: System Environment/Daemons
License: GPLv2+
URL: ftp://ftp.nohats.ca/openpgpkey-milter
Source0: ftp://ftp.nohats.ca/%{name}/%{name}-%{version}.tar.gz
Source1: tmpfiles-openpgk-milter.conf
Source2: %{name}.service
Requires: %{_sbindir}/sendmail python-gnupg unbound-python python-pymilter

Requires (post): chkconfig
Requires (preun): chkconfig, initscripts
Requires (postun): initscripts

%description
The openpgpkey-milter package provides a milter plugin for sendmail or postfix
that will automatically encrypt plaintext emails if the target recipient is
publishing an OPENPGPKEY record protected with DNSSEC. This is currently an
IETF draft (draft-wouters-dane-openpgp)

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}%{_sysconfdir}/tmpfiles.d/
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/tmpfiles.d/

mkdir -p %{buildroot}%{_localstatedir}/spool/%{name}

install -p -m 755 -D /dev/null %{buildroot}%{_localstatedir}/run/%{name}/%{name}.sock

mkdir -p %{buildroot}%{_sbindir}
install -p -a -D openpgpkey-milter %{buildroot}%{_sbindir}

install -p -m 0755 -D packaging/rhel/6/openpgpkey-milter.init %{_initrddir}/openpgpkey-milter

%files
%doc README LICENSE 
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/tmpfiles.d/%{name}.conf
%dir %attr(750,root,mail) %{_localstatedir}/run/%{name}
%dir %attr(770,root,mail) %{_localstatedir}lib/${name}
%dir %attr(770,root,mail) %{_localstatedir}/spool/%{name}
%attr(0755,root,root) %{_initrddir}/openpgpkey-milter
%ghost %{_localstatedir}/run/%{name}/%{name}.sock
%{_sbindir}/openpgpkey-milter

%post
/sbin/chkconfig --add openpgpkey-milter

%preun
if [ $1 -eq 0 ]; then
  /sbin/service openpgpkey-milter stop > /dev/null 2>&1
  /sbin/chkconfig --del openpgpkey-milter
fi

%postun
if [ $1 -ge 1 ]; then
  /sbin/service openpgpkey-milter condrestart 2>&1 >/dev/null
fi

%changelog
* Tue Dec 31 2013 Paul Wouters <pwouters@redhat.com> - 0.1-1
- Initial package
