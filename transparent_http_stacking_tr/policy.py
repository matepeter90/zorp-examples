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

class HttpProxyStackTr(HttpProxy):
    def config(self):
        HttpProxy.config(self)
        #Header modification is needed to avoid data compression.
        self.request_header["Accept-Encoding"] = (HTTP_HDR_POLICY, self.processAcceptEncoding)
        self.response_stack["GET"] = (HTTP_STK_DATA, (Z_STACK_PROGRAM, '/usr/bin/tr \'[a-z]\' \'[A-Z]\''))

    def processAcceptEncoding(self, name, value):
        lst_value = value.split(',')
        if 'gzip' in lst_value:
            lst_value.remove('gzip')
        if 'bzip' in lst_value:
            lst_value.remove('bzip')
        if 'bzip2' in lst_value:
            lst_value.remove('bzip2')
        if 'compress' in lst_value:
            lst_value.remove('compress')
        self.current_header_value = ','.join(lst_value)

        return HTTP_HDR_ACCEPT

def stack_instance():
    Service(name="service_http_transparent_stack_tr",
        proxy_class=HttpProxyStackTr,
        router=TransparentRouter()
    )
    Rule(service='service_http_transparent_stack_tr',
         dst_port=80,
         src_zone=('clients', ),
         dst_zone=('servers.http_stack_tr', )
    )
