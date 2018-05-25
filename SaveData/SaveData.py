#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from dao.SQL_Helper import SQL_Helper

class SaveData():

    def start(self, proxy_queue, db_proxy_num):
        successNum = 0
        failNum = 0
        helper = SQL_Helper()
        while True:
            try:
                proxy = proxy_queue.get(timeout=300)
                if proxy:
                    helper.insert(proxy)
                    successNum += 1
                else:
                    failNum += 1
                str = 'Fetch proxy from the queue……\tInsert proxy into database……\t' \
                      'Success ip num :%d,Fail ip num:%d' % (successNum, failNum)
                sys.stdout.write(str + "\r")
                sys.stdout.flush()
            except BaseException as e: ### 队列为空，抛出异常
                if db_proxy_num.value != 0:
                    successNum += db_proxy_num.value
                    db_proxy_num.value = 0
                    str = 'The proxy queue is empty\tNow check the passing data\t' \
                          'Success ip num :%d,Fail ip num:%d' % (successNum, failNum)
                    sys.stdout.write(str + "\r")
                    sys.stdout.flush()
                    successNum = 0
                    failNum = 0
