#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

import time
import urllib
import urllib2
import hashlib
import requests
import json


class Beta_Service(object):

    def __init__(self):
        self.t = '1524046986'
        self.imei = '6c19eac4309d3e2ebe9398d333969943'
        self.imsi = '6c19eac4309d3e2ebe9398d333969943'
        self.deviceId = '6c19eac4309d3e2ebe9398d333969943'
        self.ttid = 'iPhone OS_11.3_iPhone_basket_AppStore_wifi_20180419140613896,6c19eac4309d3e2ebe9398d333969943,1869_5.5.3_v9233'
        self.app_key = "29129215"
        self.app_secret = '57f27786442bc2c946780746c8baa0c6'
        self.cid = 'AppStore'
        self.t = int(time.time())
        self.t = str(self.t)
        self.result = {}

    def app_md5(self, data):
        data_md5 = hashlib.md5()
        data_md5.update(data)
        return data_md5.hexdigest()

    def app_sign(self, post_data):
        appkey_md5 = self.app_md5(post_data['appKey'])

        # data md5sum
        data_md5 = self.app_md5(post_data['data'])

        signbefore = self.app_secret + "&" + \
                     appkey_md5 + "&" + \
                     post_data['api'] + "&" + \
                     post_data['v'] + "&" + \
                     self.imei + "&" + \
                     self.imsi + "&" + \
                     data_md5 + "&" + \
                     post_data['t']
        # print '签名前:' + signbefore

        # sign md5sum
        sign = self.app_md5(signbefore)
        # print "签名后:" + sign

        return sign

    def post_data(self, url, api, version='1.0', data='', sid='', fileupload=False, timestamps=''):
        # server_url = 'http://10.31.74.103:8081/cn-jsfund-server-mobile/bkt/api'
        server_url = url
        post_data = {}

        post_data['imsi'] = self.imsi
        post_data['deviceId'] = self.deviceId
        post_data['type'] = 'originaljson'
        post_data['cid'] = 'AppStore'
        post_data['imei'] = self.imei
        post_data['ttid'] = self.ttid


        # if ttid == '':
        #     post_data['ttid'] = self.ttid
        # else:
        #     post_data['ttid'] = ttid

        if timestamps == '':
            post_data['t'] = self.t
        else:
            post_data['t'] = timestamps

        if sid != '':
            post_data['sid'] = sid
        else:
            sid = ''

        post_data['data'] = data
        post_data['appKey'] = self.app_key
        post_data['api'] = api

        post_data['v'] = version
        sign_value = self.app_sign(post_data)
        post_data['sign'] = sign_value

        request = urllib2.Request(server_url)

        if sid != '':
            request.add_header('Cookie', val='JSESSIONID=' + sid)
            request.add_header('Accept-Encoding', 'gzip')
            request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=utf-8')
            print (urllib.urlencode(post_data))
            request.add_data(urllib.urlencode(post_data))

        response = urllib2.urlopen(request)
        json_str = response.read()
        print (response.read)

        print ("你好")
        print (json_str)
        return json_str






if __name__ == '__main__':
    beta_service = Beta_Service()
    beta_service.post_data(url='http://10.31.74.101:8081/cn-jsfund-server-mobile/bkt/api',
                        api='api.system.simulation.trade.stock.list',
                       data='{"uid":"14489","betaId":"1016077044"}',
                       version='1.0',
                       sid='2FC0B591D933B9D0634C8579785A4703-n1')



# -*- coding:UTF-8 -*-
import requests
import re
par={'market':'0','sort':'MZ'}
url = 'http://cfh.igoldenbeta.com/cfh-web/cfh/beta/list'

response=requests.get(url,params=par)
print(response.json())    #dict
print(type(response.json()))
print(response.text)    #string
print(response.cookies)
print(type(response.content))   #bytes
print(response.content.decode("utf-8"))
print(response.json()['data']['list'][1])  # dict list 访问方式，dict {} 使用key访问，list []  使用index访问

list1=response.json()['data']['list']       #list的循环访问
for s in list1:
    print(s['name'])
