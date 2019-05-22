# -*- coding:utf-8 -*-

'''
各个交易所余额
'''

import os, sys, time, json, pymongo, redis

from services.coinw import coinw
from services.jccdex import jccdex
from services.huobi import huobi

mdb = pymongo.MongoClient('127.0.0.1', 27017)
rdb = redis.Redis(host='127.0.0.1', port=6379, db=0)

class balance:

    @staticmethod
    def get():

        # coinw_balance = coinw.get_account()
        # print(coinw_balance)
        # jccdex_balance = jccdex.get_balances()
        # print(jccdex_balance)
        huobi_balance = huobi.get_symbols()




if __name__ == "__main__":

    balance.get()

