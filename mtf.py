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


def bilateral_depth(a_dex, b_dex, c_dex, a_symbol, b_symbol, c_symbol):

    a = get_depth(a_dex, a_symbol)
    b = get_depth(b_dex, b_symbol)
    c = get_depth(c_dex, c_symbol)

    if 'bids' not in a or 'bids' not in b or 'bids' not in c or 'asks' not in a or 'asks' not in b or 'asks' not in c:
        return False

    if len(a.get('bids')) == 0 or len(a.get('asks')) == 0 or len(b.get('bids')) == 0 or len(b.get('asks')) == 0 or len(c.get('bids')) == 0 or len(c.get('asks')) == 0:
        return False

    c_bid_price = c.get('bids')[0]['price']
    c_ask_price = c.get('asks')[0]['price']

    a_bid_price = a.get('bids')[0]['price']
    a_bid_amount = a.get('bids')[0]['amount']

    b_bid_price = b.get('bids')[0]['price']
    b_bid_amount = b.get('bids')[0]['amount']

    a_ask_price = a.get('asks')[0]['price']
    a_ask_amount = a.get('asks')[0]['amount']

    b_ask_price = b.get('asks')[0]['price']
    b_ask_amount = b.get('asks')[0]['amount']

    amount1 = min([a_ask_amount, b_bid_amount])
    amount2 = min([a_bid_amount, b_ask_amount])

    a = b_bid_price * c_bid_price
    b = b_ask_price * c_ask_price

    if b_dex == 'coinbene':
        rate1 = 7.06
        rate2 = 7.08
    else:
        rate1 = 7.06
        rate2 = 7.07

    # rate1 otc 卖出usdt价格
    # rate2 otc 买入usdt价格
    #其他币种可以用usdt兑换出cnyt价格
    

    aa = b_bid_price * rate1 # 转成cnyt价格
    bb = b_ask_price * rate2 # 转成cnyt价格

    return [a_bid_price, a_ask_price, b_bid_price, b_ask_price, c_bid_price, c_ask_price, amount1, amount2, a, b, aa, bb]

def bilateral(a_dex, b_dex, c_dex, a_symbol, b_symbol, c_symbol):

    depth = bilateral_depth(a_dex, b_dex, c_dex, a_symbol, b_symbol, c_symbol)
    if depth == False:
        return depth

    buy = depth[1]
    sell = depth[10]
    amount = depth[6]
    fee = 0.002 #交易费
    profit = (sell * amount * (1 - fee)) - (buy * amount)
    exchange = '%s(buy) --> %s(sell)' % (a_dex, b_dex)
    coin = '%s ===> %s' % (a_symbol, b_symbol)
    if profit > 0:
        # print(depth)
        print(time.strftime("%Y-%m-%d %H:%M:%S"), exchange, coin, '(买)', buy, '(卖)', sell, '(数量)', amount, '(利润)', profit)
    else:
        pass

    buy = depth[11]
    sell = depth[0]
    amount = depth[7]
    fee = 0.002 #交易费
    profit = (sell * amount) - (buy * amount * (1 + fee))
    exchange = '%s(buy) --> %s(sell)' % (b_dex, a_dex)
    coin = '%s ===> %s' % (b_symbol, a_symbol)

    if profit > 0:
        # print(depth)
        print(time.strftime("%Y-%m-%d %H:%M:%S"), exchange, coin, '(买)', buy, '(卖)', sell, '(数量)', amount, '(利润)', profit)
    else:
        pass



while True:

    # print('---------------------------------------- Line')

    bilateral('jccdex', 'coinbene', 'jccdex', 'moac/cnyt', 'moac/usdt', 'usdt/cnyt')
    bilateral('jccdex', 'coinbene', 'jccdex', 'swtc/cnyt', 'swtc/usdt', 'usdt/cnyt')
    bilateral('jccdex', 'coinbene', 'jccdex', 'eth/cnyt', 'eth/usdt', 'usdt/cnyt')
    bilateral('jccdex', 'coinbene', 'jccdex', 'xrp/cnyt', 'xrp/usdt', 'usdt/cnyt')

    bilateral('jccdex', 'huobi', 'jccdex', 'eth/cnyt', 'eth/usdt', 'usdt/cnyt')
    bilateral('jccdex', 'huobi', 'jccdex', 'xrp/cnyt', 'xrp/usdt', 'usdt/cnyt')

    bilateral('jccdex', 'coinw', 'jccdex', 'eth/cnyt', 'eth/usdt', 'usdt/cnyt')
    bilateral('jccdex', 'coinw', 'jccdex', 'xrp/cnyt', 'xrp/usdt', 'usdt/cnyt')

    bilateral('jccdex', 'bitz', 'jccdex', 'eth/cnyt', 'eth/usdt', 'usdt/cnyt')
    bilateral('jccdex', 'bitz', 'jccdex', 'xrp/cnyt', 'xrp/usdt', 'usdt/cnyt')


    time.sleep(1)
