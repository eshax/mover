# -*- coding:utf-8 -*-

'''
封装 http 方法
POST
GET
'''
import logging 
logging.getLogger("urllib3").setLevel(logging.WARNING)

import requests

class http:



    '''
    GET
    '''

    @staticmethod
    def get(url):

        r = requests.get(url, timeout=5)

        return r.status_code, r.content



    '''
    POST
    '''

    @staticmethod
    def post(url, data=None, headers=None):

        r = requests.post(url, data=data, headers=headers)

        return r.status_code, r.content



if __name__ == "__main__":

    pass
    code, headers, content = http.get('http://www.baidu.com')

    print (code)
    print (content)
