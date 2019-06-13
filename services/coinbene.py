# -*- coding:utf-8 -*-


'''
满币网接口

https://www.coinbene.vip/#/

https://github.com/Coinbene/API-Documents-CHN/wiki/0.0.0-Coinbene-API%E6%96%87%E6%A1%A3

'''
import sys, os, json, time, requests, hashlib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.md5 import md5
from utils.http import http

class coinbene:

    eth = '0x925c59092c14c9a5bc0e0f869b03b64901169ebc'

    api_url     = 'https://api.coinbene.com'

    api_key     = '24f2cba00fc8a3396210369746863282'
    api_secret  = '7c40000b6ecf48feb753c8956df5ab52'

    header_dict = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",\
        "Content-Type":"application/json;charset=utf-8","Connection":"keep-alive"}

    #  此处为API请求地址及参数
    market_url = "http://api.coinbene.com/v1/market/"
    trade_url = "http://api.coinbene.com/v1/trade/"


    symbols = {
        "btc/usdt"  : "btcusdt",
        "eth/usdt"  : "ethusdt",
        "eos/usdt"  : "eosusdt",
        "bchabc/usdt"  : "bchabcusdt",
        "trx/usdt"  : "trxusdt",
        "xrp/usdt"  : "xrpusdt",
        "ltc/usdt"  : "ltcusdt",
        "neo/usdt"  : "neousdt",
        "etc/usdt"  : "etcusdt",
        "moac/usdt" : "moacusdt",
        "swtc/usdt" : "swtcusdt", 

        "eth/btc"   : "ethbtc",
        "eos/btc"   : "eosbtc",
        "trx/btc"   : "trxbtc",
        "xrp/btc"   : "xrpbtc",
        "ltc/btc"   : "ltcbtc",
        "xmr/btc"   : "xmrbtc",
        "neo/btc"   : "neobtc",
        "etc/btc"   : "etcbtc",
        
    }


    #  生成签名sign
    @staticmethod
    def sign(**kwargs):
        """
        将传入的参数生成列表形式，排序后用＆拼接成字符串，用hashbli加密成生sign
        """
        sign_list = []
        for key, value in kwargs.items():
            sign_list.append("{}={}".format(key, value))
        sign_list.sort()
        sign_str = "&".join(sign_list)
        mysecret = sign_str.upper().encode()
        m = hashlib.md5()
        m.update(mysecret)
        return m.hexdigest()

    #  生成时间戳
    @staticmethod
    def create_timestamp():
        timestamp = int(round(time.time() * 1000))
        return timestamp

    @staticmethod
    def http_post_sign(url,dic):
        mysign = coinbene.sign(**dic)
        del dic['secret']
        dic['sign'] = mysign
        return coinbene.http_request(url,data=dic)

    '''
    翻译货币对
    '''

    @staticmethod
    def get_symbol(symbol):
        return coinbene.symbols.get(symbol)

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



    @staticmethod
    def http_get_nosign(url):
        return coinbene.http_request(url, data=None)



    @staticmethod
    def http_request(url, data) :
        if data == None:
            reponse = requests.get(url,headers=coinbene.header_dict)
        else:
            reponse = requests.post(url,data=json.dumps(data),headers=coinbene.header_dict)
        try:
            if reponse.status_code == 200:
                return json.loads(reponse.text)
            else:
                return None
        except Exception as e:
            print ('http failed : %s' % e)
            return None

    '''
    获取交易深度
    '''

    @staticmethod
    def get_depth(symbol):

        symbol = coinbene.get_symbol(symbol)

        depth = {"bids": [], "asks": [], "symbol": symbol}

        url = coinbene.api_url + "/v1/market/orderbook?symbol=" + str(symbol)
        js = coinbene.http_get_nosign(url)

        if 'orderbook' in js:
            for o in js['orderbook']['bids'][:5]:
                depth['bids'].append({"price": float(o['price']), "amount": float(o['quantity'])})
            for o in js['orderbook']['asks'][:5]:
                depth['asks'].append({"price": float(o['price']), "amount": float(o['quantity'])})

        return depth


    '''
    下单
    '''

    @staticmethod
    def order(type, symbol, price, amount):
        o = {
            "apiid": coinbene.api_key,
            "secret": coinbene.api_secret,
            "timestamp": coinbene.create_timestamp(),
            "type": type + "-limit",
            "price": price,
            "quantity": amount,
            "symbol": coinbene.get_symbol(symbol)
        }
        url = coinbene.trade_url + "order/place"
        try:
            js = coinbene.http_post_sign(url, o)
            print(js)
            if js.get('status') == 'ok':
                return {'code': 200}
            else:
                return {'code': 400}
        except:
            return {'code': 400}


    '''
    查询挂单
    '''

    @staticmethod
    def query(orderid):
        """
        orderid : 订单号
        """
        o = {
            "apiid": coinbene.api_key,
            "secret": coinbene.api_secret,
            'orderid': 'orderid',
            'timestamp': coinbene.create_timestamp()
        }
        url = coinbene.trade_url + "order/info"
        return coinbene.http_post_sign(url, o)



    #  撤单
    def cancel_order(orderid):
        """
        以字典形式传参
        apiid,timestamp,secret,orderid
        """
        o = {
            "apiid": coinbene.api_key,
            "secret": coinbene.api_secret,
            'orderid': 'orderid',
            'timestamp': coinbene.create_timestamp()
        }
        url = coinbene.trade_url + "order/cancel"
        return coinbene.http_post_sign(url, o)


    #  提现
    def withdraw(symbol, amount, wallet):
        """
        以字典形式传参
        apiid,timestamp,secret,orderid
        """
        o = {
            "apiid": coinbene.api_key,
            "secret": coinbene.api_secret,
            'asset': symbol,
            'amount': amount,
            'address': wallet,
            'timestamp': coinbene.create_timestamp()
        }
        url = coinbene.trade_url + "withdraw/apply"
        return coinbene.http_post_sign(url, o)

class triangle:


    '''
    站内三角形, 单边交易
    ['swtc', 'eth', 'cnyt']

    plan A

    buy buy sell

     buy: eth/cnyt      <       1853.20 * 0.01 = 18.532cnyt
     buy: swtc/eth      <
    sell: swtc/cnyt     >

    '''

    @staticmethod
    def buy_buy_sell(symbols, buy_amount, fee):

        data = []
        try:
            for symbol in symbols:
                depth = coinbene.get_depth(symbol)
                if 'asks' not in depth or 'bids' not in depth:
                    print (time.strftime("%Y-%m-%d %H:%M:%S"), '%42s' % symbols, symbol, 'no depth')
                    return False
                if len(depth.get('asks')) == 0 or len(depth.get('bids')) == 0:
                    print (time.strftime("%Y-%m-%d %H:%M:%S"), '%42s' % symbols, symbol, 'depth count is 0')
                    return False
                data.append(depth)
        except:
            print ('error!')
            return False

        prices = [
            data[0].get('asks')[0]['price'],
            data[1].get('asks')[0]['price'],
            data[2].get('bids')[0]['price']
        ]

        amounts = [
            data[0].get('asks')[0]['amount'],
            data[1].get('asks')[0]['amount'],
            data[2].get('bids')[0]['amount']
        ]

        if amounts[0] < buy_amount:
            print (time.strftime("%Y-%m-%d %H:%M:%S"), '%42s' % symbols, '1. ask amount', amounts[0], '<', buy_amount)
            return False

        sell_amount = buy_amount / (prices[1] * 1.01)

        if sell_amount > amounts[1]:
            print (time.strftime("%Y-%m-%d %H:%M:%S"), '%42s' % symbols, '2. ask amount', amounts[1], '<', sell_amount)
            return False

        if sell_amount > amounts[2]:
            print (time.strftime("%Y-%m-%d %H:%M:%S"), '%42s' % symbols, '3. bid amount', amounts[2], '<', sell_amount)
            return False

        # 计算利润
        x = round(buy_amount * prices[0], 2)
        y = round(sell_amount * prices[2], 2)
        z = round(y - x, 2)

        print (time.strftime("%Y-%m-%d %H:%M:%S"), '%42s' % symbols, 'x: %.2f' % x, 'y: %.2f' % y, 'z: %.2f' % z, ('+' if z > 0 else '-'))

        if z < fee:
            return False

        # buy
        o = coinbene.order('buy', symbols[0], prices[0] * 1.01, buy_amount)

        time.sleep(1)

        # buy
        o = coinbene.order('buy', symbols[1], prices[1] * 1.01, sell_amount)

        time.sleep(1)

        # sell
        o = coinbene.order('sell', symbols[2], prices[2] * 0.99, sell_amount)

        # exit()

        time.sleep(10)

        return True


    '''
    站内三角形, 单边交易

    plan B

    buy sell sell

     buy: eth/usdt      <   270.18 * 0.007 = 1.89126
    sell: eth/btc       >   0.031072 * 0.007 = 0.000217504
    sell: btc/usdt      >   8681.76 * 0.000217504 = 1.88831

    '''

    @staticmethod
    def buy_sell_sell(symbols, buy_amount, fee):

        data = []
        try:
            for symbol in symbols:
                depth = coinbene.get_depth(symbol)
                if 'asks' not in depth or 'bids' not in depth:
                    return
                if len(depth.get('asks')) == 0 or len(depth.get('bids')) == 0:
                    return
                data.append(depth)
        except:
            return

        prices = [
            data[0].get('asks')[0]['price'],
            data[1].get('bids')[0]['price'],
            data[2].get('bids')[0]['price']
        ]

        amounts = [
            data[0].get('asks')[0]['amount'],
            data[1].get('bids')[0]['amount'],
            data[2].get('bids')[0]['amount']
        ]

        if amounts[0] < buy_amount:
            # print (time.strftime("%Y-%m-%d %H:%M:%S"), symbols, '1. ask amount', amounts[0], '<', buy_amount)
            return False

        if amounts[1] < buy_amount:
            # print (time.strftime("%Y-%m-%d %H:%M:%S"), symbols, '2. bid amount', amounts[1], '<', buy_amount)
            return False

        sell_amount = buy_amount * (prices[1] * 0.99)

        if sell_amount > amounts[2]:
            # print (time.strftime("%Y-%m-%d %H:%M:%S"), symbols, '3. bid amount', amounts[2], '<', sell_amount)
            return False

        # 计算利润
        x = round(buy_amount * prices[0], 2)
        y = round(sell_amount * prices[2], 2)
        z = round(y - x, 2)

        print (time.strftime("%Y-%m-%d %H:%M:%S"), '%42s' % symbols, 'x: %.2f' % x, 'y: %.2f' % y, 'z: %.2f' % z, ('+' if z > 0 else '-'))

        if z < fee:
            return False

        # buy
        o = coinbene.order('buy', symbols[0], prices[0] * 1.01, buy_amount)

        time.sleep(1)

        # sell
        o = coinbene.order('sell', symbols[1], prices[1] * 0.99, buy_amount)

        time.sleep(1)

        # sell
        o = coinbene.order('sell', symbols[2], prices[2] * 0.99, sell_amount)

        # exit()

        time.sleep(10)

        return True



if __name__ == "__main__":


    while True:

        # print (time.strftime("%Y-%m-%d %H:%M:%S"))

        print ('# buy buy sell')

        triangle.buy_buy_sell(['btc/usdt', 'eth/btc', 'eth/usdt'], 0.0002, 0.4)
        triangle.buy_buy_sell(['btc/usdt', 'eos/btc', 'eos/usdt'], 0.0002, 0.4)
        triangle.buy_buy_sell(['btc/usdt', 'trx/btc', 'trx/usdt'], 0.0002, 0.4)
        triangle.buy_buy_sell(['btc/usdt', 'xrp/btc', 'xrp/usdt'], 0.0002, 0.4)
        triangle.buy_buy_sell(['btc/usdt', 'neo/btc', 'neo/usdt'], 0.0002, 0.4)
        triangle.buy_buy_sell(['btc/usdt', 'ltc/btc', 'ltc/usdt'], 0.0002, 0.4)

        print ('# buy sell sell')

        triangle.buy_sell_sell(['eth/usdt', 'eth/btc', 'btc/usdt'], 0.007, 0.4)
        triangle.buy_sell_sell(['eos/usdt', 'eos/btc', 'btc/usdt'], 0.25, 0.4)
        triangle.buy_sell_sell(['trx/usdt', 'trx/btc', 'btc/usdt'], 5.8, 0.4)
        triangle.buy_sell_sell(['xrp/usdt', 'xrp/btc', 'btc/usdt'], 4.5, 0.4)
        triangle.buy_sell_sell(['neo/usdt', 'neo/btc', 'btc/usdt'], 0.16, 0.4)
        triangle.buy_sell_sell(['ltc/usdt', 'ltc/btc', 'btc/usdt'], 0.018, 0.4)

        time.sleep(2)
