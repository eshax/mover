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

    api_url     = 'https://api.coinbene.com'

    api_key     = '24f2cba00fc8a3396210369746863282'
    api_secret  = '7c40000b6ecf48feb753c8956df5ab52'

    header_dict = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko",\
        "Content-Type":"application/json;charset=utf-8","Connection":"keep-alive"}

    #  此处为API请求地址及参数
    market_url = "http://api.coinbene.com/v1/market/"
    trade_url = "http://api.coinbene.com/v1/trade/"

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

        symbols = {
            "btc/usdt"  : "btcusdt",
            "eth/usdt"  : "ethusdt",
            "eth/btc"   : "ethbtc",
        }

        return symbols.get(symbol)

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
        return coinbene.http_post_sign(url, o)



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
    def buy_buy_sell(symbols, buy_amount):

        data = []
        try:
            for symbol in symbols:
                depth = coinbene.get_depth(symbol)
                if 'asks' not in depth or 'bids' not in depth:
                    return False
                if len(depth.get('asks')) == 0 or len(depth.get('bids')) == 0:
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
            # print (symbols, '1. ask amount', amounts[0], '<', buy_amount)
            return False

        sell_amount = buy_amount / (prices[1] * 1.01)

        if sell_amount > amounts[1]:
            # print (symbols, '2. ask amount', amounts[1], '<', sell_amount)
            return False

        if sell_amount > amounts[2]:
            # print (symbols, '3. bid amount', amounts[2], '<', sell_amount)
            return False

        # 计算利润
        x = round(buy_amount * prices[0], 2)
        y = round(sell_amount * prices[2], 2)
        z = round(y - x, 2)

        print (time.strftime("%Y-%m-%d %H:%M:%S"), '%42s' % symbols, 'x: %.2f' % x, 'y: %.2f' % y, 'z: %.2f' % z, ('+' if z > 0 else '-'))

        if z < 0.4:
            return False

        # buy
        o = coinbene.order('buy', symbols[0], prices[0] * 1.01, buy_amount)

        time.sleep(1)

        # buy
        o = coinbene.order('buy', symbols[1], prices[1] * 1.01, sell_amount, o.get("sequence") + 1)

        time.sleep(1)

        # sell
        o = coinbene.order('sell', symbols[2], prices[2] * 0.99, sell_amount, o.get("sequence") + 1)

        # exit()

        time.sleep(10)

        return True


    '''
    站内三角形, 单边交易
    ['swtc', 'eth', 'cnyt']

    plan B

    buy sell sell

     buy: swtc/cnyt     <     0.00775 * 3000 = 23.25cnyt
    sell: swtc/eth      >   0.0000039 * 3000 = 0.0117eth
    sell: eth/cnyt      >   1782.41 * 0.0117 = 20.854197cnyt

    '''

    @staticmethod
    def buy_sell_sell(symbols, buy_amount):

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

        if z < 0.4:
            return False

        # buy
        o = coinbene.order('buy', symbols[0], prices[0] * 1.01, buy_amount)

        time.sleep(1)

        # sell
        o = coinbene.order('sell', symbols[1], prices[1] * 0.99, buy_amount, o.get('sequence') + 1)

        time.sleep(1)

        # sell
        o = coinbene.order('sell', symbols[2], prices[2] * 0.99, sell_amount, o.get('sequence') + 1)

        # exit()

        time.sleep(10)

        return True



if __name__ == "__main__":


    while True:

        # print (time.strftime("%Y-%m-%d %H:%M:%S"))

        print ('# buy buy sell')

        triangle.buy_buy_sell(['btc/usdt', 'eth/btc', 'eth/usdt'], 0.0002)

        print ('# buy sell sell')

        time.sleep(3)
