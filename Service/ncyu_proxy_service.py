import requests
from bs4 import BeautifulSoup
from Helper.helper import get_VVE
from Interface.Service.ncyu_proxy_service import NCYUProxyServiceInterface

class NCYUProxyService(NCYUProxyServiceInterface):
    LOGIN_PAGE_URL = 'https://web085004.adm.ncyu.edu.tw/NewSite/Login.aspx?Language=zh-TW'
    PRELOGIN_URL = 'https://web085004.adm.ncyu.edu.tw/NewSite/Login.aspx/PreLogin?Language=zh-TW'
    STUDENT_GRADE_URL = 'https://web085004.adm.ncyu.edu.tw/grade_net/StuSco_630.aspx'
    STUDENT_COURSES_URL = 'https://web08503a.adm.ncyu.edu.tw/stu_selq88.aspx'

    def __init__(self):
        pass

    @staticmethod
    def _prelogin(account: str, password: str):
        HEADER = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'content-type': 'application/json'
        }

        response = requests.post(
            url=NCYUProxyService.PRELOGIN_URL,
            headers=HEADER,
            json={
                'view':{
                    'AccountId': account,
                    'Password': password
                }
            }
        )

        return response.json()['d']
    
    def login(self, account: str, password: str) -> str:
        HEADER = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        }

        prelogin_response = self._prelogin(account, password)
        if prelogin_response['Code'] != '1':
            raise Exception('Login failed')

        session = requests.session()
        vve = get_VVE()
        data = {
            '__VIEWSTATE': vve['viewState'],
            '__VIEWSTATEGENERATOR': vve['viewStateGenerator'],
            '__EVENTVALIDATION': vve['eventValidation'],
            'TbxAccountId': account,
            'TbxPassword': password,
            'HfIdentity': prelogin_response['Message'],
            'HfPavalue': password,
            'BtnLogin': ''
        }
        response = session.post(url=NCYUProxyService.LOGIN_PAGE_URL, data=data, headers=HEADER)
        webpid1 = BeautifulSoup(response.text, features='html.parser').find('input', {'name': 'WebPid1'})['value']

        # idk why this piece of code have to be added. If I don't add it, the grade endpoint can not work
        # maybe some sort of verification or something?
        response = session.get(
            url='https://web085004.adm.ncyu.edu.tw/NewSite/Index2.aspx',
            data={
                'WebPid1': webpid1,
                'Language': 'zh-TW'
            }
        )

        if webpid1 == None:
            raise Exception('Login failed')

        return webpid1

    def get_student_grade(self, webpid1: str):
        HEADER = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        }
        session = requests.session()
        response = session.post(
            url=NCYUProxyService.STUDENT_GRADE_URL,
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
                url=NCYUProxyService.STUDENT_GRADE_URL,
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
        return {'result': {'所有學期': result}}
    
    def get_personal_courses(self, webpid1: str):
        HEADER = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        }
        res = requests.post(
            url=NCYUProxyService.STUDENT_COURSES_URL, # 當學期選課查詢
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
        
        return {'result':{'所有課程': curriculums}}
