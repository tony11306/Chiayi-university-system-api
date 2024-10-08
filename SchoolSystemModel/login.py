from flask import jsonify, abort
from flask.helpers import make_response
from flask_restful import Resource, reqparse
import requests
from bs4 import BeautifulSoup
import cv2
import numpy as np
from SchoolSystemModel.decorators import exception_decorator
from SchoolSystemModel.helpers import get_VVE
from CaptchaRecognition.captcha_recognizer import CaptchaRecognizer

LOGIN_PAGE_URL = 'https://web085004.adm.ncyu.edu.tw/NewSite/Login.aspx?Language=zh-TW'
PRELOGIN_URL = 'https://web085004.adm.ncyu.edu.tw/NewSite/Login.aspx/PreLogin?Language=zh-TW'
CAPTCHA_URL = 'https://web085004.adm.ncyu.edu.tw/NewSite/Captcha.ashx'


class LoginEndpoint(Resource):

    # static variable
    captcha_recognizer = CaptchaRecognizer()

    def __init__(self) -> None:
        self.reqparse_args = reqparse.RequestParser()
        self.reqparse_args.add_argument('account', type=str, required=True, help='account is required')
        self.reqparse_args.add_argument('password', type=str, required=True, help='password is required')
        super().__init__()

    # this will return webpid1
    @exception_decorator
    def post(self):
        args = self.reqparse_args.parse_args()
        account = args['account']
        password = args['password']
        HEADER = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        }

        s = requests.session()
        code = '4'
        captcha_text = ''
        response = None
        loop_times = 0
        # get captcha image
        while code == '4' and loop_times < 6:
            response = s.get(url=CAPTCHA_URL, headers=HEADER)
            captcha = response.content
            captcha = cv2.imdecode(np.frombuffer(captcha, np.uint8), cv2.IMREAD_COLOR)
            captcha_text = self.captcha_recognizer.recognize(captcha)  

            response = s.post(url=PRELOGIN_URL, headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
                'content-type': 'application/json'
            }, json={
                'view':{
                    'AccountId': account,
                    'Password': password,
                    'Captcha': captcha_text
            }}).json()['d']
            code = response['Code']
            loop_times += 1

        if code == '4':
            abort(500)

        if code != '1':
            abort(401)

        vve = get_VVE()
        data = {
            '__VIEWSTATE': vve['viewState'],
            '__VIEWSTATEGENERATOR': vve['viewStateGenerator'],
            '__EVENTVALIDATION': vve['eventValidation'],
            'TbxAccountId': account,
            'TbxPassword': password,
            'TbxCaptcha': captcha_text,
            'HfIdentity': response['Message'],
            'HfPavalue': password,
            'BtnLogin': ''
        }
        response = s.post(url=LOGIN_PAGE_URL, data=data, headers=HEADER)
        webpid1 = BeautifulSoup(response.text, features='html.parser').find('input', {'name': 'WebPid1'})['value']
        
        # idk why this piece of code have to be added. If I don't add it, the grade endpoint can not work
        # maybe some sort of verification or something?
        response = s.get(
            url='https://web085004.adm.ncyu.edu.tw/NewSite/Index2.aspx',
            data={
                'WebPid1': webpid1,
                'Language': 'zh-TW'
            }
        )

        if webpid1 == None:
            abort(417)
        return jsonify({'result': {'webpid1': webpid1}})
        