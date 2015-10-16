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

from Zorp.Ftp import *


Zone(name="clients",
     addr = ["172.16.10.0/23", ],
    )

Zone(name="servers",
     addr = ["172.16.20.0/23", ],
    )

class FtpProxyNonTransparent(FtpProxy):
    def config(self):
        FtpProxy.config(self)
        self.transparent_mode = FALSE

def zorp_instance():
    Service(name="service_ftp_nontransparent_inband",
            proxy_class = FtpProxyNonTransparent,
            router = InbandRouter(forge_port=TRUE)
    )

    Rule(service='service_ftp_nontransparent_inband',
         dst_port = 50021,
         dst_subnet = ('172.16.10.254', ),
         src_zone = ('clients', )
    )
