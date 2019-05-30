# -*- coding:utf-8 -*-


'''
Bit-Z接口

https://www.bitz.top

https://apidoc.bitz.top/cn/market-quotation-data/Get-ticker-data.html

'''
import sys, os, json, time, requests, hashlib, random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.md5 import md5
from utils.http import http

class bitz:

    api = [
        # 'https://apiv2.bitz.com',
        'https://apiv2.bit-z.pro',
        'https://api.bitzapi.com',
        'https://api.bitzoverseas.com',
        'https://api.bitzspeed.com',
    ]

    api_key = '42eb6798b7be92da77bd262df0ddbcda'
    api_secret = 'eVK0cxcMJjHPM3H2nWUShfozmoAtYTkx5U98JdeQRVRS507KhgSk4rfH6UnGtZZi'

    header = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}

    symbols = {
        "btc/usdt"  : "btc_usdt",
        "eth/usdt"  : "eth_usdt",
        "eos/usdt"  : "eos_usdt",
        "trx/usdt"  : "trx_usdt",
        "xrp/usdt"  : "xrp_usdt",
        "ltc/usdt"  : "ltc_usdt",
        "bchabc/usdt"  : "bchabc_usdt",
        "neo/usdt"  : "neo_usdt",
        "bnb/usdt"  : "bnb_usdt",

        "moac/eth" : "moac_eth",
        "swtc/eth" : "swtc_eth",
        "trx/eth" : "trx_eth", 

        "eth/btc"  : "eth_btc",
        "eos/btc"  : "eos_btc",
        "ltc/btc"  : "ltc_btc",
        "dash/btc"  : "dash_btc",
        "bnb/btc"  : "bnb_btc",
    }

    '''
    翻译货币对
    '''

    @staticmethod
    def get_symbol(symbol):
        return bitz.symbols.get(symbol)

    '''
    Post接口请求
    '''

    @staticmethod
    def post(path, param):
        code, content = http.post( random.choice(bitz.api) + path, param, bitz.header)

        if code == 200:
            return content

    '''
    Get接口请求
    '''

    @staticmethod
    def get(path):
        code, content = http.get( random.choice(bitz.api) + path, bitz.header)

        if code == 200:
            return json.loads(content)
        return None



    '''
    获取交易深度
    '''

    @staticmethod
    def get_depth(symbol):

        symbol = bitz.get_symbol(symbol)

        path = '/Market/depth?symbol=' + str(symbol)
        js = bitz.get(path)
        depth = {"bids": [], "asks": [], "symbol": symbol}

        if 'data' in js:
            for o in js['data']['bids'][:5]:
                depth['bids'].append({"price": float(o[0]), "amount": float(o[1])})
            for o in js['data']['asks'][:5]:
                depth['asks'].append({"price": float(o[0]), "amount": float(o[1])})

        return depth




if __name__ == "__main__":

    bitz.get_depth('moac/eth')

       
