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

'''
------------------------ 크롤링 --------------------------------
'''

#키워드 번역
translator = googletrans.Translator()
# keyword = input('검색어를 입력해주세요.')
keyword = '밥솥'
keyword_en = str(translator.translate(keyword, src='ko', dest='en').text)

#구글 검색 트렌드
google = google_trends.GoogleTrend([keyword_en])
## 떠오르는 연관 키워드
rising_related_keywords = google.rising()
## 상위 연관 키워드
top_related_keywords = google.top()
## 키워드 검색 추이
google_trend = google.trends()
### 월별로 축소
google_trend = google_trend.reset_index().groupby(google_trend.reset_index()['date'].dt.to_period('M')).mean()
google_trend.reset_index(inplace=True)

### 수치 정규화 (최대치 기준으로)
df = google_trend[keyword_en]
google_trend[keyword_en] = df/df.max() * 100 

#쇼피 키워드 상품 정보
shopee_item_info = shopee_crawler.main(keyword_en)

#네이버 키워드 상품 검색량, 연관 키워드 검색량
keyword_search_volume,top_10_related_keywords= naver_ads_api.main(keyword,API_KEY, SECRET_KEY, CUSTOMER_ID)

#네이버 키워드 상품 정보
naver_item_info = naver_shopping_crawler.main(keyword)

#네이버 키워드 검색 추이
naver_trend = naver_trends.main(keyword,NAVER_API_ID, NAVER_API_SECRET)


#네이버 구글 검색 추이 통합
naver_trend[keyword_en] = google_trend[keyword_en]
'''
------------------------ 웹앱 --------------------------------
'''
# import dash_core_components as dcc
# import dash_html_components as html

from dash import html,dcc,dash_table as dt,Dash
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import flask
from werkzeug.serving import run_simple

# flask server 
application = flask.Flask(__name__) 

# dash app with flask server 
dash_app1 = Dash(__name__, server=application, url_base_pathname='/dashapp1/')

# flask app
@application.route('/')
def index():
    #print('flask app index()')
    return 'OK'

dash_app1.layout = html.Div(
    # Header Message
    children=[
        html.H1(children="Temp Analytics",),
        html.P(
            children="Temp",
        ),
        dt.DataTable(
            keyword_search_volume.to_dict('records'),
            [{"name":i, "id":i} for i in keyword_search_volume.columns]
        ),
        dt.DataTable(
            top_10_related_keywords.to_dict('records'),
            [{"name":i, "id":i} for i in top_10_related_keywords.columns]
        ),
        dt.DataTable(
            naver_item_info.to_dict('records'),
            [{"name":i, "id":i} for i in naver_item_info.columns]
        ),
        dt.DataTable(
            shopee_item_info.to_dict('records'),
            [{"name":i, "id":i} for i in shopee_item_info.columns]
        ),
        # 그래프		
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": naver_trend["날짜"],
                        "y": naver_trend[keyword],
                        "type": "lines", "name":"naver"
                    },
                    {    
                        "x": naver_trend["날짜"],
                        "y": naver_trend[keyword_en],
                        "type": "lines", "name":"google"
                    },
                ],
                "layout": {"title": "Title_1"},
            },
        ),
        dt.DataTable(
            rising_related_keywords.to_dict('records'),
            [{"name":i, "id":i} for i in rising_related_keywords.columns]
        ),
        dt.DataTable(
            top_related_keywords.to_dict('records'),
            [{"name":i, "id":i} for i in top_related_keywords.columns]
        ),
        dt.DataTable(
            naver_trend.to_dict('records'),
            [{"name":i, "id":i} for i in naver_trend.columns]
        ),
    ]
)



# #dash app with pandas

# dash_app1.layout = html.Div([
#     html.Br(),
#     html.H2('Time Series'),
#     html.Br(),
#     dcc.Graph(id='time-seiries')
# ])
# app = Dash(__name__)

# app.layout = html.Div(
#     # Header Message
#     children=[
#         html.H1(children="Temp Analytics",),
#         html.P(
#             children="Temp",
#         ),
#         dt.DataTable(
#             keyword_search_volume.to_dict('records'),
#             [{"name":i, "id":i} for i in keyword_search_volume.columns]
#         ),
#         dt.DataTable(
#             top_10_related_keywords.to_dict('records'),
#             [{"name":i, "id":i} for i in top_10_related_keywords.columns]
#         ),
#         dt.DataTable(
#             naver_item_info.to_dict('records'),
#             [{"name":i, "id":i} for i in naver_item_info.columns]
#         ),
#         dt.DataTable(
#             shopee_item_info.to_dict('records'),
#             [{"name":i, "id":i} for i in shopee_item_info.columns]
#         ),
#         # 그래프		
#         dcc.Graph(
#             figure={
#                 "data": [
#                     {
#                         "x": naver_trend["날짜"],
#                         "y": naver_trend[keyword],
#                         "type": "lines", "name":"naver"
#                     },
#                     {    
#                         "x": naver_trend["날짜"],
#                         "y": naver_trend[keyword_en],
#                         "type": "lines", "name":"google"
#                     },
#                 ],
#                 "layout": {"title": "Title_1"},
#             },
#         ),
#         dt.DataTable(
#             rising_related_keywords.to_dict('records'),
#             [{"name":i, "id":i} for i in rising_related_keywords.columns]
#         ),
#         dt.DataTable(
#             top_related_keywords.to_dict('records'),
#             [{"name":i, "id":i} for i in top_related_keywords.columns]
#         ),
#         dt.DataTable(
#             naver_trend.to_dict('records'),
#             [{"name":i, "id":i} for i in naver_trend.columns]
#         ),
#     ]
# )
'''
시각화 목록
1. 네이버
    - 네이버 키워드 검색량 (데이터 프레임)
    - 연관 키워드 검색량 (데이터 프레임)
    - 키워드 상품 정보 (데이터 프레임)
    - 키워드 검색 추이 (구글이랑 같이 교차 그래프)
2. 쇼피
    - 쇼피 키워드 상품 정보 (데이터 프레임)
3. 구글
    - 키워드 검색 추이 (네이버랑 같이 교차 그래프 (월별 축소 필요))
    - 떠오르는 연관 키워드 (데이터 프레임)
    - 상위 연관 키워드 (데이터 프레임)
'''
if __name__ == '__main__':
    # app.run_server(debug=True)
    application.debug = True
    application.run()    