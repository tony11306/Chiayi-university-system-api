import time
import requests
import json
from bs4 import BeautifulSoup


# A: 蘭潭, B: 民雄, C: 林森, D: 新民
CAMPUS_OPTION_VALUES = ['A', 'B', 'C', 'D']
# 禮拜一到日
COURSE_DAYS = ['1', '2', '3', '4', '5', '6', '7']
CLASSES = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
HEADER = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
}
SEARCH_URL = 'https://web085003.adm.ncyu.edu.tw/pub_timta1.aspx'
SEARCH_URL_2 = 'https://web085003.adm.ncyu.edu.tw/pub_timta2.aspx'

def get_current_semester() -> tuple[str, str]:
    res = requests.post(url=SEARCH_URL, data={
        'WebPid1': '',
        'Language': 'zh-TW',
        'program': ''
    })

    soup = BeautifulSoup(res.text, features='html.parser')
    course_select_year = soup.find('select', {'name': 'WebYear1'}).find('option', {'selected': True})['value']
    course_select_semester = soup.find('select', {'name': 'WebTerm1'}).find('option', {'selected': True})['value']

    return (course_select_year, course_select_semester)

course_select_year, course_select_semester = get_current_semester()

print(course_select_year, course_select_semester)

courses = []

def parse_data():
    pass

def course_time_to_dict(day: str, start_end_time: str):
    start_end = start_end_time.split('~')
    return {
        "星期": day,
        "開始節次": start_end[0],
        "結束節次": start_end[1]
    }

def find_course_outline_url(td_element):
    try:
        crscode = td_element.find('a')['href'].replace('/pub_tagoutline.aspx?tagid=', '')
        crscode = crscode.replace('&WebPid1=1', '')
        return 'https://web085004.adm.ncyu.edu.tw/Syllabus/Syllabus_Rpt.aspx?CrsCode=' + crscode
    except:
        return ""

st = set()

# this will take up to 4 or 5 mins
# considering not to crash the server
# i decided not to use multi-thread request
for campus in CAMPUS_OPTION_VALUES:
    for day in COURSE_DAYS:
        for start_class in CLASSES:
            res = requests.post(url=SEARCH_URL_2, headers=HEADER, data={
                'WebPid1': '1',
                'WebYear1': course_select_year,
                'WebTerm1': course_select_semester,
                'WebCamp7': campus,
                'WebWeek8': day,
                'WebUnit9': start_class
            }, timeout=None)
            soup = BeautifulSoup(res.text, features='html.parser')
            for curriculum in soup.find_all('table')[3].find_all('tr')[1:]:
                row = curriculum.find_all('td')
                try:
                    course_id = row[2].text + row[3].text + row[5].text
                    if course_id in st:
                        continue
                    datas = {
                        '選課類別': row[0].text,
                        '課程類別': row[1].text,
                        '開課系號': row[2].text,
                        '開課序號': row[3].text,
                        '課程名稱': row[4].text,
                        '教學大綱': find_course_outline_url(row[4]),
                        '永久課號': row[5].text,
                        '開課單位': row[6].text,
                        '上課學制': row[7].text,
                        '上課學院': row[8].text,
                        '上課系所': row[9].text,
                        '上課組別': row[10].text,
                        '適用年級': row[11].text,
                        '上課班別': row[12].text,
                        '課程修別': row[13].text,
                        '學分數': row[14].text,
                        '時數': row[15].text,
                        '學期數': row[16].text,
                        '授課類別': row[17].text,
                        '備註': row[18].text,
                        '授課老師': row[19].text.strip(),
                        '上課時間': list(map(course_time_to_dict, row[20].text.strip().split(), row[21].text.strip().split())),
                        '上課教室': row[22].text,
                        '校區': row[23].text,
                        '限修人數': row[24].text,
                        '限選條件': row[26].text
                        
                    }
                    courses.append(datas)
                    st.add(course_id)
                    print(datas)
                    
                except:
                    pass

        
print(len(courses))
with open('./SchoolSystemModel/current_semester_course_datas/current_semester_course_datas.json', 'w', encoding='utf-8') as f:
    json.dump({'選課學年': f'{course_select_year} 學年度第 {course_select_semester} 學期', '所有課程': courses}, fp=f, ensure_ascii=False)
