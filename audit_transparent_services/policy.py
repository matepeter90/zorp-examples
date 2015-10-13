##
## Authors: Szilárd Pfeiffer <szilard.pfeiffer@balabit.com>
##          Tibor Balázs <tibor.balazs@balabit.com>
##
## Permission is granted to copy, distribute and/or modify this document
## under the terms of the GNU Free Documentation License, Version 1.3
## or any later version published by the Free Software Foundation;
## with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
## A copy of the license is included in the section entitled "GNU
## Free Documentation License".
##
#############################################################################

from Zorp.Core import *

from Zorp.Ftp import *
from Zorp.Http import *
from Zorp.Pop3 import *
from Zorp.Smtp import *

from zones import *

def audit_instance():
    Service(name="service_ftp_transparent_audit",
        proxy_class=FtpProxy,
        router=TransparentRouter()
    )
    Service(name="service_http_transparent_audit",
        proxy_class=HttpProxy,
        router=TransparentRouter()
    )
    Service(name="service_pop3_transparent_audit",
        proxy_class=Pop3Proxy,
        router=TransparentRouter()
    )
    Service(name="service_smtp_transparent_audit",
        proxy_class=SmtpProxy,
        router=TransparentRouter()
    )

    Rule(service='service_ftp_transparent_audit',
         dst_port=21,
         src_zone=('clients', ),
         dst_zone=('servers.audit', )
    )
    Rule(service='service_http_transparent_audit',
         dst_port=80,
         src_zone=('clients', ),
         dst_zone=('servers.audit', )
    )
    Rule(service='service_pop3_transparent_audit',
         dst_port=110,
         src_zone=('clients', ),
         dst_zone=('servers.audit', )
    )
    Rule(service='service_smtp_transparent_audit',
         dst_port=25,
         src_zone=('clients', ),
         dst_zone=('servers.audit', )
    )
