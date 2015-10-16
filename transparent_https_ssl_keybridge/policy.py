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


Zone(name="clients",
     addr = ["172.16.10.0/23", ],
    )

Zone(name="servers",
     addr = ["172.16.20.0/23", ],
    )

Zone(name="servers.plug",
     addrs = ["172.16.21.33/32", ],
     admin_parent = "servers"
    )

class HttpsProxyKeybridge(HttpProxy):
    key_generator = X509KeyBridge(
        key_file = "/etc/zorp/keybridge/key.pem",
        key_passphrase = "passphrase",
        cache_directory = "/var/lib/zorp/keybridge-cache",
        trusted_ca_files = (
            "/etc/zorp/keybridge/ZorpGPL_TrustedCA.cert.pem",
            "/etc/zorp/keybridge/ZorpGPL_TrustedCA.key.pem",
            "passphrase"
        ),
        untrusted_ca_files = (
            "/etc/zorp/keybridge/ZorpGPL_UnTrustedCA.cert.pem",
            "/etc/zorp/keybridge/ZorpGPL_UnTrustedCA.key.pem",
            "passphrase"
        )
    )

    def config(self):
        HttpProxy.config(self)
        self.require_host_header = FALSE
        self.ssl.handshake_seq = SSL_HSO_SERVER_CLIENT
        self.ssl.key_generator = self.key_generator
        self.ssl.client_keypair_generate = TRUE
        self.ssl.client_connection_security = SSL_FORCE_SSL
        self.ssl.client_verify_type = SSL_VERIFY_OPTIONAL_UNTRUSTED
        self.ssl.server_connection_security = SSL_FORCE_SSL
        self.ssl.server_verify_type = SSL_VERIFY_REQUIRED_UNTRUSTED
        self.ssl.server_ca_directory = "/etc/ssl/certs"
        self.ssl.server_trusted_certs_directory = "/etc/zorp/certs"

def zorp_instance():
    #plug service
    Service(name="service_plug",
        proxy_class = PlugProxy,
        router = TransparentRouter()
    )

    #https services
    Service(name="service_https_transparent",
        proxy_class = HttpsProxyKeybridge,
        router = TransparentRouter()
    )

    Rule(service='service_plug',
         dst_port = 443,
         src_zone = ('clients', ),
         dst_zone = ('servers.plug', )
    )
    Rule(service='service_https_transparent',
         dst_port = 443,
         src_zone = ('clients', ),
         dst_zone = ('servers', )
    )
