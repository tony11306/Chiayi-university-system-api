import requests
import cv2
import numpy as np

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
