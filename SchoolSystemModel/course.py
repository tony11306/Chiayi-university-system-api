from flask import jsonify
from flask_restful import Resource
import requests
from bs4 import BeautifulSoup
from SchoolSystemModel.decorators import exception_decorator

HEADER = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
}

class CourseEndpoint(Resource):

    @exception_decorator
    def post(self, webpid1: str):
        res = requests.post(
            url='https://web08503a.adm.ncyu.edu.tw/stu_selq02.aspx',
            headers=HEADER,
            data={
                'WebPid1': webpid1,
                'language': 'zh-TW',
                'program': ''
            }
        )
        soup = BeautifulSoup(res.text, features='html.parser')
        curriculums = []

        def map_curriculm_time_to_list(s: str):
            result = []
            for start_end in s.split(' '):
                split_result = start_end.split('~')
                result.append({
                    '開始': split_result[0],
                    '結束': split_result[1]
                })
            return result

        for curriculum in soup.find_all('table')[2].find_all('tr')[1:]:
            row = curriculum.find_all('td')
            curriculums.append({
                    '課程名稱': row[3].text,
                    '學分數': row[5].text,
                    '學期數': row[7].text,
                    '課程修別': row[8].text + '修',
                    '選課修別': row[9].text + '修' if row[8].text != '通' else '識',
                    '授課老師': row[12].text.strip(),
                    '上課星期': row[13].text.strip(),
                    '上課節次': map_curriculm_time_to_list(row[14].text.strip()),
                    '適用年級': row[15].text,
                    '上課教室': row[16].text,
                    '校區': row[17].text,
                    '限修人數': row[18].text,
                    '選上人數': row[19].text
                }
            )
        
        return jsonify({'所有課程': curriculums})
