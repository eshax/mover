# -*- coding:utf-8 -*-

'''
各交易所提现到威链
'''

import os, sys, time, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.jccdex import jccdex
from services.coinbene import coinbene
from services.coinw import coinw
from services.huobi import huobi
from services.bitz import bitz

class withdraw:

    dexs = ['coinw']
    coins = ['eth', 'moac', 'swtc']

    def run():
        for dex in withdraw.dexs:
            if dex == 'coinw':
                balance = coinw.get_account()
            elif dex == 'coinbene':
                balance = coinbene.get_account() 

            for coin in balance:
                if coin.lower() in withdraw.coins:
                    if dex == 'coinw':
                        coinw.withdraw(coin.lower(), balance[coin]['free'], jccdex.tokens[coin])
                    elif dex == 'coinbene':
                        coinbene.withdraw(coin, balance[coin]['free'], jccdex.tokens[coin])


if __name__ == "__main__":

    withdraw.run()

