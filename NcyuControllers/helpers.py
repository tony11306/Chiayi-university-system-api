import requests
from bs4 import BeautifulSoup


# get ViewState ViewStateGenerator and EventValidation
def get_VVE(url='https://web085004.adm.ncyu.edu.tw/NewSite/Login.aspx?Language=zh-TW'):

    html = requests.session().get(
        url=url, 
        headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    ).text
    soup = BeautifulSoup(html, features='html.parser')
    viewState = soup.find('input', {'id': '__VIEWSTATE'})['value']
    viewStateGenerator = soup.find('input', {'id': '__VIEWSTATEGENERATOR'})['value']
    eventValidation = soup.find('input', {'id': '__EVENTVALIDATION'})['value']
    return {
        'viewState': viewState,
        'viewStateGenerator': viewStateGenerator,
        'eventValidation': eventValidation
    }