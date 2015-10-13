Zorp examples
-------------

These folders contain various configuration examples for Zorp proxy firewall.

You just have to replace the /etc/zorp directory's content with one of the examples and start the instance.

Transparent HTTP proxy
----------------------
```bash
    sudo zorpctl stop zorp_instance
    sudo mv /etc/zorp /etc/zorp.backup
    sudo ln -s /home/user/zorp-examples/transparent_http /etc/zorp
    sudo zorpctl start zorp_instance
```
Transparent FTP proxy with virus scanning
----------------------------------------
```bash
    sudo zorpctl stop zorp_instance
    sudo mv /etc/zorp /etc/zorp.backup
    sudo ln -s /home/user/zorp-examples/transparent_ftp_clamav /etc/zorp
    sudo zorpctl start stack_instance
```
