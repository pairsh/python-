import json

import requests
from lxml import etree

headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3877.400 QQBrowser/10.8.4506.400","host":"api.bilibili.com"}
def get_requests():
    a=requests.get(url="https://api.bilibili.com/x/player/pagelist?aid=97325890&jsonp=jsonp",headers=headers)
    b=json.loads(a.text)
    c=b.get("data")[0]["cid"]
    return c
d=get_requests()

def get_and_save_flv_url(e):
    a=requests.get(url="https://api.bilibili.com/x/player/playurl?avid=97325890&cid={}&qn=32&type=&otype=json".format(e),headers=headers)
    c=json.loads(a.text)
    b=c["data"]["durl"][0]["url"]
    r=requests.get(url=b,headers=headers)
    with open("测试.flv","wb") as f:
        for data in b.iter_content(1024):
            f.write(data)
    
get_and_save_flv_url(d)