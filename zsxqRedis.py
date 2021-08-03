import re
import requests
import json
import time
import redis
import os
from urllib.parse import quote


redis_pool = redis.ConnectionPool(host='127.0.0.1', port= 6379, password= 'root', db= 0)
redis_conn = redis.Redis(connection_pool= redis_pool)


headers = {
        'Authorization': '35372488-AC29-8CEB-32B0-8207EDFE3159_65B85BD04AE259A0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }

def get_data(url):
    count = 0
    time.sleep(2)
    print(url)
    rsp = requests.get(url, headers=headers)
    print("状态码"+ str(rsp.status_code))
    print("返回值"+ str(rsp.json().get('succeeded')))

    try:
        for topic in rsp.json().get('resp_data').get('topics'):
            topic['latest_likes'] = ""
            topic['group'] = ""
            topic['show_comments'] = ""
            redis_conn.lpush('fans',json.dumps(topic,indent=2, ensure_ascii=False))
    except ZeroDivisionError as e:
        print('except',e)

    next_page = rsp.json().get('resp_data').get('topics')
    if next_page:
        create_time = next_page[-1].get('create_time')
        if create_time[20:23] == "000":
            end_time = create_time[:20]+"999"+create_time[23:]
        else :
            res = int(create_time[20:23])-1
            end_time = create_time[:20]+str(res).zfill(3)+create_time[23:] # zfill 函数补足结果前面的零，始终为3位数
        end_time = quote(end_time)
        if len(end_time) == 33:
            end_time = end_time[:24] + '0' + end_time[24:]
        next_url = start_url + '&end_time=' + end_time
        get_data(next_url)
    count+=1
    return count


if __name__ == '__main__':
    start_url = 'https://api.zsxq.com/v1.10/groups/552521181154/topics?scope=digests&count=20'
    get_data(start_url)