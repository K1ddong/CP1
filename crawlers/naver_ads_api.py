from ast import keyword
import hashlib
import hmac
import base64
import time
import random
import requests
import json
from config import get_secret


class Signature:

    @staticmethod
    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)

        hash.hexdigest()
        return base64.b64encode(hash.digest())


def get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID):
    timestamp = str(round(time.time() * 1000))
    signature = Signature().generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 
            'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 
            'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}


def get_data(keyword):
    uri = '/keywordstool'
    method = 'GET'
    r = requests.get(BASE_URL + uri+'?hintKeywords={}&showDetail=1'.format(keyword),
                    headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))

    #전체 키워드 관련 자료
    keyword_data = list(filter(lambda x:keyword in x['relKeyword'], r.json()['keywordList']))
    #필요한 것
    ##키워드 검색량
    print('키워드 검색량', keyword_data[0])
    ##검색량 기준 연관키워드 검색량
    test = [x for x in keyword_data if type(x['monthlyMobileQcCnt']) == int ]
    # print(test)
    top_10 = sorted(test, key = lambda x: x['monthlyMobileQcCnt'], reverse=True)
    print('연관 키워드',top_10[:10])
    #모바일/PC 검색량 비율
    #모바일 ctr, pc ctr
if __name__ == '__main__':
    BASE_URL = 'https://api.naver.com'
    API_KEY = get_secret("API_KEY")
    SECRET_KEY = get_secret("SECRET_KEY")
    CUSTOMER_ID = get_secret("CUSTOMER_ID")
    keyword = '밥솥'
    get_data(keyword)