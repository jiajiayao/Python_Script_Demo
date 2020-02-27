import requests
import json
import config
import time
import random

def test():
    #await asyncio.sleep(3)
   
    res = requests.get('https://www.baidu.com')
    print(res)


#爬虫主要
def getAnswer(question):

    params_url={
        'question':question,
    }

    res = requests.get(config.Set['targetUrl'], params=params_url, headers=config.Set['headers_url'], timeout=10)
    
    time.sleep(random.random() * 0.1)

    res=res.json()
    
    print(res)

    return res

def handleData(problems):
    res=[]
    for i in problems:
        res.append(getAnswer(i))

    
    return res

