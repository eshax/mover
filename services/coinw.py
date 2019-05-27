# -*- coding:utf-8 -*-


'''
币赢网接口

'''
import sys, os, json, time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.md5 import md5
from utils.http import http

class coinw:

    api_url     = 'http://api.coinw.ai/appApi.html?'

    api_key     = '1b3342b5-8baf-4669-a1bc-9047ad8b720a'
    secret_key  = '5RAIGRUWKDS2I9VAYI2I4QSZ4HZAIVETUXE1'

    api_key     = '1b3342b5-8baf-4669-a1bc-9047ad8b720a'
    secret_key  = '5RAIGRUWKDS2I9VAYI2I4QSZ4HZAIVETUXE1'


    '''
    签名
    '''

    @staticmethod
    def get_sign(param):

        if '=' in param:
            param = param.split('&')
        else:
            param = []

        param.append("api_key=%s" % coinw.api_key)

        list.sort(param)

        sign = '&'.join(param)

        #print sign

        sign += '&secret_key=' + coinw.secret_key

        #print sign

        sign = md5.encode( sign )

        param.append( "sign=%s" % sign.upper() )

        param = '&'.join(param)

        #print param

        return param



    '''
    接口请求
    '''

    @staticmethod
    def post(action, param):

        code, content = http.post( coinw.api_url + action + coinw.get_sign(param) )

        if code == 200:
            return content



    '''
    查询用户信息
    '''

    @staticmethod
    def get_account():
        data = {'exchange': 'coinw'}
        action = 'action=userinfo&'

        param = ''

        js = json.loads(coinw.post(action, param))
        for item in js.get('data').get('free'):
            free = float(js.get('data').get('free').get(item))
            freezed = float(js.get('data').get('frozen').get(item))
            if free == 0 and freezed == 0:
                continue
            else:
                data[item] = {
                "free": free,
                "freezed": freezed
            }

        return data


    '''
    货币对
    '''

    @staticmethod
    def get_symbol(symbol):

        # 2:BC/CNYT  3:LTC/CNYT  5:HC/CNYT  6:STX/CNYT  7:0X/CNYT  8:CDT/CNYT  9:TNT/CNYT  10:MANA/CNYT  11:OMG/CNYT  12:KNC/CNYT  14:ETH/CNYT  15:AE/CNYT  16:Data/CNYT  17:HPY/CNYT  18:DAT/CNYT  19:RNT/CNYT  20:DEW/CNYT  21:MAG/CNYT  23:STORJ/CNYT  24:SNT/CNYT  25:DOGE/CNYT  28:WICC/CNYT  29:EOS/CNYT  30:SDA/CNYT  31:COINS/CNYT  32:BDG/CNYT  33:CHAT/CNYT  34:IHT/CNYT  36:RCT/CNYT  37:PTC/CNYT  38:ENJ/CNYT  39:EET/CNYT  40:OC/CNYT  41:EPC/CNYT  42:MTC/CNYT  43:MOAC/CNYT  44:EOSDAC/CNYT  45:BTC/CNYT  47:SWTC/CNYT  48:EKT/CNYT  49:EON/CNYT  50:LEEK/CNYT  51:AVH/CNYT  52:CAM/CNYT  53:BCD/CNYT  54:TRIO/CNYT  55:ELF/CNYT  57:ISC/CNYT  58:ONT/CNYT  59:USDT/CNYT  60:XRP/CNYT  61:DASH/CNYT  62:RVN/CNYT  63:DCR/CNYT  65:TST/CNYT  66:QTUM/CNYT  68:ADA/CNYT  69:BCHABC/CNYT  70:TRX/CNYT  71:CVNT/CNYT  72:VET/CNYT  73:HX/CNYT  76:BXA/CNYT  77:BTT/CNYT  78:BTC/USDT  79:ETH/USDT  80:QTUM/USDT  81:HC/USDT  82:DASH/USDT  83:XRP/USDT  84:EOS/USDT  85:BNB/CNYT  86:LTC/USDT  87:ADA/USDT  88:VET/USDT  89:ONG/CNYT  91:HT/CNYT  92:FET/CNYT  93:VTHO/CNYT  94:XMR/CNYT  96:CELR/CNYT  97:VSYS/CNYT  98:TRX/USDT  99:BCHABC/USDT  102:YAX/CNYT  104:BAT/CNYT  105:ZEC/CNYT  107:DREP/CNYT  108:ATOM/CNYT  109:MATIC/CNYT

        symbols = {

            'ltc/cnyt'  : 3,

            'moac/cnyt' : 43,
            'eth/cnyt'  : 14,
            'swtc/cnyt' : 47,

            'eos/cnyt'  : 29,

            'xrp/cnyt'  : 60,
            'xrp/usdt'  : 83,

            'bchabc/usdt':99,
            'bchabc/cnyt':69,

            'eth/usdt'  : 79,
            'btc/usdt'  : 78,
            'ltc/usdt'  : 86,
            'eos/usdt'  : 84,

            'btc/cnyt'  : 45,

            'usdt/cnyt' : 59,

        }

        return symbols.get(symbol)



    '''
    查询行情深度
    '''

    @staticmethod
    def get_depth(symbol):

        depth = {"bids": [], "asks": [], "symbol": symbol}
        js = {}

        symbol = coinw.get_symbol(symbol)

        action = 'action=depth&'

        param = 'symbol=%s' % symbol

        try:

            js = json.loads(coinw.post(action, param))

            if 'data' in js:
                for o in js['data']['bids']:
                    depth['bids'].append({"price": float(o['price']), "amount": float(o['amount'])})
                for o in js['data']['asks']:
                    depth['asks'].append({"price": float(o['price']), "amount": float(o['amount'])})

        except Exception as err:
            pass
            print (err)

        return depth, js



if __name__ == "__main__":

    pass

    o = coinw.get_account()

    o = json.loads(o)

    print ('msg:', o.get("msg"))
    print ()

    while True:

        time.sleep(1)

        for a in ['eos/cnyt', 'moac/cnyt']:
            o, _ = coinw.get_depth(a)

            print (a)
            print (o)
            print ()

        break
