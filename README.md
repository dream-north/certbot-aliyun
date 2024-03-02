# certbot-aliyun
使用certbot生成和定期续签证书（nginx），在验证时自动添加阿里云DNS记录，验证后删除。

使用方法：
1. 在`docker-compose.yml`中填写相关环境变量
```{yaml}
services:
  certbot-aliyun:
    build: .
    environment:
      - TZ=Asia/Shanghai
      - ALIYUN_ACCESS_KEY_ID=***  # 阿里云AK
      - ALIYUN_ACCESS_KEY_SECRET=***  # 阿里云SK
      - CERTBOT_DOMAINS=example.com,*.example.com  # 申请的域名
      - CERTBOT_EMAIL=me@mail.com  # 个人邮箱
      - RENEW_PERIOD=86400  # 多久执行一次renew
    volumes:
      - ./letsencrypt:/etc/letsencrypt  # 生成的证书会保存在这里
```
2. build容器并执行
```
sudo docker-compose up -d
```
3. 证书会生成在容器的/etc/letsencrypt/live目录下，如果挂载了宿主机的盘，直接在nginx配置中指向这个证书即可。
