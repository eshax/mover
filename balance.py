# -*- coding:utf-8 -*-

'''
各个交易所余额
'''

import os, sys, time, json, pymongo, redis
import mysql.connector.pooling

from services.coinw import coinw
from services.jccdex import jccdex
from services.huobi import huobi

mdb = pymongo.MongoClient('127.0.0.1', 27017)
rdb = redis.Redis(host='127.0.0.1', port=6379, db=0)

dbconfig = {
    "user": "root",
    "password": "Trading123!@#",
    "host": "127.0.0.1",
    "database": "trading"
}

dbpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="dbpool",
                                                     pool_size=5,
                                                     pool_reset_session=True,
                                                     **dbconfig)
dbconn = dbpool.get_connection()
db = dbconn.cursor()

class balance:

    @staticmethod
    def get():
        sql = 'INSERT INTO exchange (name, coin, free, freezed, time) VALUES (%s, %s, %s, %s, %s)'

        coinw_balance = coinw.get_account()
        balance.save(coinw_balance)
        jccdex_balance = jccdex.get_balances()
        balance.save(jccdex_balance)
        dbconn.commit()
        db.close()
        dbconn.close()
        # huobi_balance = huobi.get_symbols()

    @staticmethod
    def save(data):
        sql = 'INSERT INTO exchange (name, coin, free, freezed) VALUES (%s, %s, %s, %s)'
        for key in data:
            if key == 'exchange':
                continue
            item = data[key]
            o = [data['exchange'], key, item['free'], item['freezed']]
            db.execute(sql, o)


if __name__ == "__main__":

    balance.get()

