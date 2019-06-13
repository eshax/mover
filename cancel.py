# -*- coding:utf-8 -*-

import time

from services.jccdex import jccdex

list = jccdex.query()
for item in list:
    jccdex.cancel_order(item['sequence'])
    time.sleep(10)

# list = jccdex.get_balances()
# for k in list:
#     if k == 'exchange' or k == 'SWT' or k == 'CNY':
#         continue
#     coin = k.lower() + '/cnyt'
#     price = float(jccdex.get_last_price(coin))
#     jccdex.order('sell', coin, price, float(list[k]['free']))
#     time.sleep(10)