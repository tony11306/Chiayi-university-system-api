import requests
from bs4 import BeautifulSoup
SEARCH_URL = 'https://web085003.adm.ncyu.edu.tw/pub_timta1.aspx'

res = requests.get(SEARCH_URL)

soup = BeautifulSoup(res.text, features='html.parser')

head = soup.find('div', {'id': 'HtmlHeader'})

head.find('font', {'color': 'blue'})

head.text.split('選課學年、學期：')[1].split('(進入本網頁時間')[0].strip()