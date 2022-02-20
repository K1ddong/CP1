from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import urllib.request
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.firefox.options import Options as FirefoxOptions

import re

#로컬용
chromedriver_loc = '/Users/dennis/projects/cp1/venv/chromedriver'
geckodriver_loc = '/Users/dennis/projects/cp1/venv/geckodriver'

def get_url(search_term):
    url = f'https://search.shopping.naver.com/search/all?query={search_term}'
    return url


def main(search_term):
    options = FirefoxOptions()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    url = get_url(search_term)
    driver.get(url)

    for i in range(3):
        driver.execute_script("window.scrollTo(0, 5000)")
        time.sleep(0.5) 

    get_item_info(driver)

    driver.close()
 

def get_item_info(driver):
    item_info = []
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    item_list = soup.find_all('div',{'class':'basicList_inner__eY_mq'})


    for item in item_list:
        item_title = item.find('div',{'class':'basicList_title__3P9Q7'}).text.strip()
        item_price = item.find('span',{'class':'price_num__2WUXn'}).text.strip()
        item_price = int(re.sub('[^0-9]', '',item_price))
        reviews = item.find('em',{'class':'basicList_num__1yXM9'}).text.strip()
        reviews = int(re.sub('[^0-9]', '',reviews))
        item_info.append([item_title,item_price,reviews])
    print(item_info)
    return item_info

if __name__ == '__main__':
    # search_term = input('검색할 상품 키워드를 입력하세요...')
    search_term = '밥솥'
    main(search_term)

