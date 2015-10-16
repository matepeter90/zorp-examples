Zone(name="clients",
     addr = ["172.16.10.0/23", ],
    )

Zone(name="servers",
     addr = ["172.16.20.0/23", ],
    )

Zone(name="servers.http_header_replace",
         addrs = ["172.16.21.25/32", ],
         admin_parent = "servers"
        )
