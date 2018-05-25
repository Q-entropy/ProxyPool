#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from config.global_var import *
from config import global_var

def global_config():
    profile_file = os.getcwd() + '/profile.txt'
    parts = open(profile_file).read().split('###')
    for part in parts:
        part_params = part.strip().split('\n')
        if len(part_params) != 0:
            first_key = part_params[0]
            profile_CONFIG[first_key] = {}
            for key_value in part_params[1:]:
                key_value_process(profile_CONFIG[first_key], key_value)
    post_process()

def post_process():
    global_var.DB_CONFIG = profile_CONFIG['DB_CONFIG']
    global_var.CONNECT_CONFIG = profile_CONFIG['CONNECT_CONFIG']
    global_var.DEFAULT_CONFIG = profile_CONFIG['DEFAULT_CONFIG']
    global_var.CRAWLER_CONFIG = profile_CONFIG['CRAWLER_CONFIG']
    global_var.RUNTIME_CONFIG = profile_CONFIG['RUNTIME_CONFIG']

    ## 数据库连接命令
    global_var.DB_CONFIG['DB_CONNECT_STRING'] \
        = 'mysql+mysqlconnector://' + \
            global_var.DB_CONFIG['DB_USER'] + ':' + \
            global_var.DB_CONFIG['DB_PASSWORD'] + '@' + \
            global_var.DB_CONFIG['DB_IP'] + ':' + \
            global_var.DB_CONFIG['DB_PORT'] + '/' + \
            global_var.DB_CONFIG['DB_NAME']

def key_value_process(parent_dict, key_value_str):
    key_value_params = key_value_str.strip().split(maxsplit=1)
    key = key_value_params[0]
    value = str_process(key_value_params[1])
    parent_dict[key] = value

def str_process(value):
    if value[0] == '\'':
        return value[1:-1]
    elif '.' in value:
        return float(value)
    else:
        return int(value)

if __name__ == '__main__':
    global_config()