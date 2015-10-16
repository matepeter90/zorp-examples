Zone(name="clients",
     addr = ["172.16.10.0/23", ],
    )

Zone(name="servers",
     addr = ["172.16.20.0/23", ],
    )

Zone(name="servers.http_url_filter",
         addrs = ["172.16.21.29/32", ],
         admin_parent = "servers"
        )
