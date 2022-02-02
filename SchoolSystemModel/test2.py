import json
import requests
from bs4 import BeautifulSoup
SEARCH_URL = 'https://web085003.adm.ncyu.edu.tw/pub_timta1.aspx'

f = open('SchoolSystemModel/current_semester_course_datas/current_semester_course_datas.json', encoding='utf-8')
datas = json.load(f)
s = set()
for data in datas['所有課程']:
    s.add(data['上課學制'])

print(s)