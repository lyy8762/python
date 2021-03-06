# -*- coding:utf-8 -*-

# A simple example using the HTTP plugin that shows the retrieval of a
# single page via HTTP.
#
# This script is automatically generated by ngrinder.
#
# @author admin
from net.grinder.script.Grinder import grinder
from net.grinder.script import Test
from net.grinder.plugin.http import HTTPRequest
from net.grinder.plugin.http import HTTPPluginControl
from HTTPClient import NVPair
from buildPostData import buildPostData
from random import randint
from org.json import JSONObject
from HTTPClient import Cookie, CookieModule, CookiePolicyHandler
from java.util import Date

control = HTTPPluginControl.getConnectionDefaults()
# if you don't want that HTTPRequest follows the redirection, please modify the following option 0.
# control.followRedirects = 1
# if you want to increase the timeout, please modify the following option.
control.timeout = 60000

log = grinder.logger.info
# Set up a cookie handler to log all cookies that are sent and received.

test1 = Test(1, "trade.detail")
request1 = HTTPRequest()
data1 = buildPostData()
# Make any method call on request1 increase TPS
test1.record(request1)

# headers信息
headers = [NVPair("Content-Type", "application/x-www-form-urlencoded"),
           NVPair("charset", "utf-8")
           ]

# 打开文件
loginFile = "./resources/login.txt"
hostFile = "./resources/host.txt"
try:
    fp1 = open(loginFile, "r")
    fp2 = open(hostFile, "r")
except IOError:
    print("Error: open file failed")
loginlist = [login.strip('\n').rstrip() for login in fp1.readlines()]
hostlist = [host.strip('\n').rstrip() for host in fp2.readlines()]
sid = ''


def test(api, data, sid, v, url):
    submitdata = data1.post_data(api=api, data=data, timestamps='', sid=sid, version=v)
    # grinder.logger.info(submitdata)
    res = request1.POST(url, submitdata, headers)
    # grinder.logger.info(res.getText())
    return res


class TestRunner:
    # initlialize a thread
    def __init__(self):
        # grinder.statistics.delayReports = True
        # # 登录
        # data = loginlist[randint(0, len(loginlist) - 1)].split(",")
        # url = "http://%s/cn-jsfund-server-mobile/bkt/api" % (hostlist[0])
        # grinder.logger.info(url)
        # res = test('api.system.user.login', '{"pw":"%s","phone":"%s"}' % (data[1], data[0]), '', '2.0', url)
        # grinder.logger.info(res.getText())
        # if res.getText().find("success") == -1:
        #     return
        # json = JSONObject(res.getText())
        # self.sid = JSONObject(res.getText()).get('data').getString('sid')
        # grinder.logger.info(sid)

        pass

    # test method
    def __call__(self):
        # 加cookie
        threadContext = HTTPPluginControl.getThreadHTTPClientContext()
        expiryDate = Date()
        expiryDate.year += 10
        grinder.logger.info(hostlist[2][:-5])
        # url地址
        url2 = 'http://%s/goldbeta-service/bkt/api' % (hostlist[2])
        result = test('api.system.simulation.trade.stock.list',
                      '{"uid":"527","betaId":"1020491295"}',527 , '1.0', url2)

        # 返回结果检查，有返回特定字符，则判断请求成功
        if result.getText().find("success") != -1:
            grinder.statistics.forLastTest.success = 1
            grinder.logger.info(result.getText())
        else:
            grinder.statistics.forLastTest.success = 0
            # 请求失败，则输出失败时服务器返回的值
            grinder.logger.info(result.getText())