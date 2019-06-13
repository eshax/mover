# -*- coding:utf-8 -*-

import time, redis
import mysql.connector.pooling

from services.jccdex import jccdex
from services.coinbene import coinbene
from services.coinw import coinw
from services.huobi import huobi
from services.bitz import bitz

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

def get_depth(dex, symbol):

    depth = {}

    try:
        if dex == 'jccdex':
            depth, _ = jccdex.get_depth(symbol)

        if dex == 'coinbene':
            depth = coinbene.get_depth(symbol)

        if dex == 'coinw':
            depth = coinw.get_depth(symbol)

        if dex == 'huobi':
            depth, _ = huobi.get_depth(symbol)

        if dex == 'bitz':
            depth, _ = bitz.get_depth(symbol)

    except:
        pass

    return depth

def bilateral_depth(a_dex, b_dex, a_symbol, b_symbol):

    a = get_depth(a_dex, a_symbol)
    b = get_depth(b_dex, b_symbol)

    if 'bids' not in a or 'bids' not in b or 'asks' not in a or 'asks' not in b:
        return False

    if len(a.get('bids')) == 0 or len(a.get('asks')) == 0 or len(b.get('bids')) == 0 or len(b.get('asks')) == 0:
        return False

    a_bid_price     = a.get('bids')[0]['price']
    a_bid_amount    = a.get('bids')[0]['amount']
    b_bid_price     = b.get('bids')[0]['price']
    b_bid_amount    = b.get('bids')[0]['amount']
    a_ask_price     = a.get('asks')[0]['price']
    a_ask_amount    = a.get('asks')[0]['amount']
    b_ask_price     = b.get('asks')[0]['price']
    b_ask_amount    = b.get('asks')[0]['amount']

    amount1 = min([a_ask_amount, b_bid_amount])
    amount2 = min([a_bid_amount, b_ask_amount])

    a_coins = a_symbol.split('/')
    b_coins = b_symbol.split('/')

    if a_coins[0] in ['xrp', 'eth', 'moac']:
    # if a_coins[0] in ['xrp']:
        return False

    if a_coins[1] == 'cnyt':
        a_otc_sell = 1
        a_otc_buy = 1
    else:
        a_otc_sell = float(rdb.hget('otc', a_coins[1] + '_sell'))
        a_otc_buy = float(rdb.hget('otc',  a_coins[1] + '_buy'))


    if b_coins[1] == 'cnyt':
        b_otc_sell = 1
        b_otc_buy = 1
    else:
        b_otc_sell = float(rdb.hget('otc', b_coins[1] + '_sell'))
        b_otc_buy = float(rdb.hget('otc', b_coins[1] + '_buy'))

    a_bid_price_cnyt = round(a_bid_price * a_otc_buy, 4) # 转成cnyt价格
    a_ask_price_cnyt = round(a_ask_price * a_otc_sell, 4) # 转成cnyt价格

    b_bid_price_cnyt = round(b_bid_price * b_otc_buy, 4) # 转成cnyt价格
    b_ask_price_cnyt = round(b_ask_price * b_otc_sell, 4) # 转成cnyt价格

    return [a_bid_price_cnyt, a_ask_price_cnyt, b_bid_price_cnyt, b_ask_price_cnyt, amount1, amount2, a_bid_price, a_ask_price, b_bid_price, b_ask_price]

def bilateral(a_dex, b_dex, a_symbol, b_symbol):

    depth = bilateral_depth(a_dex, b_dex, a_symbol, b_symbol)

    if not depth:
        return False

    if a_dex == 'jccdex':
        a_fee = 0
    else:
        a_fee = 0.002

    if b_dex == 'jccdex':
        b_fee = 0
    else:
        b_fee = 0.002

    buy = depth[1]
    sell = depth[2]
    buy_ = depth[7]
    sell_ = depth[8]
    amount = depth[4]
    cost = round(buy * amount * (1 + a_fee), 4)
    earn = round(sell * amount * (1 - b_fee), 4)
    profit = round(earn - cost, 4)

    # if profit != 0:
    #     rate = round(profit / cost * 100, 2)
    #     log = '%s(%s) --> %s(%s) 买:%s 卖:%s 数量:%s 成本:%s 利润:%s 利润率:%s' % (a_dex, a_symbol, b_dex, b_symbol, buy, sell, amount, cost, profit, str(rate) + '%')
    #     print(time.strftime("%Y-%m-%d %H:%M:%S"), log)
    #     print(depth)

    if profit > 1:
        rate = round(profit / cost * 100, 2)
        if rate > 1:
            log = '%s(%s) --> %s(%s) 买:%s 卖:%s 数量:%s 成本:%s 利润:%s 利润率:%s' % (a_dex, a_symbol, b_dex, b_symbol, buy, sell, amount, cost, profit, str(rate) + '%')
            print(time.strftime("%Y-%m-%d %H:%M:%S"), log)
            # print(depth)
            doing(a_dex, b_dex, a_symbol, b_symbol, buy_, sell_, amount)
            save(a_dex, b_dex, a_symbol, b_symbol, buy, sell, rate, amount, cost, profit)

    buy = depth[3]
    sell = depth[0]
    buy_ = depth[9]
    sell_ = depth[6]
    amount = depth[5]
    cost = round(buy * amount * (1 + b_fee), 4)
    earn = round(sell * amount * (1 - a_fee), 4)
    profit = round(earn - cost, 4)

    # if profit != 0:
    #     rate = round(profit / cost * 100, 2)
    #     log = '%s(%s) --> %s(%s) 买:%s 卖:%s 数量:%s 成本:%s 利润:%s 利润率:%s' % (b_dex, b_symbol, a_dex, a_symbol, buy, sell, amount, cost, profit, str(rate) + '%')
    #     print(time.strftime("%Y-%m-%d %H:%M:%S"), log)
    #     print(depth)

    if profit > 1:
        rate = round(profit / cost * 100, 2)
        if rate > 1:
            log = '%s(%s) --> %s(%s) 买:%s 卖:%s 数量:%s 成本:%s 利润:%s 利润率:%s' % (b_dex, b_symbol, a_dex, a_symbol, buy, sell, amount, cost, profit, str(rate) + '%')
            print(time.strftime("%Y-%m-%d %H:%M:%S"), log)
            # print(depth)
            doing(b_dex, a_dex, b_symbol, a_symbol, buy_, sell_, amount)
            save(b_dex, a_dex, b_symbol, a_symbol, buy, sell, rate, amount, cost, profit)

def doing(a_dex, b_dex, a_symbol, b_symbol, buy, sell, amount):
    # print(a_dex, b_dex, a_symbol, b_symbol, buy, sell, amount)
    ret = order(a_dex, 'buy', a_symbol, buy, amount)
    if ret['code'] == 200:
        order(b_dex, 'sell', b_symbol, sell, amount)

def order(dex, type, symbol, price, amount):
    # return {'code' : 400}
    if dex == 'jccdex':
        return jccdex.order(type, symbol, price, amount)
    elif dex == 'coinw':
        return coinw.order(type, symbol, price, amount)
    elif dex == 'coinbene':
        return coinbene.order(type, symbol, price, amount)
    else:
        return {'code' : 400}

def save(a_dex, b_dex, a_symbol, b_symbol, buy, sell, rate, amount, cost, profit):
    sql = 'INSERT INTO btf (a_dex, b_dex, a_coin, b_coin, buy, sell, rate, amount, cost, profit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    o = [a_dex, b_dex, a_symbol, b_symbol, buy, sell, rate, amount, cost, profit]
    try:
        db.execute(sql, o)
        dbconn.commit()
    except:
        pass

while True:

    print('---------------------------------------- Line')

    data = [
        ('jccdex', jccdex.symbols.keys(), ['cnyt', 'usdt']),
        ('coinw', coinw.symbols.keys(), ['usdt']),
        ('coinbene', coinbene.symbols.keys(), ['usdt']),
        ('bitz', bitz.symbols.keys(), ['usdt']),
        ('huobi', huobi.symbols.keys(), ['usdt']),
    ]

    for i in range(0, len(data)):
        a_dex = data[i][0]
        if a_dex == 'jccdex':
            for j in range(i + 1, len(data)):
                b_dex = data[j][0]
                for a_symbol in data[i][1]:
                    if a_symbol.split('/')[1] in data[i][2]: 
                        for b_symbol in data[j][1]:
                            if b_symbol.split('/')[1] in data[j][2]:
                                if a_symbol.split('/')[0] == b_symbol.split('/')[0]:
                                    bilateral(a_dex, b_dex, a_symbol, b_symbol)
                                    time.sleep(1)
