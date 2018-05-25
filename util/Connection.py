#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import chardet
import requests
import re
from bs4 import BeautifulSoup
from lxml import etree

from config.global_var import profile_CONFIG
from dao.SQL_Helper import SQL_Helper
from util.get_RandHeader import get_RandHeader


class Connection():
    @staticmethod
    def download(url):
        CONNECT_CONFIG = profile_CONFIG['CONNECT_CONFIG']
        try:
            r = requests.get(url=url, headers=get_RandHeader(), timeout=CONNECT_CONFIG['TIME_OUT'])
            r.encoding = chardet.detect(r.content)['encoding']
            if (not r.ok) or len(r.content) < 500:
                raise ConnectionError
            else:
                return r.text

        except Exception:
            count = 0  # 重试次数
            proxylist = SQL_Helper.select(10)
            if not proxylist:
                return None

            while count < CONNECT_CONFIG['RETRY_TIME']:
                try:
                    proxy = random.choice(proxylist)
                    ip = proxy[0]
                    port = proxy[1]
                    proxies = {"http": "http://%s:%s" % (ip, port), "https": "http://%s:%s" % (ip, port)}

                    r = requests.get(url=url, headers=get_RandHeader(), timeout=CONNECT_CONFIG['TIME_OUT'], proxies=proxies)
                    r.encoding = chardet.detect(r.content)['encoding']
                    if (not r.ok) or len(r.content) < 500:
                        raise ConnectionError
                    else:
                        return r.text
                except Exception:
                    count += 1

        return None

    @staticmethod
    def to_BS4(url):
        return BeautifulSoup(Connection.download(url), 'lxml')

    @staticmethod
    def xpath_parser(url, parser):
        item_list = []
        response = Connection.download(url)
        root = etree.HTML(response)
        items = root.xpath(parser['pattern'])
        positions = eval(parser['position'])
        for item in items:
            unit = {}
            for key, value in positions.items():
                unit[key] = item.xpath(value)[0].text
            item_list.append(unit)
        return item_list

    @staticmethod
    def regex_parser(url, parser):
        item_list = []
        response = Connection.download(url)
        pattern = re.compile(parser['pattern'])
        matchs = pattern.findall(response)
        positions = eval(parser['position'])
        for match in matchs:
            unit = {}
            for key, value in positions.items():
                unit[key] = match[value]
            item_list.append(unit)
        return item_list

if __name__ == '__main__':
    ttt = {}
    ttt['pattern'] = './/*[@id="ip_list"]/tr[position()>1]'
    ttt['position'] = "{'ip': './td[2]', 'port': './td[3]', 'type': './td[5]', 'protocol': './td[6]'}"
    print(Connection.xpath_parser('http://www.xicidaili.com/nn/1', ttt))

