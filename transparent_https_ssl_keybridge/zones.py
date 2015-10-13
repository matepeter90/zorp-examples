############################################################################
## -*- coding: UTF-8 -*-
##
## Copyright (c) 2014 BalaBit IT Ltd, Budapest, Hungary
## Copyright (c) 2014 Szilárd Pfeiffer <szilard.pfeiffer@balabit.com>
## Copyright (c) 2014 Tibor Balázs <tibor.balazs@balabit.com>
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


InetZone(name="clients",
     addr=["172.16.10.0/23", ],
     inbound_services=["*"],
     outbound_services=["*"]
    )

InetZone(name="servers",
     addr=["172.16.20.0/23", ],
     inbound_services=["*"],
     outbound_services=["*"]
    )

InetZone(name="servers.plug",
     addrs=["172.16.21.33/32", ],
     inbound_services=["*"],
     outbound_services=["*"],
     admin_parent="servers"
    )
