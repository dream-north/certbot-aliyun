#!/bin/bash
certbot certonly -d $CERTBOT_DOMAINS -n -m $CERTBOT_EMAIL --no-eff-email --agree-tos --manual --preferred-challenges dns --manual-auth-hook "python3 aliyun_dns_auth.py add" --manual-cleanup-hook "python3 aliyun_dns_auth.py clean"
