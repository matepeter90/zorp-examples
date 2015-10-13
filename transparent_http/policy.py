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

from Zorp.Http import *

from zones import *

def zorp_instance():
    #http services
    Service(name='service_http_transparent',
            proxy_class=HttpProxy,
            router=TransparentRouter()
    )

    Rule(service='service_http_transparent',
         dst_port=80,
         src_zone=('clients', ),
         dst_zone=('servers', )
    )
