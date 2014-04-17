Name: openpgpkey-milter
Version: 0.4
Release: 1%{?dist}
Summary: OPENPGPKEY basd automatic encryption of emails using the milter API
Group: System Environment/Daemons
License: GPLv3+
BuildArch:noarch
URL: ftp://ftp.nohats.ca/openpgpkey-milter
Source0: ftp://ftp.nohats.ca/%{name}/%{name}-%{version}.tar.gz
Requires: %{_sbindir}/sendmail python-gnupg unbound-python python-pymilter python-setproctitle

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
mkdir -p %{buildroot}%{_localstatedir}/spool/%{name} %{buildroot}%{_localstatedir}/run/%{name}

mkdir -p %{buildroot}%{_sbindir}
install -p -m 0755 -D %{name} %{buildroot}%{_sbindir}/%{name}

install -p -m 0755 -D packaging/rhel/6/%{name}.init %{buildroot}%{_initrddir}/%{name}

%files
%doc README LICENSE 
%dir %attr(750,root,mail) %{_localstatedir}/run/%{name}
%dir %attr(770,root,mail) %{_localstatedir}/spool/%{name}
%attr(0755,root,root) %{_initrddir}/%{name}
%attr(0755,root,root) %{_sbindir}/%{name}

%post
/sbin/chkconfig --add %{name}

%preun
if [ $1 -eq 0 ]; then
  /sbin/service %{name} stop > /dev/null 2>&1
  /sbin/chkconfig --del %{name}
fi

%postun
if [ $1 -ge 1 ]; then
  /sbin/service %{name} condrestart 2>&1 >/dev/null
fi

%changelog
* Thu Apr 17 2014 Paul Wouters <pwouters@redhat.com> - 0.4-1
- Updated to 0.4

* Tue Dec 31 2013 Paul Wouters <pwouters@redhat.com> - 0.1-1
- Initial package
