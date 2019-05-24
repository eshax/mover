# -*- coding:utf-8 -*-

from services.jccdex import jccdex

class common:

    @staticmethod
    def get_depth(dex, symbol):

        if dex == 'jccdex':

            depth, js = jccdex.get_depth(symbol)

            return depth


if __name__ == '__main__':

    o = common.get_depth('jccdex', 'swtc/eth')

    print (o)
