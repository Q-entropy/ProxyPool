#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dao.SQL_Helper import SQL_Helper
from dao.Proxy import Proxy
from util.check_proxy import check_proxy
from multiprocessing import Process, Queue

class Validator():

    def __init__(self):
        check_queue = Queue()

    def check_from_DB(self, proxy_dict):
        helper = SQL_Helper()
        proxies = check_proxy.get_proxies(proxy_dict['ip'], proxy_dict['port'])
        result = check_proxy.check_http_or_https(proxies=proxies)
        if result['isValid']:
            helper.update({'ip': proxy_dict['ip'], 'port': proxy_dict['port']},
                          {'speed': result['speed'], 'types':result['types'], 'protol': result['protol']})
        else:
            proxy_dict['score'] -= 1
            if proxy_dict['score'] <= 0:
                helper.delete({'ip': proxy_dict['ip'], 'port': proxy_dict['port']})
            else:
                helper.update({'ip': proxy_dict['ip'], 'port': proxy_dict['port']},
                          {'score':proxy_dict['score']})