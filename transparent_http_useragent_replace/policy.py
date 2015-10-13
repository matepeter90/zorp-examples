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

class HttpProxyHeaderReplace(HttpProxy):
    def config(self):
        HttpProxy.config(self)
        self.request_header["User-Agent"] = (HTTP_HDR_CHANGE_VALUE, "Forged Browser 1.0")

def zorp_instance():
    Service(name="service_http_transparent_header_replace",
        proxy_class=HttpProxyHeaderReplace,
        router=TransparentRouter()
    )

    Rule(service='service_http_transparent_header_replace',
         dst_port=80,
         src_zone=('clients', ),
         dst_zone=('servers.http_header_replace', )
    )
