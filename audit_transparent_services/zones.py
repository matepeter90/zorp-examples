Zone(name="clients",
     addr = ["172.16.10.0/23", ],
    )

Zone(name="servers",
     addr = ["172.16.20.0/23", ],
    )

Zone(name="servers.audit",
         addrs = ["172.16.21.1/32", ],
         admin_parent = "servers"
        )

