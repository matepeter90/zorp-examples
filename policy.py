#############################################################################
## -*- coding: UTF-8 -*-
##
## Copyright (c) 2011 BalaBit IT Ltd, Budapest, Hungary
## Copyright (c) 2011 Szilárd Pfeiffer <szilard.pfeiffer@balabit.com>
## Copyright (c) 2011 Tibor Balázs <tibor.balazs@balabit.com>
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

InetZone(name="clients",
         addrs=["172.16.10.0/23", ],
         inbound_services=["*"],
         outbound_services=["*"]
        )

InetZone(name="servers",
         addrs=["172.16.20.0/23", ],
         inbound_services=["*"],
         outbound_services=["*"]
        )

def zorp_instance():
    #http services
    Service(name='service_http_transparent',
            proxy_class=HttpProxy,
            router=TransparentRouter()
    )
    Service(name="service_http_transparent_directed",
            proxy_class=HttpProxy,
            router=DirectedRouter(dest_addr=SockAddrInet('172.16.20.254', 80))
    )
    Service(name="service_http_nontransparent_inband",
            proxy_class=HttpProxyNonTransparent,
            router=InbandRouter(forge_port=TRUE)
    )

    #ftp services
    Service(name="service_ftp_transparent",
            proxy_class=FtpProxyRO,
            router=TransparentRouter()
    )

    Rule(service='service_http_transparent',
         dst_port=80,
         src_zone=('clients', ),
         dst_zone=('servers', )
    )
    Rule(service='service_http_transparent_directed',
         dst_port=8080,
         src_zone=('clients', )
    )
    Rule(service='service_http_nontransparent_inband',
         dst_port=50080,
         dst_subnet=('172.16.10.254', ),
         src_zone=('clients', )
    )

    Rule(service='service_ftp_transparent',
         dst_port=21,
         src_zone=('clients', ),
         dst_zone=('servers', )
    )
