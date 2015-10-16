Zone(name="clients",
     addr = ["172.16.10.0/23", ],
    )

Zone(name="servers",
     addr = ["172.16.20.0/23", ],
    )

Zone(name="servers.smtp_one_sided_ssl",
         addrs = ["172.16.21.13/32", ],
         admin_parent = "servers"
        )
