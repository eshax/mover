# -*- coding:utf-8 -*-

import time

from services.jccdex import triangle as jt
from services.coinbene import triangle as ct

def jccdex_triangle():

    print('# [jccdex] buy buy sell')

    jt.buy_buy_sell(['eth/cnyt', 'swtc/eth', 'swtc/cnyt'], 0.02)
    jt.buy_buy_sell(['eth/cnyt', 'moac/eth', 'moac/cnyt'], 0.02)
    jt.buy_buy_sell(['usdt/cnyt', 'eth/usdt', 'eth/cnyt'], 4)
    jt.buy_buy_sell(['swtc/cnyt', 'moac/swtc', 'moac/cnyt'], 3000)
    jt.buy_buy_sell(['swtc/cnyt', 'jcc/swtc', 'jcc/cnyt'], 3000)
    jt.buy_buy_sell(['swtc/cnyt', 'xrp/swtc', 'xrp/cnyt'], 3000)
    jt.buy_buy_sell(['swtc/cnyt', 'csp/swtc', 'csp/cnyt'], 3000)
    jt.buy_buy_sell(['swtc/cnyt', 'call/swtc', 'call/cnyt'], 3000)
    jt.buy_buy_sell(['swtc/cnyt', 'slash/swtc', 'slash/cnyt'], 3000)
    jt.buy_buy_sell(['swtc/cnyt', 'stm/swtc', 'stm/cnyt'], 3000)
    jt.buy_buy_sell(['usdt/cnyt', 'swtc/usdt', 'swtc/cnyt'], 4)
    jt.buy_buy_sell(['usdt/cnyt', 'moac/usdt', 'moac/cnyt'], 4)
    jt.buy_buy_sell(['usdt/cnyt', 'fst/usdt', 'fst/cnyt'], 4)
    jt.buy_buy_sell(['usdt/cnyt', 'xrp/usdt', 'xrp/cnyt'], 4)

    print ('# [jccdex] buy sell sell')

    jt.buy_sell_sell(['swtc/cnyt', 'swtc/eth', 'eth/cnyt'], 3000)
    jt.buy_sell_sell(['moac/cnyt', 'moac/eth', 'eth/cnyt'], 5)
    jt.buy_sell_sell(['eth/cnyt', 'eth/usdt', 'usdt/cnyt'], 0.02)
    jt.buy_sell_sell(['moac/cnyt', 'moac/swtc','swtc/cnyt'], 5)
    jt.buy_sell_sell(['jcc/cnyt', 'jcc/swtc', 'swtc/cnyt'], 100)
    jt.buy_sell_sell(['xrp/cnyt', 'xrp/swtc', 'swtc/cnyt'], 10)
    jt.buy_sell_sell(['csp/cnyt', 'csp/swtc', 'swtc/cnyt'], 500)
    jt.buy_sell_sell(['call/cnyt', 'call/swtc', 'swtc/cnyt'], 3000)
    jt.buy_sell_sell(['slash/cnyt', 'slash/swtc', 'swtc/cnyt'], 3000)
    jt.buy_sell_sell(['swtc/cnyt', 'swtc/usdt', 'usdt/cnyt'], 3000)
    jt.buy_sell_sell(['stm/cnyt', 'stm/swtc', 'swtc/cnyt'], 3000)
    jt.buy_sell_sell(['moac/cnyt', 'moac/usdt', 'usdt/cnyt'], 5)
    jt.buy_sell_sell(['fst/cnyt', 'fst/usdt', 'usdt/cnyt'], 20)
    jt.buy_sell_sell(['xrp/cnyt', 'xrp/usdt', 'usdt/cnyt'], 10)


def coinbene_triangle():

    print ('# [continue] buy buy sell')

    ct.buy_buy_sell(['btc/usdt', 'eth/btc', 'eth/usdt'], 0.0002, 0.4)
    ct.buy_buy_sell(['btc/usdt', 'eos/btc', 'eos/usdt'], 0.0002, 0.4)
    ct.buy_buy_sell(['btc/usdt', 'trx/btc', 'trx/usdt'], 0.0002, 0.4)
    ct.buy_buy_sell(['btc/usdt', 'xrp/btc', 'xrp/usdt'], 0.0002, 0.4)
    ct.buy_buy_sell(['btc/usdt', 'neo/btc', 'neo/usdt'], 0.0002, 0.4)
    ct.buy_buy_sell(['btc/usdt', 'cnn/btc', 'cnn/usdt'], 0.0002, 0.4)
    ct.buy_buy_sell(['btc/usdt', 'ltc/btc', 'ltc/usdt'], 0.0002, 0.4)

    print ('# [continue] buy sell sell')

    ct.buy_sell_sell(['eth/usdt', 'eth/btc', 'btc/usdt'], 0.007, 0.4)
    ct.buy_sell_sell(['eos/usdt', 'eos/btc', 'btc/usdt'], 0.25, 0.4)
    ct.buy_sell_sell(['trx/usdt', 'trx/btc', 'btc/usdt'], 5.8, 0.4)
    ct.buy_sell_sell(['xrp/usdt', 'xrp/btc', 'btc/usdt'], 4.5, 0.4)
    ct.buy_sell_sell(['neo/usdt', 'neo/btc', 'btc/usdt'], 0.16, 0.4)
    ct.buy_sell_sell(['cnn/usdt', 'cnn/btc', 'btc/usdt'], 10000, 0.4)
    ct.buy_sell_sell(['ltc/usdt', 'ltc/btc', 'btc/usdt'], 0.018, 0.4)


while True:

    jccdex_triangle()

    coinbene_triangle()

    time.sleep(1)
