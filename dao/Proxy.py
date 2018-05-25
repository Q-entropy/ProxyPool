#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import Column, Integer, DateTime, Numeric, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from config.global_var import DEFAULT_CONFIG

BaseModel = declarative_base()

class Proxy(BaseModel):
    __tablename__ = 'proxy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(VARCHAR(16), nullable=False)
    port = Column(Integer, nullable=False)
    types = Column(Integer, nullable=False)
    protocol = Column(Integer, nullable=False, default=0)
    country = Column(VARCHAR(100), nullable=False)
    area = Column(VARCHAR(100), nullable=False)
    updatetime = Column(DateTime(), default=datetime.datetime.utcnow)
    speed = Column(Numeric(5, 2), nullable=False)
    score = Column(Integer, nullable=False, default=DEFAULT_CONFIG['DEFAULT_SCORE'])