#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import time
import json

from config.global_var import profile_CONFIG
from util.get_RandHeader import get_RandHeader

class check_proxy():

    @staticmethod
    def get_HostIP():
        CONNECT_CONFIG = profile_CONFIG['CONNECT_CONFIG']
        try:
            r = requests.get(url=CONNECT_CONFIG['CHECK_IP'], headers=get_RandHeader(), timeout=CONNECT_CONFIG['TIME_OUT'])
            ip = json.loads(r.text)
            return ip['origin']
        except Exception as e:
            print('主机IP获取失败')
            print(e)

    @staticmethod
    def get_proxies(IP, port):
        return {"http": "http://%s:%s" % (IP, port), "https": "http://%s:%s" % (IP, port)}

    @staticmethod
    def check_http_or_https(proxies):
        check_result = {}
        check_result['isValid'] = True
        http_result = check_proxy.__check_isValid(proxy=proxies, isHttp=True)
        https_result = check_proxy.__check_isValid(proxy=proxies, isHttp=False)
        if http_result['isValid'] and https_result['isValid']:
            check_result['protol'] = 2
            check_result['types'] = http_result['types']
            check_result['speed'] = http_result['speed']
        elif https_result['isValid']:
            check_result['protol'] = 1
            check_result['types'] = https_result['types']
            check_result['speed'] = https_result['speed']
        elif http_result['isValid']:
            check_result['protol'] = 0
            check_result['types'] = http_result['types']
            check_result['speed'] = http_result['speed']
        else:
            check_result['isValid'] = False
        return check_result

    @staticmethod
    def __check_isValid(proxies, isHttp=True):
        CONNECT_CONFIG = profile_CONFIG['CONNECT_CONFIG']
        check_result = []
        if isHttp : test_url = CONNECT_CONFIG['TEST_HTTP_HEADER']
        else : test_url = CONNECT_CONFIG['TEST_HTTP_HEADER']
        try:
            start = time.time()
            r = requests.get(url=test_url, headers=get_RandHeader(), timeout=CONNECT_CONFIG['TIME_OUT'], proxies=proxies)
            if r.ok:
                check_result['speed'] = round(time.time() - start, 2)
                content = json.loads(r.text)
                headers = content['headers']
                ip = content['origin']
                proxy_connection = headers.get('Proxy-Connection', None)
                if ',' in ip:
                    check_result['types'] = 2
                elif proxy_connection:
                    check_result['types'] = 1
                else:
                    check_result['types'] = 0

                check_result['isValid'] = True
            else:
                check_result['isValid'] = False
        except Exception as e:
            check_result['isValid'] = False
        return check_result