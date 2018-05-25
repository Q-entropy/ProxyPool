#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class var:
    UserAgent_list = []

def read_Headers():
    AGENT_FILE = 'UserAgent.txt'
    var.UserAgent_list = open(AGENT_FILE).read().splitlines()

def var_config():
    read_Headers()