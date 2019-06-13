# -*- coding:utf-8 -*-

'''
威链充值到各交易所
'''

import os, sys, time, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.jccdex import jccdex
from services.coinbene import coinbene
from services.coinw import coinw
from services.huobi import huobi
from services.bitz import bitz

class recharge:

    dexs = ['coinw', 'coinbene']

    def run():
        balance = jccdex.get_balances()
        for dex in recharge.dexs:
            if dex == 'coinw':
                eth = coinw.eth
            elif dex == 'coinbene':
                eth = coinbene.eth
        depth, _ = jccdex.get_depth('eth/cnyt')
        print(depth.get('bids')[0])
        print(depth.get('asks')[0])
        

if __name__ == "__main__":

    recharge.run()

