#
# Authors: Szilárd Pfeiffer <szilard.pfeiffer@balabit.com>
#          Tibor Balázs <tibor.balazs@balabit.com>
#
# Permission is granted to copy, distribute and/or modify this document
# under the terms of the GNU Free Documentation License, Version 1.3
# or any later version published by the Free Software Foundation;
# with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
# A copy of the license is included in the section entitled "GNU
# Free Documentation License".
#
############################################################################

from Zorp.Core import *
from Zorp.Proxy import *

from Zorp.Smtp import *
from Zorp.Pop3 import *

from zones import *

class SmtpProxyOneSideSsl(SmtpProxy):
    def config(self):
        SmtpProxy.config(self)
        self.relay_zones=("*",)
        self.ssl.server_connection_security=SSL_FORCE_SSL
        self.ssl.server_verify_type=SSL_VERIFY_OPTIONAL_UNTRUSTED

def zorp_instance():
    Service(name="service_smtp_transparent_one_sided_ssl",
        proxy_class=SmtpProxyOneSideSsl,
        router=DirectedRouter(dest_addr=(SockAddrInet('172.16.20.254', 465),))
    )

    Rule(service='service_smtp_transparent_one_sided_ssl',
         dst_port=25,
         src_zone=('clients'),
         dst_zone=('servers.smtp_one_sided_ssl')
    )
