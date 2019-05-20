# -*- coding:utf-8 -*-

'''
虚拟币搬砖扫描器
'''

import os, sys, time, json, pymongo, redis

from services.coinw import coinw
from services.jccdex import jccdex
from services.huobi import huobi

import prettytable as pt

mdb = pymongo.MongoClient('127.0.0.1', 27017)
rdb = redis.Redis(host='127.0.0.1', port=6379, db=0)

class plan:

    '''
    生成搬砖计划
    跨市单币种, 双边交易
    '''

    @staticmethod
    def bilateral(symbol, ratio, ask_dex, ask_price, ask_amount, bid_dex, bid_price, bid_amount):

        # 最大允许交易量
        max_amount = ask_amount
        if ask_amount > bid_amount:
            max_amount = bid_amount

        # 建议单次搬砖交易量
        amount = max_amount * 0.5

        o = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "type": "bilateral",
            "dex": "%s/%s" % (ask_dex, bid_dex),
            "symbol": symbol,
            "ratio": ratio,
            "amount": amount,
            "plan": [
                { "step": 1, "type": "buy" , "dex": ask_dex, "price": ask_price, "amount": ask_amount },
                { "step": 2, "type": "sell", "dex": bid_dex, "price": bid_price, "amount": bid_amount }
            ]
        }

        rdb.lpush('bilateral', json.dumps(o, ensure_ascii=False))
        mdb.mover.plan.insert(o)


    '''
    生成搬砖计划
    站内三角形, 单边交易
                                               ask                             bid
        [ltc/usdt]           100.000000(20.621800)             90.340000(0.202400)
        [ltc/cnyt]            633.304000(9.833000)            628.299000(1.966000)
       [usdt/cnyt]            6.936000(890.586300)            6.890000(778.358900)

    symbol: ltc/usdt/cnyt
    '''

    @staticmethod
    def triangle(symbols, ratio, dex, types, prices, amounts):
        '''
        params::
            symbols: ['ltc', 'usdt', 'cnyt']    # 币种
            ratio:                              # 获利比例
            dex:                                # 交易所
            types:                              # 交易类型 buy sell ask bid
            prices:                             # 交易金额
            amounts:                            # 交易量
        '''

        # 建议搬砖的仓位, 盘面可交易量的一半 = 0.5
        e = 0.5

        if types == ['buy', 'buy', 'sell']:
            '''
            buy: [usdt/cnyt]    6.936000(890.586300)
            buy:  [ltc/usdt]   100.000000(20.621800)
            sell: [ltc/cnyt]    633.304000(9.833000)
            '''
            a = amounts[0] / prices[1]
            b = amounts[1]
            c = amounts[2]
            d = sorted([a, b, c])[0] * e
            x = d * prices[1]
            y = d
            z = d

        if types == ['buy', 'sell', 'sell']:
            '''
            buy:   [ltc/cnyt]    633.304000(9.833000)
            sell:  [ltc/usdt]   100.000000(20.621800)
            sell: [usdt/cnyt]    6.936000(890.586300)
            '''
            a = amounts[0]
            b = amounts[1]
            c = amounts[2] / prices[1]
            d = sorted([a, b, c])[0] * e
            x = d
            y = d
            z = d * prices[1]

        if types == ['ask', 'buy', 'sell']:
            '''
            ask:   [ltc/usdt]   100.000000(20.621800)
            buy:   [ltc/cnyt]    633.304000(9.833000)
            sell: [usdt/cnyt]    6.936000(890.586300)
            '''
            a = amounts[0]
            b = amounts[1]
            c = amounts[2] / prices[0]
            d = sorted([a, b, c])[0] * e
            x = d
            y = d
            z = d * prices[0]

        if types == ['bid', 'buy', 'sell']:
            '''
            bid:   [ltc/usdt]   100.000000(20.621800)
            buy:  [usdt/cnyt]    6.936000(890.586300)
            sell:  [ltc/cnyt]    633.304000(9.833000)
            '''
            a = amounts[0]
            b = amounts[1] / prices[0]
            c = amounts[2]
            d = sorted([a, b, c])[0] * e
            x = d
            y = d * prices[0]
            z = d

        o = {
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "type": "triangle",
            "dex": dex,
            "ratio": ratio,
            "prices": prices, "amount": amounts, "types": types, "symbols": symbols,
            "plan": [
                { "step": 1, "symbol": symbols[0], "type": types[0], "price": prices[0], "amount": x },
                { "step": 2, "symbol": symbols[1], "type": types[1], "price": prices[1], "amount": y },
                { "step": 3, "symbol": symbols[2], "type": types[2], "price": prices[2], "amount": z }
            ]

        }

        if types[0] in ['buy']:
            rdb.lpush('triangle', json.dumps(o, ensure_ascii=False))

        mdb.mover.plan.insert(o)




class scan:



    '''
    获取指定交易市场的委托单据
    '''

    @staticmethod
    def get_depth(dex, symbol):

        # 币赢
        if dex == 'coinw':
            return coinw.get_depth(symbol)

        # 威链
        if dex == 'jccdex':
            return jccdex.get_depth(symbol)

        # 火币
        if dex == 'huobi':
            return huobi.get_depth(symbol)


    '''
    跨市单币种, 双边交易
    '''

    @staticmethod
    def bilateral(dex, symbol):

        dex_data = dex.split(':')

        a_dex = dex_data[0]
        b_dex = dex_data[1]

        a, _ = scan.get_depth(a_dex, symbol)
        b, _ = scan.get_depth(b_dex, symbol)

        if len(a.get("bids")) == 0 or len(b.get("bids")) == 0 or len(a.get("asks")) == 0 or len(b.get("asks")) == 0:
            return

        a_b_p = a.get("bids")[0]["price"]
        a_b_a = a.get("bids")[0]["amount"]
        b_b_p = b.get("bids")[0]["price"]
        b_b_a = b.get("bids")[0]["amount"]

        a_a_p = a.get("asks")[0]["price"]
        a_a_a = a.get("asks")[0]["amount"]
        b_a_p = b.get("asks")[0]["price"]
        b_a_a = b.get("asks")[0]["amount"]

        r_a = (float(a_b_p / b_a_p) * 100.00 - 100.00)
        r_b = (float(b_b_p / a_a_p) * 100.00 - 100.00)

        r_a_s = '*' if r_a > 0.0 else ' '
        r_b_s = '*' if r_b > 0.0 else ' '

        field_names = ['%18s' % ('[%s]' % symbol), '%24s' % 'ask', '%24s' % 'bid', '     ratio', ' ']
        tb = pt.PrettyTable()
        tb.field_names = field_names

        tb.add_row([b_dex+' : '+a_dex, '%.5f(%.5f)' % (b_a_p, b_a_a), '%.5f(%.5f)' % (a_b_p, a_b_a), '%.2f%%' % r_a, r_a_s])
        if r_a > 0.0:
            plan.bilateral(symbol, r_a, b_dex, b_a_p, b_a_a, a_dex, a_b_p, a_b_a)

        tb.add_row([a_dex+' : '+b_dex, '%.5f(%.5f)' % (a_a_p, a_a_a), '%.5f(%.5f)' % (b_b_p, b_b_a), '%.2f%%' % r_b, r_b_s])
        if r_b > 0.0:
            plan.bilateral(symbol, r_b, a_dex, a_a_p, a_a_a, b_dex, b_b_p, b_b_a)

        tb.set_style(pt.PLAIN_COLUMNS)

        for s in field_names:
            tb.align[s] = "r"

        print ()
        print (tb)



    '''
    站内三角形, 单边交易
    ['swtc', 'eth', 'cnyt']
    '''

    @staticmethod
    def triangle(dex, symbols):

        symbols = symbols.split('/')

        try:
            field_names = ['%18s' % '', '%24s' % 'ask', '%24s' % 'bid']
            tb = pt.PrettyTable()
            tb.field_names = field_names

            data = []
            data.append('%s/%s' % (symbols[0], symbols[1]))
            data.append('%s/%s' % (symbols[0], symbols[2]))
            data.append('%s/%s' % (symbols[1], symbols[2]))

            price, amount = [], []

            for symbol in data:

                o, _ = scan.get_depth(dex, symbol)

                ap = o.get("asks")[0]["price"]
                bp = o.get("bids")[0]["price"]
                aa = o.get("asks")[0]["amount"]
                ba = o.get("bids")[0]["amount"]

                price.append(ap)
                price.append(bp)
                amount.append(aa)
                amount.append(ba)

                tb.add_row(['[%s]' % symbol, '%f(%f)' % (ap, aa), '%f(%f)' % (bp, ba)])

            tb.set_style(pt.PLAIN_COLUMNS)
            for s in field_names:
                tb.align[s] = "r"

            print ()
            print (tb)

            '''
            plan 1
            '''

            print ()
            print ('%s > %s > %s > %s' % (symbols[2], symbols[0], symbols[1], symbols[2]))
            print ('buy > sell > sell')
            field_names = [
                '%24s' % ('[%s](ask)(buy)' % data[1]),
                '%24s' % ('[%s](bid)(sell)' % data[0]),
                '%24s' % ('[%s](bid)(sell)' % data[2]),
                '     ratio',
                ' '
                ]
            r = (price[1] - (price[2] / price[5])) / price[1] * 100.00
            if r > 0:
                plan.triangle([data[1], data[0], data[2]], r, dex, ['buy', 'sell', 'sell'], [price[2], price[1], price[5]], [amount[2], amount[1], amount[5]])
            tb = pt.PrettyTable()
            tb.field_names = field_names
            tb.add_row([
                '%f(%f)' % (price[2], amount[2]),
                '%f(%f)' % (price[1], amount[1]),
                '%f(%f)' % (price[5], amount[5]),
                '%f%%' % r,
                '%s' % '*' if r > 0 else ''
                ])
            tb.set_style(pt.PLAIN_COLUMNS)
            for s in field_names:
                tb.align[s] = "r"
            print ()
            print (tb)

            '''
            plan 2
            '''

            print
            print ('buy > do-ask > sell')
            field_names = [
                '%24s' % ('[%s](ask)(buy)' % data[1]),
                '%24s' % ('[%s](ask)(do-ask)' % data[0]),
                '%24s' % ('[%s](bid)(sell)' % data[2]),
                '     ratio',
                ' '
                ]
            r = (price[0] - (price[2] / price[5])) / price[0] * 100.00
            if r > 0:
                plan.triangle([data[0], data[1], data[2]], r, dex, ['ask', 'buy', 'sell'], [price[0], price[2], price[5]], [amount[0], amount[2], amount[5]])
            tb = pt.PrettyTable()
            tb.field_names = field_names
            tb.add_row([
                '%f(%f)' % (price[2], amount[2]),
                '%f(%f)' % (price[0], amount[0]),
                '%f(%f)' % (price[5], amount[5]),
                '%f%%' % r,
                '%s' % '*' if r > 0 else ''
                ])
            tb.set_style(pt.PLAIN_COLUMNS)
            for s in field_names:
                tb.align[s] = "r"
            print ()
            print (tb)

            '''
            plan 3
            '''

            print
            print ('%s > %s > %s > %s' % (symbols[2], symbols[1], symbols[0], symbols[2]))
            print ('buy > buy > sell')
            field_names = [
                '%24s' % ('[%s](ask)(buy)' % data[2]),
                '%24s' % ('[%s](ask)(buy)' % data[0]),
                '%24s' % ('[%s](bid)(sell)' % data[1]),
                '     ratio',
                ' '
                ]
            r = ((price[3] / price[4]) - price[0]) / price[0] * 100.00
            if r > 0:
                plan.triangle([data[2], data[0], data[1]], r, dex, ['buy', 'buy', 'sell'], [price[4], price[0], price[3]], [amount[4], amount[0], amount[3]])
            tb = pt.PrettyTable()
            tb.field_names = field_names
            tb.add_row([
                '%f(%f)' % (price[4], amount[4]),
                '%f(%f)' % (price[0], amount[0]),
                '%f(%f)' % (price[3], amount[3]),
                '%f%%' % r,
                '%s' % '*' if r > 0 else ''
                ])
            tb.set_style(pt.PLAIN_COLUMNS)
            for s in field_names:
                tb.align[s] = "r"
            print ()
            print (tb)

            '''
            plan 4
            '''

            print ()
            print ('buy > do-bid > sell')
            field_names = [
                '%24s' % ('[%s](ask)(buy)' % data[2]),
                '%24s' % ('[%s](bid)(do-bid)' % data[0]),
                '%24s' % ('[%s](bid)(sell)' % data[1]),
                '     ratio',
                ' '
                ]
            r = ((price[3] / price[4]) - price[1]) / price[1] * 100.00
            if r > 0:
                plan.triangle([data[0], data[2], data[1]], r, dex, ['bid', 'buy', 'sell'], [price[1], price[4], price[3]], [amount[1], amount[4], amount[3]])
            tb = pt.PrettyTable()
            tb.field_names = field_names
            tb.add_row([
                '%f(%f)' % (price[4], amount[4]),
                '%f(%f)' % (price[1], amount[1]),
                '%f(%f)' % (price[3], amount[3]),
                '%f%%' % r,
                '%s' % '*' if r > 0 else ''
                ])
            tb.set_style(pt.PLAIN_COLUMNS)
            for s in field_names:
                tb.align[s] = "r"
            print ()
            print (tb)

        except Exception as err:
            print (err)



    '''
    跨市三角形, 三边交易或多边交易

    '''

    @staticmethod
    def trilateral(dex, symbols):
        pass



if __name__ == "__main__":

    pass

    while True:

        time.sleep(1)

        print (time.strftime("%Y-%m-%d %H:%M:%S"))

        '''
        ::scan.list

            [coinw:jccdex]
            coinw:jccdex,moac/cnyt
            coinw:jccdex,eth/cnyt
            coinw:jccdex,swtc/cnyt

            [coinw:huobi]
            coinw:huobi,eth/usdt
            coinw:huobi,btc/usdt
            coinw:huobi,ltc/usdt
            coinw:huobi,eos/usdt

            [jccdex]
            jccdex,swtc/eth/cnyt

            [coinw]
            coinw,btc/usdt/cnyt
            coinw,eth/usdt/cnyt
            coinw,ltc/usdt/cnyt
            coinw,eos/usdt/cnyt
            coinw,xrp/usdt/cnyt
            coinw,bchabc/usdt/cnyt
        '''
        print ('read scan.list')
        if os.path.exists('scan.list'):
            with open('scan.list', 'r') as f:
                for line in f.readlines():

                    if '[' in line or '#' in line:
                        continue

                    o = line.split(',')
                    if len(o) != 2:
                        continue

                    print (line)

                    dex = o[0].strip()
                    symbol = o[1].strip()

                    # bilateral
                    if ':' in dex and len(symbol.split('/')) == 2:
                        scan.bilateral(dex, symbol)

                    # triangle
                    if ':' not in dex and len(symbol.split('/')) > 2:
                        scan.triangle(dex, symbol)

                    # trilateral
                    if ':' in dex and len(symbol.split('/')) > 2:
                        scan.trilateral(dex, symbol)

                    print ()
                    print ()

        #break
