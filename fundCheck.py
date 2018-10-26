# -*- coding:UTF-8 -*-
import requests

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

