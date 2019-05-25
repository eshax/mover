# -*- coding:utf-8 -*-


import os, sys, time, json, redis, pymongo

rdb = redis.Redis(host='127.0.0.1', port=6379, db=0)
mdb = pymongo.MongoClient('127.0.0.1', 27017)

from common import common

class triangle:

    from services.jccdex import jccdex

    @staticmethod
    def run():

        mover_count = 2
        
        while True:

            o = rdb.rpop("triangle")

            if o:

                print (time.strftime("%Y-%m-%d %H:%M:%S"))

                o = json.loads(o)

                ooo_time    = o.get('time')
                now_time    = time.strftime('%Y-%m-%d %H:%M:%S')

                # 放弃10秒钟以前的计划
                if (compare_time(ooo_time, now_time) > 10):
                    print ('放弃10秒钟以前的计划')
                    continue

                # 不做利润太小的搬砖
                if o.get('ratio') < 1.00:
                    print ('不做利润太小的搬砖')
                    print (o.get("ratio"), o.get("type"))
                    continue

                # 只做 直搬
                if o.get('type')[0] != 'buy':
                    print ('只做直搬')
                    print (o.get("type"))
                    continue

                if triangle.check(o):
                    
                    # 测试阶段、限制搬砖次数
                    if mover_count > 0:
                        triangle.move(o)
                        mover_count -= 1

            else:

                time.sleep(1)



    '''
    确认搬砖计划
    '''

    @staticmethod
    def check(o):

        for plan in o.get('plan'):

            price = plan.get('price')
            amount = plan.get('amount')
            type = plan.get('type')
            symbol = plan.get('symbol')

            depth = common.get_depth(symbol)

            if type == 'buy':
                asks = depth.get('asks')
                if len(asks) == 0:
                    return False

                a = asks[0]
                if price < a.get('price'):
                    print ('发现计划中的价格比当前卖一价格低, 放弃搬砖')
                    print (price, '<', a.get('price'))
                    return False

                if amount < a.get('amount'):
                    print ('发现计划中的交易量比当前卖一的挂单量少, 放弃搬砖')
                    print (amount, '<', a.get('amount'))
                    return False

            if type == 'sell':
                bids = depth.get('bids')
                if len(bids) == 0:
                    return False

                b = bids[0]
                if price > b.get('price'):
                    print ('发现计划中的价格比当前买一的价格高, 放弃搬砖')
                    print (price, '>', b.get('price'))
                    return False

                if amount < b.get('amount'):
                    print ('发现计划中的交易量比当前卖一的挂单量少, 放弃搬砖')
                    print (amount, '<', b.get("amount"))
                    return False

        print ('!!!!符合搬砖条件!!!!!可以执行搬砖!!!!!')
        return True



    '''
    执行搬砖动作
    '''

    @staticmethod
    def move(o):

        print (o.get('symbol'))

        for p in o.get("plan"):

            if o.get('dex') == 'jccdex':

                type = p.get('type')
                symbol = p.get('symbol')
                price = p.get('price')
                amount = p.get('amount')

                od = jccdex.order(type, symbol, price, amount)
                if od.get('code') == 400:
                    p['msg'] = '交易失败!'
                    mdb.mover.error.insert(o)
                    return False

                if od.get('code') == 200:
                    n = 10
                    while n > 0:
                        time.sleep(0.5)
                        tx_data = jccdex.get_tx()

                        if 'data' in tx_data:
                            if 'transactions' in tx_data.get('data'):
                                for tn in tx_data.get('data').get('transactions'):
                                    if tn.get('hash') == od.get('hash'):
                                        p['msg'] = '交易成功!'
                                        continue
                        n = n - 1

                    if n == 0:
                        p['msg'] = '交易失败!'
                        mdb.mover.error.insert(o)
                        return False
                    
        mdb.mover.finish.insert(o)
        return True
                


'''
时间比较 秒
'''
def compare_time(time1, time2):
    s_time = time.mktime(time.strptime(time1,'%Y-%m-%d %H:%M:%S'))
    e_time = time.mktime(time.strptime(time2,'%Y-%m-%d %H:%M:%S'))
    return int(e_time) - int(s_time)



if __name__ == '__main__':

    triangle.run()

    # print (common.get_depth('jccdex', 'swtc/eth'))
