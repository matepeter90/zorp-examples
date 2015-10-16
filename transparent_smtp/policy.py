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


Zone(name="clients",
     addr = ["172.16.10.0/23", ],
    )

Zone(name="servers",
     addr = ["172.16.20.0/23", ],
    )

def zorp_instance():
    #smtp services
    Service(name="service_smtp_transparent",
        proxy_class = SmtpProxy,
        router = TransparentRouter()
    )

    Rule(service='service_smtp_transparent',
         dst_port = 25,
         src_zone = ('clients'),
         dst_zone = ('servers')
    )
