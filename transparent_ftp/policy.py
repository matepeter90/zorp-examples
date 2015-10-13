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

from zones import *

def zorp_instance():
    #ftp services
    Service(name="service_ftp_transparent",
            proxy_class=FtpProxyRO,
            router=TransparentRouter()
    )

    Rule(service='service_ftp_transparent',
         dst_port=21,
         src_zone=('clients', ),
         dst_zone=('servers', )
    )
