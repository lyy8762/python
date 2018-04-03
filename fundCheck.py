import urllib2
import re
url = 'http://cfh.igoldenbeta.com/cfh-web/cfh/beta/list?market=0&sort=MZ'

req=urllib2.Request(url)
con=urllib2.urlopen(req)


doc=con.read()
#print doc.decode("GBK").encode("utf-8")

r='dayreturn":"........'

print re.findall(r,doc)
#print doc