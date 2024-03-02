import pytest

from aliyun_dns_auth import AliyunDnsAuth

def test_get_base_domain() -> None:
    assert AliyunDnsAuth._get_base_domain('*.example.com') == 'example.com'
    assert AliyunDnsAuth._get_base_domain('example.com') == 'example.com'
    assert AliyunDnsAuth._get_base_domain('a.example.com') == 'example.com'
    assert AliyunDnsAuth._get_base_domain('a.example.com.cn') == 'example.com.cn'

def test_get_pr() -> None:
    assert AliyunDnsAuth._get_pr('*.example.com') == '_acme-challenge'
    assert AliyunDnsAuth._get_pr('example.com') == '_acme-challenge'
    assert AliyunDnsAuth._get_pr('a.example.com') == '_acme-challenge.a'
    assert AliyunDnsAuth._get_pr('a.example.com.cn') == '_acme-challenge.a'

