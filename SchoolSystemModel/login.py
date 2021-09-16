from flask import jsonify, abort
from flask.helpers import make_response
from flask_restful import Resource
import requests
from bs4 import BeautifulSoup
from SchoolSystemModel.decorators import exception_decorator
from SchoolSystemModel.helpers import get_VVE

LOGIN_PAGE_URL = 'https://web085004.adm.ncyu.edu.tw/NewSite/Login.aspx?Language=zh-TW'
PRELOGIN_URL = 'https://web085004.adm.ncyu.edu.tw/NewSite/Login.aspx/PreLogin?Language=zh-TW'

class LoginEndpoint(Resource):

    @staticmethod
    def prelogin(account: str, password: str):
        HEADER = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
            'content-type': 'application/json'
        }

        response = requests.post(
            url=PRELOGIN_URL,
            headers=HEADER,
            json={
                'view':{
                    'AccountId': account,
                    'Password': password
                }
            }
        )

        return response.json()['d']

    # this will return webpid1
    @exception_decorator
    def post(self, account: str, password: str):
        HEADER = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        }

        prelogin_response = self.prelogin(account, password)
        if prelogin_response['Code'] != '1':
            abort(401)

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
        response = session.post(url=LOGIN_PAGE_URL, data=data, headers=HEADER)
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
            abort(417)
        return jsonify({'result': {'webpid1': webpid1}})
        