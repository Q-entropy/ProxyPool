#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from util.var import var
import random

def get_RandHeader():
    return {
        'User-Agent': random.choice(var.UserAgent_list),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
    }
