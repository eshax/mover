# -*- coding:utf-8 -*-

import os, sys, time, json, binascii, requests, random

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

class jccdex:

    api = {
        "exHosts": ["ewdjbbl8jgf.jccdex.cn",
                    "e5e9637c2fa.jccdex.cn",
                    "e9joixcvsdvi4sf.jccdex.cn",
                    "eaf28bebdff.jccdex.cn",
                    "ejid19dcf155a0.jccdex.cn",
                    "ejii363fa7e9a6.jccdex.cn",
                    "ejin22b16fbe3e.jccdex.cn",
                    "ejio68dd7d047f.jccdex.cn"],
        "infoHosts": [
                    "i3b44eb75ef.jccdex.cn",
                    "i059e8792d5.jccdex.cn",
                    "i352fb2ef56.jccdex.cn",
                    "ib149d5a1e5.jccdex.cn",
                    "i8c0429aaeb.jccdex.cn",
                    "i33a177bdf2.jccdex.cn",
                    "i1ff1c92a2f.jccdex.cn",
                    "iujhg293cabc.jccdex.cn",
                    "iujh6753cabc.jccdex.cn",
                    "ikj98kyq754c.jccdex.cn",
                    "il8hn7hcgyxk.jccdex.cn"]
    }

    ex_api      = 'https://ewdjbbl8jgf.jccdex.cn'
    account = "jaSmctLLJhTaYbPA2bFxU9T5AFrroZFWQ3"
    secret  = "ssbczL7WYpmG1mP1xPZsjDkWi6J6H"


    '''
    查询 api
    '''

    @staticmethod
    def info(url):

        url = 'https://' + random.choice(jccdex.api['infoHosts']) + url

        code, content = http.get(url)

        if code == 200:
            return content


    '''
    交易 api
    '''

    @staticmethod
    def exchange(url, data=None):

        url = 'https://' + random.choice(jccdex.api['exHosts']) + url

        if data:
            code, content = http.post(url, data=data)
        else:
            code, content = http.get(url)

        if code == 200:
            return content

    symbols = [
        ('usdt', 'JUSDT'),
        ('moac', 'JMOAC'),
        ('fst', 'JFST'),
        ('xrp', 'JXRP'),
        ('csp', 'CSP'),
        ('eth', 'JETH'),
        ('swtc', 'SWT'),
        ('jcc', 'JJCC'),
        ('call', 'JCALL'),
        ('slash', 'JSLASH'),
        ('vcc', 'VCC'),
    ]

    '''
    币种翻译
    '''

    @staticmethod
    def get_symbol(symbol):

        symbols = {
            'usdt/cnyt' : 'JUSDT-CNY',

            'moac/cnyt' : 'JMOAC-CNY',
            'moac/eth'  : 'JMOAC-JETH',
            'moac/usdt' : 'JMOAC-JUSDT',
            'moac/swtc' : 'JMOAC-SWT',

            'fst/cnyt'  : 'JFST-CNY',
            'fst/usdt'  : 'JFST-JUSDT',

            'xrp/cnyt'  : 'JXRP-CNY',
            'xrp/usdt'  : 'JXRP-JUSDT',
            'xrp/swtc'  : 'JXRP-SWT',

            'csp/cnyt'  : 'CSP-CNY',
            'csp/swtc'  : 'CSP-SWT',

            'eth/cnyt'  : 'JETH-CNY',
            'eth/usdt'  : 'JETH-JUSDT',

            'swtc/cnyt' : 'SWT-CNY',
            'swtc/usdt' : 'SWT-JUSDT',
            'swtc/eth'  : 'SWT-JETH',

            'jcc/cnyt'  : 'JJCC-CNY',
            'jcc/swtc'  : 'JJCC-SWT',

            'call/cnyt'  : 'JCALL-CNY',
            'call/swtc'  : 'JCALL-SWT',

            'slash/cnyt'  : 'JSLASH-CNY',
            'slash/swtc'  : 'JSLASH-SWT',

            'vcc/cnyt'  : 'VCC-CNY',
            'vcc/swtc'  : 'VCC-SWT',

        }

        return symbols.get(symbol)


    '''
    读取帐户余额
    '''

    @staticmethod
    def get_balances():
        data = {'exchange': 'jccdex'}

        url = '/exchange/balances/%s' % jccdex.account

        try:

            js = json.loads(jccdex.exchange(url))
            for item in js.get('data'):
                data[item.get('currency')] = {
                    "free": float(item.get('value')) - float(item.get('freezed')),
                    "freezed": float(item.get('freezed')),
                }
        except:
            pass

        return data


    '''
    读取帐户某个币种的余额
    '''
    @staticmethod
    def get_balances_by_currency(currency):
        js = jccdex.get_balances()

        for x, y in jccdex.symbols:
            if y in js and x == currency:
                return float(js[y].get('free'))

        return 0.0

    '''
    获取交易序号
    '''

    @staticmethod
    def get_sequence():
        url = '/exchange/sequence/%s' % jccdex.account
        js = json.loads(jccdex.exchange(url))
        return js.get('data').get('sequence')


    '''
    查询委托
    '''

    @staticmethod
    def query():
        url = '/exchange/orders/%s/1' % jccdex.account
        js = json.loads(jccdex.exchange(url))
        return js.get('data')


    '''
    挂单
    '''

    @staticmethod
    def order(type, symbol, price, amount):

        """
        type:    交易类型  buy(买),  sell(卖)
        symbol:  统一的货币对 (swtc/cnyt)
        price:   交易金额
        amount:  交易数量
        """

        # 交易币种
        symbols = jccdex.get_symbol(symbol)
        symbols = symbols.split('-')

        sequence = jccdex.get_sequence()

        # 交易类型
        if type.lower() == 'buy':
            # buy 买
            flags = 0
            gets_cny = symbols[1]
            pays_cny = symbols[0]
            gets_val = price * amount
            pays_val = amount
        else:
            # sell 卖
            flags = 524288
            gets_cny = symbols[0]
            pays_cny = symbols[1]
            gets_val = amount
            pays_val = price * amount

        o = {
            "Flags": flags,
            "Fee": 0.00001,
            "Account": jccdex.account,
            "TransactionType": 'OfferCreate',
            "TakerGets": {
                "value": gets_val,
                "currency": gets_cny,
                "issuer": 'jGa9J9TkqtBcUoHe2zqhVFFbgUVED6o9or'
            },
            "TakerPays": {
                "value": pays_val,
                "currency": pays_cny,
                "issuer": "jGa9J9TkqtBcUoHe2zqhVFFbgUVED6o9or"
            }
        }

        w = Wallet(jccdex.secret)

        o['Sequence'] = sequence
        o['SigningPubKey'] = w.get_public_key()
        prefix = 0x53545800
        serial = Serializer(None)
        hash = serial.from_json(o).hash(prefix)
        o['TxnSignature'] = w.sign(hash)

        print(o)
        blob = serial.from_json(o).to_hex()
        print(blob)

        data = {}
        data['sign'] = blob

        url = '/exchange/sign_order'
        js = jccdex.exchange(url, data = data)
        js = json.loads(js)
        print(js.get('msg'))

        if 'data' in js:
            hash = js.get('data').get('hash')
            return {'sequence': sequence, 'hash': hash, 'code': 200}
        else:
            return {'sequence': sequence, 'hash': '', 'code': 400}


    '''
    撤单
    '''

    @staticmethod
    def cancel_order(sequence):

        o = {
            "Flags": 0,
            "Fee": 0.00001,
            "Account": jccdex.account,
            "TransactionType": 'OfferCancel',
            "OfferSequence": sequence
        }

        w = Wallet(jccdex.secret)

        o['Sequence'] = jccdex.get_sequence()
        o['SigningPubKey'] = w.get_public_key()
        prefix = 0x53545800
        serial = Serializer(None)
        hash = serial.from_json(o).hash(prefix)
        o['TxnSignature'] = w.sign(hash)

        print(o)
        blob = serial.from_json(o).to_hex()
        print(blob)

        url = 'http://' + random.choice(jccdex.api['exHosts']) + '/exchange/sign_cancel_order'

        data = {}
        data['sign'] = blob

        r = requests.delete(url, data=data)
        print(r.content)

        js = json.loads(r.content)
        print(js.get('msg'))



    '''
    读取帐户交易记录
    '''

    @staticmethod
    def get_tx():

        url = '/exchange/tx/%s' % jccdex.account

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


class triangle:


    '''
    站内三角形, 单边交易
    ['swtc', 'eth', 'cnyt']

    plan A

    buy buy sell

     buy: eth/cnyt      <
     buy: swtc/eth      <
    sell: swtc/cnyt     >

    '''

    @staticmethod
    def buy_buy_sell(symbols, buy_amount):

        data = []
        try:
            for symbol in symbols:
                depth, _ = jccdex.get_depth(symbol)
                if 'asks' not in depth or 'bids' not in depth:
                    return False
                if len(depth.get('asks')) == 0 or len(depth.get('bids')) == 0:
                    return False
                data.append(depth)
        except:
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

        sell_amount = round(buy_amount / prices[1], 2)
        sell_amount -= 0.01
        sell_amount = round(sell_amount, 2)

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

        print (time.strftime("%Y-%m-%d %H:%M:%S"), '%42s' % symbols, 'x: %.2f' % x, 'y: %.2f' % y, 'z: %.2f' % z, ('+' if z > 0.1 else '-'))

        if z < 0.1:
            # print ('预计亏损!!! 放弃!!!')
            return False

        # buy
        jccdex.order('buy', symbols[0], prices[0] * 1.1, buy_amount)

        count = 5
        while count > 0:
            if ( jccdex.get_balances_by_currency(symbols[1].split('/')[1]) ) >= buy_amount:
                break
            count -= 1
            if count > 0:
                time.sleep(0.5)
        if count == 0:
            return False

        # buy
        jccdex.order('buy', symbols[1], prices[1] * 1.1, sell_amount)

        count = 5
        while count > 0:
            if ( jccdex.get_balances_by_currency(symbols[2].split('/')[0]) ) >= sell_amount:
                break
            count -= 1
            if count > 0:
                time.sleep(0.5)
        if count == 0:
            return False

        # sell
        jccdex.order('sell', symbols[2], prices[2] * 0.9, sell_amount)

        exit()

        return True


    '''
    站内三角形, 单边交易
    ['swtc', 'eth', 'cnyt']

    plan B

    buy sell sell

     buy: swtc/cnyt     <   0.00775 * 3000 = 23.25
    sell: swtc/eth      >   0.000004
    sell: eth/cnyt      >   1782.41

    '''

    @staticmethod
    def buy_sell_sell(symbols, buy_amount):

        data = []
        try:
            for symbol in symbols:
                depth, _ = jccdex.get_depth(symbol)
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
            # print (symbols, '1. ask amount', amounts[0], '<', buy_amount)
            return

        if amounts[1] < buy_amount:
            # print (symbols, '2. bid amount', amounts[1], '<', buy_amount)
            return

        sell_amount = round(buy_amount * prices[1], 2)
        sell_amount -= 0.01
        sell_amount = round(sell_amount, 2)

        if sell_amount > amounts[2]:
            # print (symbols, '3. bid amount', amounts[2], '<', sell_amount)
            return

        # 计算利润
        x = round(buy_amount * prices[0], 2)
        y = round(sell_amount * prices[2], 2)
        z = round(y - x, 2)

        print (time.strftime("%Y-%m-%d %H:%M:%S"), '%42s' % symbols, 'x: %.2f' % x, 'y: %.2f' % y, 'z: %.2f' % z, ('+' if z > 0.1 else '-'))

        if z < 0.1:
            # print ('预计亏损!!! 放弃!!!')
            return

        print (symbols, '!!!发现收益!!!开始搬砖!!!')

        # buy
        jccdex.order('buy', symbols[0], prices[0] * 1.1, buy_amount)

        count = 5
        while count > 0:
            if ( jccdex.get_balances_by_currency(symbols[1].split('/')[0]) ) >= buy_amount:
                break
            count -= 1
            if count > 0:
                time.sleep(0.5)
        if count == 0:
            return False

        # sell
        jccdex.order('sell', symbols[1], prices[1] * 0.9, buy_amount)

        count = 5
        while count > 0:
            if ( jccdex.get_balances_by_currency(symbols[2].split('/')[0]) ) >= sell_amount:
                break
            count -= 1
            if count > 0:
                time.sleep(0.5)
        if count == 0:
            return False

        exit()

        # sell
        jccdex.order('sell', symbols[2], prices[2] * 0.9, sell_amount)



if __name__ == "__main__":

    while True:

        print (time.strftime("%Y-%m-%d %H:%M:%S"))

        print ('# buy buy sell')

        triangle.buy_buy_sell(['eth/cnyt', 'swtc/eth', 'swtc/cnyt'], 0.015)
        triangle.buy_buy_sell(['eth/cnyt', 'moac/eth', 'moac/cnyt'], 0.015)
        triangle.buy_buy_sell(['usdt/cnyt', 'eth/usdt', 'eth/cnyt'], 4)
        triangle.buy_buy_sell(['swtc/cnyt', 'moac/swtc', 'moac/cnyt'], 3000)
        triangle.buy_buy_sell(['swtc/cnyt', 'jcc/swtc', 'jcc/cnyt'], 3000)
        triangle.buy_buy_sell(['swtc/cnyt', 'xrp/swtc', 'xrp/cnyt'], 3000)
        triangle.buy_buy_sell(['swtc/cnyt', 'csp/swtc', 'csp/cnyt'], 3000)
        triangle.buy_buy_sell(['swtc/cnyt', 'call/swtc', 'call/cnyt'], 3000)
        triangle.buy_buy_sell(['swtc/cnyt', 'slash/swtc', 'slash/cnyt'], 3000)
        triangle.buy_buy_sell(['usdt/cnyt', 'swtc/usdt', 'swtc/cnyt'], 4)
        triangle.buy_buy_sell(['usdt/cnyt', 'moac/usdt', 'moac/cnyt'], 4)
        triangle.buy_buy_sell(['usdt/cnyt', 'fst/usdt', 'fst/cnyt'], 4)
        triangle.buy_buy_sell(['usdt/cnyt', 'xrp/usdt', 'xrp/cnyt'], 4)

        print ('# buy sell sell')

        triangle.buy_sell_sell(['swtc/cnyt', 'swtc/eth', 'eth/cnyt'], 3000)
        triangle.buy_sell_sell(['moac/cnyt', 'moac/eth', 'eth/cnyt'], 5)
        triangle.buy_sell_sell(['eth/cnyt', 'eth/usdt', 'usdt/cnyt'], 0.015)
        triangle.buy_sell_sell(['moac/cnyt', 'moac/swtc','swtc/cnyt'], 5)
        triangle.buy_sell_sell(['jcc/cnyt', 'jcc/swtc', 'swtc/cnyt'], 100)
        triangle.buy_sell_sell(['xrp/cnyt', 'xrp/swtc', 'swtc/cnyt'], 10)
        triangle.buy_sell_sell(['csp/cnyt', 'csp/swtc', 'swtc/cnyt'], 500)
        triangle.buy_sell_sell(['call/cnyt', 'call/swtc', 'swtc/cnyt'], 3000)
        triangle.buy_sell_sell(['slash/cnyt', 'slash/swtc', 'swtc/cnyt'], 3000)
        triangle.buy_sell_sell(['swtc/cnyt', 'swtc/usdt', 'usdt/cnyt'], 3000)
        triangle.buy_sell_sell(['moac/cnyt', 'moac/usdt', 'usdt/cnyt'], 5)
        triangle.buy_sell_sell(['fst/cnyt', 'fst/usdt', 'usdt/cnyt'], 20)
        triangle.buy_sell_sell(['xrp/cnyt', 'xrp/usdt', 'usdt/cnyt'], 10)

        time.sleep(3)
