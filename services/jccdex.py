# -*- coding:utf-8 -*-

import os, sys, time, json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.http import http

import jingtumsdk

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

class jccdex:


    info_api = 'https://i3b44eb75ef.jccdex.cn'
    ex_api = 'https://ewdjbbl8jgf.jccdex.cn'
    
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
    挂单
    '''
    
    @staticmethod
    def order():

        try:
        
            account = "jaSmctLLJhTaYbPA2bFxU9T5AFrroZFWQ3"
            symbol = 'SWT-CNY'
            symbols = symbol.split('-')
            order_type = 'buy'
            order_price = '0.005'
            order_amount = 1000
            
            if order_type == "buy":
                order_get_cny = symbols[0]
                order_get_val = str(float(order_price) * float(order_amount))
                order_pay_cny = symbols[1]
                order_pay_val = str(float(order_price))
                
            else:
                order_get_cny = symbols[1]
                order_get_val = str(float(order_price))
                order_pay_cny = symbols[0]
                order_pay_val = str(float(order_price) * float(order_amount))
                
            order_issuer = "jGa9J9TkqtBcUoHe2zqhVFFbgUVED6o9or"
            
            secret = "ssbczL7WYpmG1mP1xPZsjDkWi6J6H"

            o = {
                "Flags": 0,
                "TransactionType": "OfferCreate",
                "Account": account,
                "TakerPays": {
                    "value": order_pay_val,
                    "currency": order_pay_cny,
                    "issuer": order_issuer
                },
                "TakerGets": {
                    "value": order_get_val,
                    "currency": order_get_cny,
                    "issuer": order_issuer
                }
            }
                        
            o['sign'] = jingtumsdk.sign.signature_for_transaction(o, secret)
            
            url = jccdex.ex_api + '/exchange/sign_order'
        
            print o
        
            code, js = http.post(url, data = o )

            print code
            print json.loads(js)
            print json.loads(js).get('msg')
            
        except BaseException as e:
            print e
        
        


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
            
            if js.has_key("data"):
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

        #o, _ = jccdex.get_depth('jcc/cnyt')
        #print o
        
        #js = jccdex.get_balances()
        #print js

        #js = jccdex.get_tx()
        #print js
        
        jccdex.order()
        
        print 
        
        break

