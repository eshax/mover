# -*- coding:utf-8 -*-

import time

from services.jccdex import jccdex


prices = {}

'''
查询最新的价格
'''
def get_last_price(dex, symbol):

    if dex == 'jccdex':
        return jccdex.get_last_price(symbol)

    return None


'''
下单
'''
def order(dex, symbol, price, point, amount):

    buy = price - point
    sell = price + point

    print (time.strftime("%Y-%m-%d %H:%M:%S"), dex, symbol, 'price', price)
    print (time.strftime("%Y-%m-%d %H:%M:%S"), dex, symbol, 'buy  ', buy, amount)
    print (time.strftime("%Y-%m-%d %H:%M:%S"), dex, symbol, 'sell ', sell, amount)

    sequence = jccdex.get_sequence()

    # buy
    while True:
        try:
            o = jccdex.order('buy', symbol, buy, amount, sequence)
            if o.get('code') == 200:
                break
        except:
            pass
        time.sleep(1)

    # get sequence
    while True:
        try:
            _sequence = jccdex.get_sequence()
            if sequence == _sequence:
                continue
            else:
                sequence = _sequence
                break
        except:
            pass
        time.sleep(1)

    # sell
    while True:
        try:
            o = jccdex.order('sell', symbol, sell, amount, sequence)
            if o.get('code') == 200:
                break
        except:
            pass
        time.sleep(1)

    print ()


'''
剥头皮
'''
def scalp(dex, symbol, point, amount):

    price = get_last_price(dex, symbol)

    if not price:
        return

    price = float(price)

    if symbol not in prices:
        prices[symbol] = 0.0

    if price > (prices[symbol] + point) or price < (prices[symbol] - point):
        order(dex, symbol, price, point, amount)
        prices[symbol] = price

        time.sleep(10)



while True:

    try:
        scalp('jccdex', 'swtc/cnyt', 0.00001, 10)
    except:
        time.sleep(60)
        
    time.sleep(1)
