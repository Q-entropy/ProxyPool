#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dao.Proxy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.global_var import DB_CONFIG

class SQL_Helper():
    params = {'ip': Proxy.ip, 'port': Proxy.port, 'types': Proxy.types, 'protocol': Proxy.protocol,
              'country': Proxy.country, 'area': Proxy.area, 'score': Proxy.score}

    def __init__(self):
        print(DB_CONFIG['DB_CONNECT_string'])
        self.engine = create_engine(DB_CONFIG['DB_CONNECT_string'], echo=False)
        DB_Session = sessionmaker(bind=self.engine)
        self.session = DB_Session()

    def create_db(self):
        BaseModel.metadata.create_all(self.engine)

    def drop_db(self):
        BaseModel.metadata.drop_all(self.engine)


    def insert(self, value):
        proxy = Proxy(ip=value['ip'], port=value['port'], types=value['types'], protocol=value['protocol'],
                      country=value['country'],
                      area=value['area'], speed=value['speed'])
        self.session.add(proxy)
        self.session.commit()


    def delete(self, conditions=None):
        if conditions:
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(self.params.get(key) == conditions.get(key))
            conditions = conditon_list
            query = self.session.query(Proxy)
            for condition in conditions:
                query = query.filter(condition)
            deleteNum = query.delete()
            self.session.commit()
        else:
            deleteNum = 0
        return ('deleteNum', deleteNum)


    def update(self, conditions=None, value=None):
        '''
        conditions的格式是个字典。类似self.params
        :param conditions:
        :param value:也是个字典：{'ip':192.168.0.1}
        :return:
        '''
        if conditions and value:
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(self.params.get(key) == conditions.get(key))
            conditions = conditon_list
            query = self.session.query(Proxy)
            for condition in conditions:
                query = query.filter(condition)
            updatevalue = {}
            for key in list(value.keys()):
                if self.params.get(key, None):
                    updatevalue[self.params.get(key, None)] = value.get(key)
            updateNum = query.update(updatevalue)
            self.session.commit()
        else:
            updateNum = 0
        return {'updateNum': updateNum}

    @staticmethod
    def select(self, count=None, conditions=None):
        if conditions:
            conditon_list = []
            for key in list(conditions.keys()):
                if self.params.get(key, None):
                    conditon_list.append(self.params.get(key) == conditions.get(key))
            conditions = conditon_list
        else:
            conditions = []

        query = self.session.query(Proxy.ip, Proxy.port, Proxy.score)
        if len(conditions) > 0 and count:
            for condition in conditions:
                query = query.filter(condition)
            return query.order_by(Proxy.score.desc(), Proxy.speed).limit(count).all()
        elif count:
            return query.order_by(Proxy.score.desc(), Proxy.speed).limit(count).all()
        elif len(conditions) > 0:
            for condition in conditions:
                query = query.filter(condition)
            return query.order_by(Proxy.score.desc(), Proxy.speed).all()
        else:
            return query.order_by(Proxy.score.desc(), Proxy.speed).all()


    def close(self):
        pass

if __name__ == '__main__':
    sqlhelper = SQL_Helper()
    sqlhelper.create_db()
    proxy = {'ip': '192.168.1.1', 'port': 80, 'protocol': 0, 'country': '中国', 'area': '广州', 'speed': 11.123, 'types': 0}
    sqlhelper.insert(proxy)
    sqlhelper.update({'ip': '192.168.1.1', 'port': 80}, {'score': 10})
    print(sqlhelper.select(1))