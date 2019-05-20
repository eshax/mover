# -*- coding:utf-8 -*-

import os, sys, time, json, binascii, requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.http import http

from jingtum_python_lib.remote import Remote
from jingtum_python_baselib.wallet import Wallet
from jingtum_python_baselib.serializer import Serializer

'''
威链交易所

api doc:
    https://github.com/JCCDex/jcc_server_doc

tx:
    https://explorec9d536e.jccdex.cn/#/wallet/?wallet=jaSmctLLJhTaYbPA2bFxU9T5AFrroZFWQ3

sign:
    https://github.com/JCCDex/jcc_jingtum_lib

sdk:
    https://github.com/jingtum/jingtum-python-sdk

'''

account = "jaSmctLLJhTaYbPA2bFxU9T5AFrroZFWQ3"
secret  = "ssbczL7WYpmG1mP1xPZsjDkWi6J6H"

class jccdex:


    info_api    = 'https://i3b44eb75ef.jccdex.cn'
    ex_api      = 'https://ewdjbbl8jgf.jccdex.cn'
    account_key = 'jaSmctLLJhTaYbPA2bFxU9T5AFrroZFWQ3'


    '''
    查询 api
    '''

    @staticmethod
    def info(url):

        url = jccdex.info_api + url

        code, content = http.get(url)

        if code == 200:
            return content


    '''
    交易 api
    '''

    @staticmethod
    def exchange(url, data=None):

        url = jccdex.ex_api + url

        if data:
            code, content = http.post(url, data=data)
        else:
            code, content = http.get(url)

        if code == 200:
            return content


    '''
    币种翻译
    '''

    @staticmethod
    def get_symbol(symbol):

        symbols = {
            'moac/cnyt' : 'JMOAC-CNY',

            'eth/cnyt'  : 'JETH-CNY',
            'swtc/cnyt' : 'SWT-CNY',
            'swtc/eth'  : 'SWT-JETH',

            'jcc/cnyt'  : 'JJCC-CNY',
        }

        return symbols.get(symbol)


    '''
    读取帐户余额
    '''

    @staticmethod
    def get_balances():

        url = '/exchange/balances/%s' % jccdex.account_key

        try:

            js = json.loads(jccdex.exchange(url))

        except:
            pass

        return js


    '''
    获取交易序号
    '''

    @staticmethod
    def get_sequence():
        url = jccdex.ex_api + '/exchange/sequence/' + account
        code, js = http.get(url)
        if code == 200:
            js = json.loads(js)
            return js.get('data').get('sequence')


    '''
    挂单
    '''

    @staticmethod
    def order():

        o = {
            "Flags": 0,
            "Fee": 0.00001,
            "Account": jccdex.account_key,
            "TransactionType": 'OfferCreate',
            "TakerGets": {
                "value": 0.005,
                "currency": 'CNY',
                "issuer": 'jGa9J9TkqtBcUoHe2zqhVFFbgUVED6o9or'
            },
            "TakerPays": {
                "value": 1,
                "currency": 'SWT',
                "issuer": "jGa9J9TkqtBcUoHe2zqhVFFbgUVED6o9or"
            }
        }

        w = Wallet(secret)

        o['Sequence'] = jccdex.get_sequence()
        o['SigningPubKey'] = w.get_public_key()
        prefix = 0x53545800
        serial = Serializer(None)
        hash = serial.from_json(o).hash(prefix)
        o['TxnSignature'] = w.sign(hash)

        print(o)
        blob = serial.from_json(o).to_hex()
        print(blob)

        url = jccdex.ex_api + '/exchange/sign_order'

        data = {}
        data['sign'] = blob

        r = requests.post(url, data=data)
        print(r.content)

        js = json.loads(r.content)
        print(js.get('msg'))

        return js.get("hash")


    '''
    读取帐户交易记录
    '''

    @staticmethod
    def get_tx():

        url = '/exchange/tx/%s' % jccdex.account_key

        try:

            js = json.loads(jccdex.exchange(url))

        except:
            pass

        return js


    '''
    读取交易深度
    '''

    @staticmethod
    def get_depth(symbol):

        depth = {"bids": [], "asks": [], "symbol": symbol}
        js = {}

        url = '/info/depth/%s/normal' % jccdex.get_symbol(symbol)

        try:

            js = json.loads(jccdex.info(url))

            if 'data' in js:
                for o in js['data']['bids']:
                    depth['bids'].append({"price": float(o['price']), "amount": float(o['amount'])})
                for o in js['data']['asks']:
                    depth['asks'].append({"price": float(o['price']), "amount": float(o['amount'])})

        except:
            pass

        return depth, js


if __name__ == "__main__":

    pass

    while True:

        time.sleep(1)

        # o, _ = jccdex.get_depth('eth/cnyt')
        # print (o)

        # js = jccdex.get_balances()
        # print (js)

        # js = jccdex.get_tx()
        # print js

        hash = jccdex.order()
        print (hash)

        break
