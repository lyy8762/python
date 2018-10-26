# coding:utf-8
#爬取豆瓣读书上的一些书目信息

from lxml import etree
import requests
from chardet import detect

url = 'https://book.douban.com/'
resp = requests.get(url, timeout=15)
ecoding = detect(resp.content).get('encoding')
html = resp.content.decode(ecoding)
tree = etree.HTML(html)
books = tree.xpath('//div[@class="section popular-books"]/div[@class="bd"]/ul/li')
for book in books:
    title = book.xpath('.//div[@class="info"]/h4/a')[0].text.strip()
    author = book.xpath('.//div[@class="info"]/p[@class="author"]/text()')[0] .strip()
    print u'《', title, u'》', '\t', '--' + author

print '\n'

#获取新书速递模块的图书 （是四个list 下面又有list 两个for循环）
lists = tree.xpath('//div[@class="section books-express "]/div[@class="bd"]/div/div/ul')
for list in lists:
    books2 = list.xpath('.//li')
    for book2 in books2:
        title2 = book2.xpath('.//div[@class="info"]/div[@class="title"]/a')[0].text.strip()
        author2 = book2.xpath('.//div[@class="info"]/div[@class="author"]/text()')[0].strip()
        print u'《', title2, u'》', '\t', '--' + author2
    print '\n'
