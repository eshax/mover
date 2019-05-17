# -*- coding:utf-8 -*-

import base64
import datetime
import hashlib
import hmac
import json
import urllib
import urllib2
import requests

ACCESS_KEY = "c663ff43-ecbd2ab6-0cf99e68-12cf0"
SECRET_KEY = "c1e4c567-78cd05ad-7393d405-5ba0c"

MARKET_URL = "https://api.huobi.pro"
TRADE_URL = "https://api.huobi.pro"

class huobi:


    @staticmethod
    def http_get_request(url, params, add_to_headers=None):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        }
        if add_to_headers:
            headers.update(add_to_headers)
        try:
            postdata = urllib.urlencode(params)
            response = requests.get(url, postdata, headers=headers, timeout=5) 
            try:
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return
            except BaseException as e:
                print("httpGet failed, detail is:%s,%s" %(response.text,e))
                return
        except:
            pass


    @staticmethod
    def http_post_request(url, params, add_to_headers=None):
        headers = {
            "Accept": "application/json",
            'Content-Type': 'application/json'
        }
        if add_to_headers:
            headers.update(add_to_headers)
        postdata = json.dumps(params)
        response = requests.post(url, postdata, headers=headers, timeout=10)
        try:
            
            if response.status_code == 200:
                return response.json()
            else:
                return
        except BaseException as e:
            print("httpPost failed, detail is:%s,%s" %(response.text,e))
            return


    @staticmethod
    def api_key_get(params, request_path):
        method = 'GET'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params.update({'AccessKeyId': ACCESS_KEY,
                       'SignatureMethod': 'HmacSHA256',
                       'SignatureVersion': '2',
                       'Timestamp': timestamp})

        host_url = TRADE_URL

        params['Signature'] = huobi.createSign(params, method, 'api.huobi.pro', request_path, SECRET_KEY)

        url = host_url + request_path
        return huobi.http_get_request(url, params)


    @staticmethod
    def api_key_post(params, request_path):
        method = 'POST'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params_to_sign = {'AccessKeyId': ACCESS_KEY,
                          'SignatureMethod': 'HmacSHA256',
                          'SignatureVersion': '2',
                          'Timestamp': timestamp}

        host_url = TRADE_URL

        params_to_sign['Signature'] = huobi.createSign(params_to_sign, method, 'api.huobi.pro', request_path, SECRET_KEY)
        
        url = host_url + request_path + '?' + urllib.urlencode(params_to_sign)
        return huobi.http_post_request(url, params)


    @staticmethod
    def createSign(pParams, method, host_url, request_path, secret_key):
        sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
        encode_params = urllib.urlencode(sorted_params)
        payload = [method, host_url, request_path, encode_params]
        payload = '\n'.join(payload)
        payload = payload.encode(encoding='UTF8')
        secret_key = secret_key.encode(encoding='UTF8')

        digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)
        signature = signature.decode()
        return signature


    @staticmethod
    def get_depth(symbol, type='step1'):
        """
        :param symbol
        :param type: 可选值：{ percent10, step0, step1, step2, step3, step4, step5 }
        :return:
        """
        depth = {"symbol": symbol, "bids": [], "asks": []}
        js = {}
        
        params = {'symbol': huobi.get_symbol(symbol),
                  'type': type}
        
        
        url = MARKET_URL + '/market/depth'

        try:
            js = huobi.http_get_request(url, params)
            if js.has_key('tick'):
                bids = js['tick']['bids']
                bids.sort(key = lambda x: -float(x[0]))
                for b in bids[:5]:
                    depth['bids'].append({ 'price': float(b[0]), 'amount': float(b[1]) })

                asks = js['tick']['asks']
                asks.sort(key = lambda x: float(x[0]))
                for a in asks[:5]:
                    depth['asks'].append({ 'price': float(a[0]), 'amount': float(a[1]) })
        except:
            pass
            
        return depth, js


    @staticmethod
    def get_symbol(symbol):
        symbols = {
            "eth/usdt": "ethusdt",
            "btc/usdt": "btcusdt",
            "ltc/usdt": "ltcusdt",
            "eos/usdt": "eosusdt",
        }
        return symbols.get(symbol)


    @staticmethod
    def get_symbols(long_polling=None):
        params = {}
        if long_polling:
            params['long-polling'] = long_polling
        path = '/v1/common/symbols'
        return huobi.api_key_get(params, path)



if __name__ == '__main__':

    js = huobi.get_symbols()
    
    for o in js['data']:
        if 'eth' in o['symbol']:
            #print o['symbol']
            pass


    js, _ = huobi.get_depth('eth/usdt', 'step0')
    print js


