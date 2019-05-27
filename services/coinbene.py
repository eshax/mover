# -*- coding:utf-8 -*-


'''
满币网接口

'''
import sys, os, json, time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.md5 import md5
from utils.http import http

class coinbene:

    api_url     = 'https://api.coinbene.com'

    api_key     = '24f2cba00fc8a3396210369746863282'
    api_secret  = '7c40000b6ecf48feb753c8956df5ab52'

    '''
    签名
    '''

    @staticmethod
    def get_sign(param = ''):

        if '=' in param:
            param = param.split('&')
        else:
            param = []

        param.append("apiid=%s" % coinbene.api_key)
        secret = "secret=%s" % coinbene.api_secret
        param.append(secret)
        param.append("timestamp=%s" % int(round(time.time() * 1000)))
        list.sort(param)

        sign = '&'.join(param).upper()
        param.append("sign=%s" % md5.encode(sign))

        param.remove(secret)
        data = {}
        for item in param:
            items = item.split('=')
            data[items[0]] = items[1]
        return json.dumps(data)


    '''
    接口请求
    '''

    @staticmethod
    def post(path, param):
        headers = {
            "Content-type": "application/json"
        }
        code, content = http.post( coinbene.api_url + path, coinbene.get_sign(param), headers )

        if code == 200:
            return content



    '''
    查询用户信息
    '''

    @staticmethod
    def get_account():
        data = {'exchange': 'coinbene'}
        param = 'account=exchange'
        path = '/v1/trade/balance'
        js = json.loads(coinbene.post(path, param))
        for item in js.get('balance'):
            if float(item['total']) == 0:
                continue
            else:
               data[item['asset']] = {
                "free": float(item['available']),
                "freezed": float(item['reserved'])
            }

        return data



if __name__ == "__main__":

    # pass

    o = coinbene.get_account()
    print(o)

    # o = json.loads(o)

    # print ('msg:', o.get("msg"))
    # print ()

    # while True:

    #     time.sleep(1)

    #     for a in ['eos/cnyt', 'moac/cnyt']:
    #         o, _ = coinw.get_depth(a)

    #         print (a)
    #         print (o)
    #         print ()

    #     break
