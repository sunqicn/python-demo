import os
import json
from sys import winver

a = [{"name":"feff","age":12}]

myload = []
with open('data.json','r',encoding='utf-8') as f:
    myload = json.load(f)
    print(myload)
    myload.extend(a)

with open('data.json','w',encoding='utf-8') as f:
    f.write(json.dumps(myload))



    