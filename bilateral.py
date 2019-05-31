# -*- coding:utf-8 -*-

import time

from services.jccdex import jccdex
from services.coinbene import coinbene
from services.coinw import coinw
from services.huobi import huobi
from services.bitz import bitz

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



def bilateral_depth(a_dex, b_dex, symbol):

    a = get_depth(a_dex, symbol)
    b = get_depth(b_dex, symbol)

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

    return [a_bid_price, a_bid_amount, a_ask_price, a_ask_amount, b_bid_price, b_bid_amount, b_ask_price, b_ask_amount]



def bilateral(a_dex, b_dex, symbol, amount):

    depth = bilateral_depth(a_dex, b_dex, symbol)

    if not depth:
        return False

    if amount < depth[3] and amount < depth[5]:
        bp = depth[2]
        sp = depth[4]
        x = (sp - bp) / bp
        ma = min(depth[3], depth[5])            # 盘口最小挂单
        y = round((sp * ma) - (bp * ma), 2)     # 盘口利润
        # x = (sp - bp) / ((sp + bp) / 2)
        print (time.strftime("%Y-%m-%d %H:%M:%S"), 'buy-sell    ', '%20s' % ('%s-%s' % (a_dex, b_dex)), '%14s' % symbol, '%10s' % round(bp, 5), '%10s' % round(sp, 5), '%10s' % round(ma, 5), '%10s' % y, '%10s' % ('%.2f%%' % (x * 100.0)), '+' if x > 0.01 else '')
        if (sp - bp) / ((sp + bp) / 2) > 0.01:
            pass
            # order(a_dex, 'buy', symbol, buy_price, amount)
            # order(b_dex, 'sell', symbol, sell_price, amount)

    if amount < depth[7] and amount < depth[1]:
        bp = depth[6]
        sp = depth[0]
        x = (sp - bp) / bp
        ma = min(depth[7], depth[1])            # 盘口最小挂单
        y = round((sp * ma) - (bp * ma), 2)     # 盘口利润
        # x = (sp - bp) / ((sp + bp) / 2)
        print (time.strftime("%Y-%m-%d %H:%M:%S"), '    sell-buy', '%20s' % ('%s-%s' % (a_dex, b_dex)), '%14s' % symbol, '%10s' % round(sp, 5), '%10s' % round(bp, 5), '%10s' % round(ma, 5), '%10s' % y, '%10s' % ('%.2f%%' % (x * 100.0)), '+' if x > 0.01 else '')
        if (sp - bp) / ((sp + bp) / 2) > 0.01:
            pass
            # order(b_dex, 'buy', symbol, buy_price, amount)
            # order(a_dex, 'sell', symbol, sell_price, amount)


while True:

    print('---------------------------------------- Line')

    data = [
        ('jccdex', jccdex.symbols.keys()),
        ('coinw', coinw.symbols.keys()),
        ('coinbene', coinbene.symbols.keys()),
        ('bitz', bitz.symbols.keys()),
        ('huobi', huobi.symbols.keys()),
    ]

    data = [(x, y, a, b) for x, a in data for y, b in data if y > x]

    for x, y, a, b in data:
    	for c in (a & b):
            bilateral(x, y, c, 0)
            print()
            time.sleep(1)
