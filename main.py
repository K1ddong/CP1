from crawlers import shopee_crawler, naver_trends,naver_shopping_crawler,naver_ads_api,google_trends
from config_for_main import get_secret

import googletrans

# #네이버 데이터랩 api
NAVER_API_ID = get_secret("NAVER_API_ID")
NAVER_API_SECRET = get_secret("NAVER_API_SECRET")

# #네이버 검색광고 api
API_KEY = get_secret("API_KEY")
SECRET_KEY = get_secret("SECRET_KEY")
CUSTOMER_ID = get_secret("CUSTOMER_ID")

translator = googletrans.Translator()


if __name__ == '__main__':
    
    keyword = input('검색어를 입력해주세요.')
    keyword_en = str(translator.translate(keyword, src='ko', dest='en').text)

    #구글 검색 트렌드
    google = google_trends.GoogleTrend([keyword_en])
    ## 떠오르는 연관 키워드
    rising_related_keywords = google.rising()
    ## 상위 연관 키워드
    top_related_keywords = google.top()
    ## 키워드 검색 추이
    keyword_search_trend = google.trends()

    #쇼피 키워드 상품 정보
    shopee_item_info = shopee_crawler.main(keyword_en)

    #네이버 키워드 상품 검색량, 연관 키워드 검색량
    keyword_search_volume,top_10_related_keywords= naver_ads_api.main(keyword,API_KEY, SECRET_KEY, CUSTOMER_ID)

    #네이버 키워드 상품 정보
    naver_item_info = naver_shopping_crawler.main(keyword)

    #네이버 키워드 검색 추이
    naver_trend = naver_trends.main(keyword,NAVER_API_ID, NAVER_API_SECRET)


