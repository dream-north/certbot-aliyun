#!/bin/bash
certbot renew --manual --preferred-challenges dns --manual-auth-hook "python3 aliyun_dns_auth.py add" --manual-cleanup-hook "python3 aliyun_dns_auth.py clean"
