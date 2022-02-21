from pytrends.request import TrendReq
import pandas as pd


def show_google_trends(keyword):
    #영어로 검색, 에러 관련 파라미터 timeout, retries, backoff_factor
    trendshow = TrendReq(hl='en-US', tz=360, timeout=(3,12), 
                                retries=1, backoff_factor=0.1)

    #오늘부터 12달 전까지의 기록, today 3-m => 3달 전, geo = 지역
    trendshow.build_payload(keyword, cat=0, timeframe='today 12-m', geo='MY')

    #관련 검색어
    related_keywords = trendshow.related_queries()
    rising_related_keywords = related_keywords[keyword[0]]['rising']
    top_related_keywords = related_keywords[keyword[0]]['top']

    #기간별 검색 트렌드
    keyword_search_trend = trendshow.interest_over_time()
    keyword_search_trend.reset_index(inplace=True)
    keyword_search_trend = keyword_search_trend[['date',keyword[0]]]
    print(rising_related_keywords,top_related_keywords,keyword_search_trend)


if __name__ == '__main__':
    keyword = ['rice cooker']
    show_google_trends(keyword)
