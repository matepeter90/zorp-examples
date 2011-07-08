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
from Zorp.Proxy import *

from Zorp.Ftp import *
from Zorp.Http import *
from Zorp.Pop3 import *
from Zorp.Smtp import *

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

InetZone(name="servers.audit",
         addrs=["172.16.21.1/32", ],
         inbound_services=["*"],
         outbound_services=["*"],
         admin_parent="servers"
        )

InetZone(name="servers.stack_clamav",
         addrs=["172.16.21.5/32", ],
         inbound_services=["*"],
         outbound_services=["*"],
         admin_parent="servers"
        )

InetZone(name="servers.smtp_starttls",
         addrs=["172.16.21.9/32", ],
         inbound_services=["*"],
         outbound_services=["*"],
         admin_parent="servers"
        )

InetZone(name="servers.smtp_one_sided_ssl",
         addrs=["172.16.21.13/32", ],
         inbound_services=["*"],
         outbound_services=["*"],
         admin_parent="servers"
        )

InetZone(name="servers.http_stack_cat",
         addrs=["172.16.21.17/32", ],
         inbound_services=["*"],
         outbound_services=["*"],
         admin_parent="servers"
        )

InetZone(name="servers.http_stack_tr",
         addrs=["172.16.21.21/32", ],
         inbound_services=["*"],
         outbound_services=["*"],
         admin_parent="servers"
        )

class FtpProxyNonTransparent(FtpProxy):
    def config(self):
        FtpProxy.config(self)
        self.transparent_mode=FALSE

class SmtpProxyStartTls(SmtpProxy):
    def config(self):
        SmtpProxy.config(self)
        self.relay_zones=("*",)
        self.ssl.client_connection_security = SSL_ACCEPT_STARTTLS
        self.ssl.client_verify_type = SSL_VERIFY_OPTIONAL_UNTRUSTED
        self.ssl.client_keypair_files=(
                           "/etc/ssl/certs/ssl-cert-snakeoil.pem",
                           "/etc/ssl/private/ssl-cert-snakeoil.key"
                                              )
        self.ssl.server_verify_type = SSL_VERIFY_OPTIONAL_UNTRUSTED

class SmtpProxyOneSideSsl(SmtpProxy):
    def config(self):
        SmtpProxy.config(self)
        self.relay_zones=("*",)
        self.ssl.server_connection_security=SSL_FORCE_SSL
        self.ssl.server_verify_type=SSL_VERIFY_OPTIONAL_UNTRUSTED

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
    Service(name="service_ftp_nontransparent_inband",
            proxy_class=FtpProxyNonTransparent,
            router=InbandRouter(forge_port=TRUE)
    )

    #smtp services
    Service(name="service_smtp_transparent",
        proxy_class=SmtpProxy,
        router=TransparentRouter()
    )
    Service(name="service_smtp_transparent_starttls",
        proxy_class=SmtpProxyStartTls,
        router=TransparentRouter()
    )
    Service(name="service_smtp_transparent_one_sided_ssl",
        proxy_class=SmtpProxyOneSideSsl,
        router=DirectedRouter(dest_addr=(SockAddrInet('172.16.20.254', 465),))
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
    Rule(service='service_ftp_nontransparent_inband',
         dst_port=50021,
         dst_subnet=('172.16.10.254', ),
         src_zone=('clients', )
    )

    Rule(service='service_smtp_transparent',
         dst_port=25,
         src_zone=('clients'),
         dst_zone=('servers')
    )
    Rule(service='service_smtp_transparent_starttls',
         dst_port=25,
         src_zone=('clients'),
         dst_zone=('servers.smtp_starttls')
    )
    Rule(service='service_smtp_transparent_one_sided_ssl',
         dst_port=25,
         src_zone=('clients'),
         dst_zone=('servers.smtp_one_sided_ssl')
    )

def audit_instance():
    Service(name="service_ftp_transparent_audit",
        proxy_class=FtpProxy,
        router=TransparentRouter()
    )
    Service(name="service_http_transparent_audit",
        proxy_class=HttpProxy,
        router=TransparentRouter()
    )
    Service(name="service_pop3_transparent_audit",
        proxy_class=Pop3Proxy,
        router=TransparentRouter()
    )
    Service(name="service_smtp_transparent_audit",
        proxy_class=SmtpProxy,
        router=TransparentRouter()
    )

    Rule(service='service_ftp_transparent_audit',
         dst_port=21,
         src_zone=('clients', ),
         dst_zone=('servers.audit', )
    )
    Rule(service='service_http_transparent_audit',
         dst_port=80,
         src_zone=('clients', ),
         dst_zone=('servers.audit', )
    )
    Rule(service='service_pop3_transparent_audit',
         dst_port=110,
         src_zone=('clients', ),
         dst_zone=('servers.audit', )
    )
    Rule(service='service_smtp_transparent_audit',
         dst_port=25,
         src_zone=('clients', ),
         dst_zone=('servers.audit', )
    )

class HttpProxyStackClamav(HttpProxy):
    def config(self):
        HttpProxy.config(self)
        self.keep_persistent = TRUE
        self.response_stack["GET"] = (HTTP_STK_DATA, (Z_STACK_PROGRAM, '/etc/zorp/scripts/clamav_stack.py'))

class HttpProxyStackCat(HttpProxy):
    def config(self):
        HttpProxy.config(self)
        self.response_stack["GET"] = (HTTP_STK_DATA, (Z_STACK_PROGRAM, '/bin/cat'))

class HttpProxyStackTr(HttpProxy):
    def config(self):
        HttpProxy.config(self)
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
    Service(name="service_http_transparent_stack_clamav",
        proxy_class=HttpProxyStackClamav,
        router=TransparentRouter()
    )
    Service(name="service_http_transparent_stack_cat",
        proxy_class=HttpProxyStackCat,
        router=TransparentRouter()
    )
    Service(name="service_http_transparent_stack_tr",
        proxy_class=HttpProxyStackTr,
        router=TransparentRouter()
    )

    Rule(service='service_http_transparent_stack_clamav',
         dst_port=80,
         src_zone=('clients', ),
         dst_zone=('servers.stack_clamav', )
    )
    Rule(service='service_http_transparent_stack_cat',
         dst_port=80,
         src_zone=('clients', ),
         dst_zone=('servers.http_stack_cat', )
    )
    Rule(service='service_http_transparent_stack_tr',
         dst_port=80,
         src_zone=('clients', ),
         dst_zone=('servers.http_stack_tr', )
    )
