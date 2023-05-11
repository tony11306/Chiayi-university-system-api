import requests
import cv2
import numpy as np

'''
from CaptchaRecognition.captcha_recognizer import CaptchaRecognizer

CAPTCHA_URL = 'https://web085004.adm.ncyu.edu.tw/NewSite/Captcha.ashx'
HEADER = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
    'content-type': 'application/json'
}

s = requests.session()
response = s.get(url=CAPTCHA_URL, headers=HEADER)
captcha = response.content

# to cv2 image
captcha = cv2.imdecode(np.frombuffer(captcha, np.uint8), cv2.IMREAD_COLOR)
# show captcha
cv2.imshow('captcha', captcha)
cv2.waitKey(0)

predict = CaptchaRecognizer().recognize(captcha)
print(predict)
'''



if __name__ == '__main__':
    HEADER = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    webpid1 = '2B5BD4716A8D47F1A59B879B8AAC0E57D23B21154BF94A8ABEEFEFFD3E3BC408'

    '''
    session = requests.session()
    res = session.post(
        url='https://web08503a.adm.ncyu.edu.tw/stu_selq88.aspx', # 當學期選課查詢
        headers=HEADER,
        data={
            'WebPid1': webpid1,
            'language': 'zh-TW',
            'program': ''
        }
    )
    '''

    '''
    url = 'https://web085004.adm.ncyu.edu.tw/grade_net/StuSco_630.aspx'
    session = requests.session()
    res = requests.post(
        url=url,
        data={
            'WebPid1': webpid1,
            'Language': 'zh-TW'
        }
    )
    print(res.text)
    '''

    url = 'https://web085004.adm.ncyu.edu.tw/grade_net/StuSco_630.aspx'
    req = requests.Request(
        method='POST',
        url=url,
        data={
            'WebPid1': webpid1,
            'Language': 'zh-TW'
        }
    ).prepare()

    print(req.url)
    print(req.method)
    print(req.headers)
    print(req.body)

    session = requests.session()
    res = session.send(req)
    print(res.text)

