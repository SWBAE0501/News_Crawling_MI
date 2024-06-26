import requests
from bs4 import BeautifulSoup
from pytrends.requests import TrendReq

pytrends = TrendReq(h1 = 'ko-KR', tz=540)
df = pytrends.trending_searches(pn = 'south_korea')
print

#크롤링 함수 정의

def google_news_crawler(query):
    #구글 뉴스 검색 url
    url = f"https://news.google.com/search?q={query}&h1=ko&gl=KR&ceid=KR%3Ako"
    
    #https 요청 보내기
    response = requests.get(url)
    
    #요청 성공 시, html 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    allNews = soup.select('c-wiz.XBspb')[:5]
    global ELEMENTS
    for news in allNews:
        TITLES = news.select_one('a.JtKRv').text
        link = news.select_one('a.JtKRv')['href']
        link = link.lstrip('.')
        element = f'\a{TITLES}'+"\t (https://news.google.com"+link+')'
        ELEMENTS.append(element)
    assert response.status_code == 200, "No result found"
    
#콘텐츠 파일 작성

with open('google_news_results.txt', 'w', encoding = 'utf-8') as file:
	QUERYS = ["구글", "애플", "삼성", "넷플릭스", "아마존", "엔비디아", "메타", "XR","AR", "MR"]
    for search_query in QUERYS:
        google_news_crawler(search_query)
        file.write(f'[{search_query}]\n\n')
        for item in ELEMENTS:
            file.write(item+'\n')
        file.write('\n')
file.close()

#메일발송

import smtplib
from email.message import EmailMessage

#텍스트 파일 읽기
with open('google_news_results.txt', 'r', encoding = 'utf-8') as file:
	email_content = file.read()
    
#이메일 메시지 설정
msg = EmailMessage()
msg['Subject'] = '구글 뉴스 검색 결과'
msg['From'] = 'news_noreply@naver.com'
msg['To'] = 'tkddnjsgla@naver.com'
msg.set_content(email_content)

#smtp  서버 설정 및 로그인
server = smtplib.SMTP('smtp.naver.com' , 587)
server.starttls()
server.login('news_noreply','bsw6436778!')

#이메일 발송
server.send_message(msg)
server.quit()
   
    
    
    
    
    
    
    
    
    