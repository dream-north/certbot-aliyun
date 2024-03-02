FROM ubuntu:20.04

COPY ./requirements.txt ./

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime

RUN apt update \
    && apt install -y python3 python3-pip libaugeas0 \
    && pip install -r requirements.txt \
    && apt clean

WORKDIR /app
COPY ./aliyun_dns_auth.py /app/
COPY ./certonly.sh /app/
COPY ./renew.sh /app/
COPY ./run.sh /app/

RUN chmod +x ./certonly.sh ./renew.sh ./run.sh

CMD ["./run.sh"]
