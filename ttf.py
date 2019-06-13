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



def triangle_depth(dex, a_symbol, b_symbol, c_symbol, type):

    a = get_depth(dex, a_symbol)
    b = get_depth(dex, b_symbol)
    c = get_depth(dex, c_symbol)

    if 'bids' not in a or 'bids' not in b or 'bids' not in c or 'asks' not in a or 'asks' not in b or 'asks' not in c:
        return False

    if len(a.get('bids')) == 0 or len(a.get('asks')) == 0 or len(b.get('bids')) == 0 or len(b.get('asks')) == 0 or len(c.get('bids')) == 0 or len(c.get('asks')) == 0:
        return False

    a_bid_price     = a.get('bids')[0]['price']
    a_bid_amount    = a.get('bids')[0]['amount']
    b_bid_price     = b.get('bids')[0]['price']
    b_bid_amount    = b.get('bids')[0]['amount']
    c_bid_price     = c.get('bids')[0]['price']
    c_bid_amount    = c.get('bids')[0]['amount']
    a_ask_price     = a.get('asks')[0]['price']
    a_ask_amount    = a.get('asks')[0]['amount']
    b_ask_price     = b.get('asks')[0]['price']
    b_ask_amount    = b.get('asks')[0]['amount']
    c_ask_price     = c.get('asks')[0]['price']
    c_ask_amount    = c.get('asks')[0]['amount']

    if type == 'bbs':
        return [a_ask_price, a_ask_amount, b_ask_price, b_ask_amount, c_bid_price, c_bid_amount]
    else:
        return [a_ask_price, a_ask_amount, b_bid_price, b_bid_amount, c_bid_price, c_bid_amount]


def triangle(dex, a_symbol, b_symbol, c_symbol, type):

    depth = triangle_depth(dex, a_symbol, b_symbol, c_symbol, type)

    if not depth:
        return False

    if dex == 'jccdex':
        fee = 0
    else:
        fee = 0.002

    step1_price = depth[0]
    step2_price = depth[2]
    step3_price = depth[4]

    if (type == 'bbs'):
        amount = min(depth[1] / step2_price, depth[3], depth[5])
        step1_amount = amount * step2_price 
        step2_amount = amount
        step3_amount = amount
        cost = round(step1_amount * step1_price, 4)
        earn = round(amount * step3_price, 4)

    else:
        amount = min(depth[1], depth[3], depth[5] / step2_price)
        step1_amount = amount
        step2_amount = amount
        step3_amount = amount * step2_price 
        cost = round(amount * step1_price, 4)
        earn = round(step3_amount * step3_price, 4)

    profit = round(earn - cost, 4)

    if profit != 0:
        rate = round(profit / cost * 100, 2)
        log = '(%s) %s %s -> %s -> %s 成本:%s 利润:%s 利润率:%s %s' % (dex, type, a_symbol, b_symbol, c_symbol, cost, profit, str(rate) + '%', ('* * * *' if profit > 0 else ''))
        print(time.strftime("%Y-%m-%d %H:%M:%S"), log)

    if profit > 1:
        rate = round(profit / cost * 100, 2)
        if rate > 1:
            # log = '(%s) %s %s -> %s -> %s 成本:%s 利润:%s 利润率:%s' % (dex, type, a_symbol, b_symbol, c_symbol, cost, profit, str(rate) + '%')
            # print(time.strftime("%Y-%m-%d %H:%M:%S"), log)
            # print(depth)
            doing(dex, type, a_symbol, step1_price, step1_amount, b_symbol, step2_price, step2_amount, c_symbol, step3_price, step3_amount, cost, profit, rate)
            save(dex, type, a_symbol, step1_price, step1_amount, b_symbol, step2_price, step2_amount, c_symbol, step3_price, step3_amount, cost, profit, rate)

def doing(dex, type, a_coin, a_price, a_amount, b_coin, b_price, b_amount, c_coin, c_price, c_amount, cost, profit, rate):
    ret1 = order(dex, 'buy', a_coin, a_price, a_amount)
    ret2 = {'code': 404}

    if (type == 'bbs'):
        if ret1['code'] == 200:
            ret2 = order(dex, 'buy', b_coin, b_price, b_amount)
    else:
        if ret1['code'] == 200:
            ret2 = order(dex, 'sell', b_coin, b_price, b_amount)

    if ret2['code'] == 200:
        order(dex, 'sell', c_coin, c_price, c_amount)


def save(dex, type, a_coin, a_price, a_amount, b_coin, b_price, b_amount, c_coin, c_price, c_amount, cost, profit, rate):
    sql = 'INSERT INTO ttf (dex, type, a_coin, a_price, a_amount, b_coin, b_price, b_amount, c_coin, c_price, c_amount, cost, profit, rate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    o = [dex, type, a_coin, a_price, a_amount, b_coin, b_price, b_amount, c_coin, c_price, c_amount, cost, profit, rate]
    try:
        db.execute(sql, o)
        dbconn.commit()
    except:
        pass

def order(dex, type, symbol, price, amount):
    if dex == 'jccdex':
        ret = jccdex.order(type, symbol, price, amount)
        time.sleep(10)
        return ret
    elif dex == 'coinw':
        return coinw.order(type, symbol, price, amount)
    elif dex == 'coinbene':
        return coinbene.order(type, symbol, price, amount)
    else:
        return {'code' : 400}

while True:

    print('---------------------------------------- Line')

    data = [
        ('jccdex', jccdex.symbols.keys(), 'cnyt'),
        ('coinw', coinw.symbols.keys(), 'cnyt'),
        ('coinbene', coinbene.symbols.keys(), 'usdt'),
        ('bitz', bitz.symbols.keys(), 'usdt'),
        ('huobi', huobi.symbols.keys(), 'usdt'),
    ]

    for item in data:
        # if item[0] == 'jccdex':
        for a_symbol in item[1]:
            if a_symbol.split('/')[1] == item[2]:
                for b_symbol in item[1]:
                    if a_symbol != b_symbol:
                        if a_symbol.split('/')[0] == b_symbol.split('/')[1]:
                            c_symbol = b_symbol.split('/')[0] + '/' +item[2]
                            triangle(item[0], a_symbol, b_symbol, c_symbol, 'bbs')
                            time.sleep(1)
                            continue
                        elif a_symbol.split('/')[0] == b_symbol.split('/')[0]:
                            c_symbol = b_symbol.split('/')[1] + '/' +item[2]
                            triangle(item[0], a_symbol, b_symbol, c_symbol, 'bss')
                            time.sleep(1)
