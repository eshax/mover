﻿# -*- coding:utf-8 -*-

import os, sys, time, json, binascii, requests, random

from jccdex import jccdex

class services:


    '''
    查询各交易所交易深度
    '''

    @staticmethod
    def get_depth(dex, symbol):

        if dex == 'jccdex':

            depth, _ = jccdex.get_depth(symbol)

            return depth