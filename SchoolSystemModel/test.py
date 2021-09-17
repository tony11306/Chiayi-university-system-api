import requests
import json

list1 = '一 二 三'
list2 = '1~1 2~2 3~3'

def map_function(day, start_end_time):
    start_end = start_end_time.split('~')
    return {
        "星期": day,
        "開始節次": start_end[0],
        "結束節次": start_end[1]
    }

print(list(map(map_function, list1.split(), list2.split())))