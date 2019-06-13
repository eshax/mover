# -*- coding:utf-8 -*-

'''
otc价格
'''

import os, sys, time, json, redis
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.http import http

rdb = redis.Redis(host='127.0.0.1', port=6379, db=0)

class otc:

    coins = {
        'btc' : 1,
        'usdt' : 2,
        'eth' : 3,
    }

    api = 'https://otc-api.eiijo.cn/v1/data/trade-market?country=37&currency=1&payMethod=0&currPage=1&coinId=%s&tradeType=%s&blockType=general&online=1'

    @staticmethod
    def get():
        for coin in otc.coins:
            for type in ['buy', 'sell']:
                code, content = http.get( otc.api % (otc.coins[coin], type))
                if code == 200:
                    js = json.loads(content)
                    k = '%s_%s' % (coin, type)
                    v = js['data'][0]['price']
                    rdb.hset('otc', k, v)

if __name__ == "__main__":

    otc.get()

