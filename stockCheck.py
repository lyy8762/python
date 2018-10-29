#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import os

url = 'https://stockcheck.igoldenbeta.com:8333/stock-check-web/fiveLevelStockList?type=0&start=0&limit=20'

req=urllib.Request(url)
con=urllib.urlopen(req)

doc=con.read()
print (doc)
 