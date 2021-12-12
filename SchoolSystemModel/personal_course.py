from flask import jsonify, abort
from flask_restful import Resource, reqparse
import requests
from bs4 import BeautifulSoup
from SchoolSystemModel.decorators import exception_decorator

HEADER = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
}

class CourseEndpoint(Resource):

    def __init__(self) -> None:
        self.reqparse_args = reqparse.RequestParser()
        self.reqparse_args.add_argument('webpid1', type=str, required=True, help='webpid1 is required')
        super().__init__()

    @exception_decorator
    def post(self):
        args = self.reqparse_args.parse_args()
        webpid1 = args['webpid1']
        res = requests.post(
            url='https://web08503a.adm.ncyu.edu.tw/stu_selq88.aspx', # 當學期選課查詢
            headers=HEADER,
            data={
                'WebPid1': webpid1,
                'language': 'zh-TW',
                'program': ''
            }
        )
        soup = BeautifulSoup(res.text, features='html.parser')
        curriculums = []

        def course_time_to_dict(day: str, start_end_time: str):
            start_end = start_end_time.split('~')
            return {
                "星期": day,
                "開始節次": start_end[0],
                "結束節次": start_end[1]
            }

        for curriculum in soup.find_all('table')[2].find_all('tr')[1:]:
            row = curriculum.find_all('td')
            curriculums.append({
                    '課程名稱': row[3].text,
                    '學分數': row[5].text,
                    '學期數': row[7].text,
                    '課程修別': row[8].text + '修',
                    '選課修別': row[9].text + '修' if row[9].text != '通' else '識',
                    '授課老師': row[12].text.strip(),
                    '上課時間': list(map(course_time_to_dict, row[13].text.strip().split(), row[14].text.strip().split())),
                    '適用年級': row[15].text,
                    '上課教室': row[16].text,
                    '校區': row[17].text,
                    '限修人數': row[18].text,
                    '選上人數': row[19].text
                }
            )
        
        return jsonify({'result':{'所有課程': curriculums}})
