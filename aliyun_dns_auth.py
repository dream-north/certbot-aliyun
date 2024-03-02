import os
import sys
import tldextract
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DeleteDomainRecordRequest import DeleteDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest

# 阿里云 Access Key ID 和 Access Key Secret
ACCESS_KEY_ID = os.getenv('ALIYUN_ACCESS_KEY_ID')
ACCESS_KEY_SECRET = os.getenv('ALIYUN_ACCESS_KEY_SECRET')

# 获取 Certbot 提供的环境变量
CERTBOT_DOMAIN = os.getenv('CERTBOT_DOMAIN')
CERTBOT_VALIDATION = os.getenv('CERTBOT_VALIDATION')


class AliyunDnsAuth:
    challange_pr = '_acme-challenge'
    def __init__(self) -> None:
        self.client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, 'cn-hangzhou')

    def add_dns_record(self) -> None:
        # 创建添加 DNS 记录的请求
        request = AddDomainRecordRequest()
        request.set_accept_format('json')
        
        # 设置域名和记录类型
        request.set_DomainName(self._get_base_domain(CERTBOT_DOMAIN))  # 这里需要设置为你的域名的主域名
        request.set_RR(self._get_pr(CERTBOT_DOMAIN))  # 这里设置子域名
        request.set_Type('TXT')
        request.set_Value(CERTBOT_VALIDATION)
        
        # 发送请求
        response = self.client.do_action_with_exception(request)
        
        print(str(response, encoding='utf-8'))

    def clean_dns_record(self) -> None:
        query_request = DescribeDomainRecordsRequest()
        query_request.set_accept_format('json')
        query_request.set_DomainName(self._get_base_domain(CERTBOT_DOMAIN))  # 替换为你的主域名
        query_request.set_RRKeyWord(self._get_pr(CERTBOT_DOMAIN))
        query_request.set_Type('TXT')
        query_response = self.client.do_action_with_exception(query_request)
        records = json.loads(str(query_response, encoding='utf-8'))['DomainRecords']['Record']

        for record in records:
            delete_request = DeleteDomainRecordRequest()
            delete_request.set_accept_format('json')
            delete_request.set_RecordId(record['RecordId'])
            response = self.client.do_action_with_exception(delete_request)
            print(str(response, encoding='utf-8'))

    @staticmethod
    def _get_base_domain(domain: str) -> str:
        ext = tldextract.extract(domain)
        # 组合二级域名（如果有）和顶级域名
        base_domain = "{}.{}".format(ext.domain, ext.suffix)
        return base_domain

    @classmethod
    def _get_pr(cls, domain: str) -> str:
        base_domain = cls._get_base_domain(domain)
        if domain.startswith("*."):
            pr = cls.challange_pr
        else:
            pr = f'{cls.challange_pr}.' + domain.replace(base_domain, '').strip('.')
        return pr.strip('.')

if __name__ == '__main__':
    method = sys.argv[-1]
    if method == 'add':
        AliyunDnsAuth().add_dns_record()
    elif method == 'clean':
        AliyunDnsAuth().clean_dns_record()
    else:
        raise ValueError(f'method must be one of [`add`, `clean`], but got {method} !')
