# -*- coding:utf-8 -*-


import os, sys, time, json, redis, pymongo


rdb = redis.Redis(host='127.0.0.1', port=6379, db=0)



def main():

    while True:

        o = rdb.rpop("triangle")

        o = json.loads(o)

        ooo_time    = o.get('time')
        now_time    = time.strftime('%Y-%m-%d %H:%M:%S')

        # 放弃10秒钟以前的计划
        if (compare_time(ooo_time, now_time) > 10):
            continue

        # 不做利润太小的搬砖
        if o.get('ratio') < 2:
            return

        check(o)



'''
确认搬砖计划
'''
def check(o):

    move(o)



'''
执行搬砖动作
'''
def move(o):

    print (o.get('symbol'))



'''
时间比较 秒
'''
def compare_time(time1, time2):
    s_time = time.mktime(time.strptime(time1,'%Y-%m-%d %H:%M:%S'))
    e_time = time.mktime(time.strptime(time2,'%Y-%m-%d %H:%M:%S'))
    return int(e_time) - int(s_time)



if __name__ == '__main__':

    main()
