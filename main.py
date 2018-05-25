#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import config
from config.global_var import profile_CONFIG
from util.Connection import Connection

ttt = {}
ttt['pattern'] = './/*[@id="ip_list"]/tr[position()>1]'
ttt['position'] = "{'ip': './td[2]', 'port': './td[3]', 'type': './td[5]', 'protocol': './td[6]'}"
print(Connection.xpath_parser('http://www.xicidaili.com/nn/1', ttt))