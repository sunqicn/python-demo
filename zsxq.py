import re
import requests
import json
import time
import os
from urllib.parse import quote


headers = {
        'Authorization': '35372488-AC29-8CEB-32B0-8207EDFE3159_65B85BD04AE259A0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }

def get_data(url):
    time.sleep(2)
    print(url)
    rsp = requests.get(url, headers=headers)
    print("状态码"+ str(rsp.status_code))
    
    # with open('test.json', 'w', encoding='utf-8') as f:        # 将返回数据写入 test.json 方便查看
    #     f.write(json.dumps(rsp.json(), indent=2, ensure_ascii=False))

    try:
        with open('data.json','r',encoding='utf-8') as f:
            myload = json.load(f)
            newlist = rsp.json().get('resp_data').get('topics')
            for topic in newlist:
                topic['latest_likes'] = ""
                topic['group'] = ""
                topic['show_comments'] = ""

                myload.append(topic)
        
        with open('data.json','w',encoding='utf-8') as f:
            f.write(json.dumps(myload, indent=2, ensure_ascii=False))
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

    return myload


if __name__ == '__main__':
    start_url = 'https://api.zsxq.com/v2/groups/552521181154/topics?scope=digests&count=20'
    get_data(start_url)