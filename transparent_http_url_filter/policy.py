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

from Zorp.Http import *

from zones import *

class HttpProxyUrlFilter(HttpProxy):
        def config(self):
                HttpProxy.config(self)
                self.request["GET"] = (HTTP_REQ_POLICY, self.filterURL)

        def filterURL(self, method, url, version):
                if (url == "http://server_disallowed.zorp/"):
                        self.error_info = 'Access of this content is denied by the local policy.'
                        return HTTP_REQ_REJECT
                return HTTP_REQ_ACCEPT

def zorp_instance():
    Service(name="service_http_transparent_url_filter",
        proxy_class=HttpProxyUrlFilter,
        router=TransparentRouter()
    )

    Rule(service='service_http_transparent_url_filter',
         dst_port=80,
         src_zone=('clients', ),
         dst_zone=('servers.http_url_filter', )
    )
