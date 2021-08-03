import re
import requests
import json
import time
import redis
import datetime
import os
from urllib.parse import quote


redis_pool = redis.ConnectionPool(host='127.0.0.1', port= 6379, password= 'root', db= 0)
redis_conn = redis.Redis(connection_pool= redis_pool)


headers = {
        'Authorization': '35372488-AC29-8CEB-32B0-8207EDFE3159_65B85BD04AE259A0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }

# https://api.zsxq.com/v1.10/topics/418452541842558/share_url
# datas = redis_conn.lrange('fans',0,-1)
# print(datas)

data_aug = []
pattern= re.compile(r'<[^>]+>',re.S)
for item in redis_conn.lrange('fans',0,-1):
    _item = json.loads(item)
    _id = _item['topic_id']
    rsp = requests.get('https://api.zsxq.com/v1.10/topics/'+str(_id)+'/share_url', headers=headers)
    print("状态码"+ str(rsp.status_code))
    print("返回值"+ str(rsp.json()))

    _sharurl = rsp.json().get('resp_data').get('share_url')
    _title = pattern.sub('', _item['talk']['text'])
    _dateTime = _item['create_time']
    _dict = {"id":_id, "title":_title,"datetime":_dateTime,'shareurl':_sharurl}
    data_aug.append(_dict)
with open('data.json','w',encoding='utf-8') as f:
    f.write(json.dumps(data_aug, indent=2, ensure_ascii=False))
