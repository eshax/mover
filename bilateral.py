# -*- coding:utf-8 -*-

import time

from services.jccdex import jccdex
from services.coinbene import coinbene
from services.coinw import coinw



def get_depth(dex, symbol):

    depth = {}

    if dex == 'jccdex':
        depth, _ = jccdex.get_depth(symbol)

    if dex == 'coinbene':
        depth = coinbene.get_depth(symbol)

    if dex == 'coinw':
        depth = coinw.get_depth(symbol)

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
        x = (sp - bp) / ((sp + bp) / 2)
        print (time.strftime("%Y-%m-%d %H:%M:%S"), 'buy-sell', '%s-%s' % (a_dex, b_dex), symbol, bp, sp, '%.2f' % x, '+' if x > 0.01 else '')
        if (sp - bp) / ((sp + bp) / 2) > 0.01:
            pass
            # order(a_dex, 'buy', symbol, buy_price, amount)
            # order(b_dex, 'sell', symbol, sell_price, amount)
    # else:
    #     print (time.strftime("%Y-%m-%d %H:%M:%S"), 'buy-sell', '%s-%s' % (a_dex, b_dex), symbol, 'low on amount', amount, '>', depth[3], '|', depth[5])

    if amount < depth[7] and amount < depth[1]:
        bp = depth[6]
        sp = depth[0]
        x = (sp - bp) / ((sp + bp) / 2)
        print (time.strftime("%Y-%m-%d %H:%M:%S"), 'sell-buy', '%s-%s' % (a_dex, b_dex), symbol, sp, bp, '%.2f' % x, '+' if x > 0.01 else '')
        if (sp - bp) / ((sp + bp) / 2) > 0.01:
            pass
            # order(b_dex, 'buy', symbol, buy_price, amount)
            # order(a_dex, 'sell', symbol, sell_price, amount)
    # else:
    #     print (time.strftime("%Y-%m-%d %H:%M:%S"), 'sell-buy', '%s-%s' % (a_dex, b_dex), symbol, 'low amount', amount, '>', depth[7], '|', depth[1])


while True:

    bilateral('jccdex', 'coinbene', 'eth/usdt', 0)
    bilateral('jccdex', 'coinbene', 'moac/usdt', 0)
    bilateral('jccdex', 'coinbene', 'swtc/usdt', 0)
    bilateral('jccdex', 'coinbene', 'xrp/usdt', 0)

    bilateral('jccdex', 'coinw', 'moac/cnyt', 0)
    bilateral('jccdex', 'coinw', 'swtc/cnyt', 0)
    bilateral('jccdex', 'coinw', 'eth/cnyt', 0)
    bilateral('jccdex', 'coinw', 'eth/usdt', 0)
    bilateral('jccdex', 'coinw', 'xrp/cnyt', 0)
    bilateral('jccdex', 'coinw', 'xrp/usdt', 0)


    bilateral('coinw', 'coinbene', 'eth/usdt', 0)
    bilateral('coinw', 'coinbene', 'xrp/usdt', 0)
    bilateral('coinw', 'coinbene', 'eos/usdt', 0)
    bilateral('coinw', 'coinbene', 'btc/usdt', 0)
    bilateral('coinw', 'coinbene', 'bchabc/usdt', 0)

    time.sleep(1)
