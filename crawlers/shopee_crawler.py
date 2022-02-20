from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import urllib.request
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.firefox.options import Options as FirefoxOptions

#로컬용
chromedriver_loc = '/Users/dennis/projects/cp1/venv/chromedriver'
geckodriver_loc = '/Users/dennis/projects/cp1/venv/geckodriver'

def get_url(search_term):
    url = f'https://shopee.com.my/search?keyword={search_term}&sortBy=sales' #페이지 필요할 경우 &page={}
    return url


def main(search_term):
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')

    # # 브라우저의 사이즈 지정(화면 사이즈에 따라서 동적으로 엘리멘트가 변하는 경우 필요할듯)
    # chrome_options.add_argument('windows-size=1920x1080')
    # # 그래픽 카드 사용하지 않음
    # chrome_options.add_argument('disable-gpu')
    # # http request header의 User-Agent 변조, 기본으로 크롤링 할 경우
    # # 이 정보는 크롬 헤드리스 웹드라이버로 넘어가므로 똑똑한 웹서버는
    # # 이 정보를 보고 응답을 안해줄수도 있는데 이걸 피하기 위해 변조할수있다.
    # chrome_options.add_argument('User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')


    # driver = webdriver.Chrome(executable_path=chromedriver_loc, options=chrome_options)
    
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)

    url = get_url(search_term)
    driver.get(url)

    # 페이지 스크롤
    SCROLL_PAUSE_TIME = 0.5
    y = 100
    # 현재 페이지 위치
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # y만큼 스크롤 다운
        driver.execute_script("window.scrollTo(0, "+str(y)+")")
        # 페이지 로딩
        time.sleep(SCROLL_PAUSE_TIME)
        # 현재 페이지 위치
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div[3]/div[1]/button').click()
            except:
                break
        y += 500
        last_height = new_height

    get_item_info(driver)

    driver.close()
 

def get_item_info(driver):
        rows = []
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        for i,item in enumerate(soup.find_all('div', {'class': 'col-xs-2-4 shopee-search-item-result__item'})):
            #상품명
            # name = item.find('div', {'class': '_10Wbs- _2STCsK _3IqNCf'})
            # if name is not None:
            #     name = name.text.strip()
            # else:
            #     name = ''
            #상품 가격(최저)
            price = item.find('div', {'class': 'zp9xm9 kNGSLn l-u0xK'})
            if price is not None:
                price = price.find('span', {'class': '_3c5u7X'}).text.strip()
            else:
                price = ''

            #판매량(월)
            sold = item.find('div', {'class':'_1uq9fs'})
            if sold is not None:
                sold = sold.text.strip()
            else:
                sold = ''

            #원가(세일 전)
            original_price = item.find('div', {'class':'zp9xm9 U-y_Gd _3rcqcF'})
            if original_price is not None:
                original_price = original_price.text.strip()
            else:
                original_price = ''

            #할인율
            dc_rate = item.find('span', {'class': 'percent'})
            if dc_rate is not None:
                dc_rate = dc_rate.text.strip()
            else:
                dc_rate = ''

            #상품 link
            # link = item.find('a')
            # if link is not None:
            #     link = link.get('href')
            # else:
            #     link = ''

            print([i, price, sold, original_price, dc_rate])
            rows.append([i, price, sold, original_price, dc_rate])
        return rows

if __name__ == '__main__':
    # search_term = input('검색할 상품 키워드를 입력하세요...')
    search_term = 'rice cooker'
    main(search_term)

