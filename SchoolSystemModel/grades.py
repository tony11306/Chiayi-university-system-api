from flask import jsonify
from flask.helpers import make_response
from flask_restful import Resource, reqparse
from flask import abort
import requests
from bs4 import BeautifulSoup
from SchoolSystemModel.decorators import exception_decorator
from requests import Session

HEADER = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
}

class GradeEndpoint(Resource):

    def __init__(self) -> None:
        self.reqparse_args = reqparse.RequestParser()
        self.reqparse_args.add_argument('webpid1', type=str, required=True, help='webpid1 is required')
        super().__init__()

    @exception_decorator
    def post(self):
        args = self.reqparse_args.parse_args()
        webpid1 = args['webpid1']
        url = 'https://web085004.adm.ncyu.edu.tw/grade_net/StuSco_630.aspx'
        session = requests.session()
        response = session.post(
            url=url,
            data={
                'WebPid1': webpid1,
                'Language': 'zh-TW'
            }
        )

        soup = BeautifulSoup(response.text, 'html.parser')
        semesterIDs = list(map(lambda tag: tag['value'], soup.find_all('option'))) # maps tag to text
        previous_page_id = soup.find('input', {'name': '__PREVIOUSPAGE'})['value']
        view_state = soup.find('input', {'id': '__VIEWSTATE'})['value']
        view_state_generator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
        event_validation = soup.find('input', {'id': '__EVENTVALIDATION'})['value']

        def get_semester_grade(semesterID):
            response = session.post(
                url=url,
                data={
                    '__EVENTTARGET': '',
                    '__EVENTARGUMENT': '',
                    '__VIEWSTATE': view_state,
                    '__VIEWSTATEGENERATOR': view_state_generator,
                    '__PREVIOUSPAGE': previous_page_id,
                    '__EVENTVALIDATION': event_validation,
                    'ddlSyearSem': semesterID,
                    'WebPid1': webpid1,
                    'Language': 'zh-TW',
                    'btnOK': '確定送出'.encode('big5')

                },
                headers=HEADER
            )
            
            soup = BeautifulSoup(response.text, 'html.parser')
            semester_text = soup.find('span', {'id': 'labelSyearSem'}).text
            result = {
                '學期': semester_text,
                '學期平均': float(soup.find('span', {'id': 'FVSelstchf_lblScoavg'}).text),
                'GPA': float(soup.find('span', {'id': 'FVSelstchf_lblGPA'}).text),
                '實得學分': float(soup.find('span', {'id': 'FVSelstchf_lblRgcrd'}).text),
                '課程': []
            }
            courses = soup.find('table', {'title': '學生單學期成績'}).find_all('tr')
            for course in courses[1:]:
                course_tds = course.find_all('td')
                result['課程'].append({
                    '課程代號': course_tds[0].text.strip('\n'),
                    '課程名稱': course_tds[1].text.strip('\n'),
                    '修別': course_tds[2].text.strip('\n'),
                    '學分': float(course_tds[3].text),
                    '學期成績': int(course_tds[4].text)
                })
            return result
            
        result = list(map(get_semester_grade, semesterIDs))
        return jsonify({'result': {'所有學期': result}})