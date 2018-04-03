import requests
import re
url = 'http://cfh.igoldenbeta.com/cfh-web/cfh/beta/list?market=0&sort=MZ'

response=requests.get(url)
print(response.status_code)
print(type(response.text))
print(response.text)
print(response.cookies)
print(type(response.content))
print(response.content.decode("utf-8"))

