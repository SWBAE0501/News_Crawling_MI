import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from urllib.parse import quote
from dotenv import load_dotenv
import os

#크롤링 함수 정의
def google_news_crawler(query: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " +
                      "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    
    base_url = "https://news.google.com/search?q={query}%20when%3A3h&hl=ko&gl=KR&ceid=KR%3Ako"
    encoded_query = quote(query)
    url = base_url.format(query=encoded_query)

    response = requests.get(url, headers=headers)
    assert response.status_code == 200, "No result found"
    soup = BeautifulSoup(response.content, "html.parser")

    results = []
    for item in soup.find_all("a", attrs={"class": "JtKRv"})[:5]:
        title = item.get_text(strip=True)
        link = item["href"]
        if link.startswith("./"):
            link = "https://news.google.com" + link[1:]

        results.append(f"[{title}] - ({link})\n")
    
    return results

 
    
#콘텐츠 파일 작성

with open('google_news_results.txt', 'w', encoding = 'utf-8') as file:
    query = ["삼성전자", "중소벤처기업부", "동반성장위원회", "동반성장", "상생협력"]
    for search_query in query:
        results = google_news_crawler(search_query)
        file.write(f'키워드 : [{search_query}]\n\n')
        for item in results:
            file.write(item+'\n')
        file.write('\n')



#텍스트 파일 읽기
with open('google_news_results.txt', 'r', encoding = 'utf-8') as file:
	email_content = file.read()

load_dotenv()

#이메일 메시지 설정
msg = EmailMessage()
msg['Subject'] = '구글 뉴스 검색 결과'
msg['From'] = os.getenv("EMAIL_FROM")
msg['To'] = os.getenv("EMAIL_TO")
msg.set_content(email_content)

#smtp  서버 설정 및 로그인
server = smtplib.SMTP('smtp.naver.com' , 587)
server.starttls()

MY_ID = os.getenv("MY_ID")
MY_PW = os.getenv("MY_PW")
server.login(MY_ID, MY_PW)

#이메일 발송
server.send_message(msg)
server.quit()
   
    
    
    
    
    
    
    
    
    