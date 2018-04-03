import urllib2
import re


url = 'https://stockcheck.igoldenbeta.com:8333/stock-check-web/fiveLevelStockList?type=0&start=0&limit=20'

req=urllib2.Request(url)
con=urllib2.urlopen(req)

doc=con.read()

print doc






