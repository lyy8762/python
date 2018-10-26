# coding:utf-8
#爬取站长之家上面网站信息1-10页面的网站信息

from lxml import etree
import requests
from chardet import detect

doc=open('C:\Users\lyy\Desktop\Learning\python\url.txt','w')
n=list(range(1,21))
for i in n:
    if i==1:
        url='http://top.chinaz.com/all/index.html'
    else:
        url='http://top.chinaz.com/all/index_'+str(i)+'.html'
    resp=requests.get(url,timeout=15)
    ecoding=detect(resp.content).get('encoding')
    html=resp.content.decode(ecoding)
    tree=etree.HTML(html)
    sites=tree.xpath('//ul[@class="listCentent"]/li')
    print 'the '+str(i) + 'st page:'
    for site in sites:
        name = site.xpath('.//div[@class="CentTxt"]/h3/a')[0].text.strip()
        url = site.xpath('.//div[@class="CentTxt"]/h3/span/text()')[0]
        print 'name:'+ name +';    url:' +url

























