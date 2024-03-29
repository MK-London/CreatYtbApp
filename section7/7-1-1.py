# Section7-1
# Selenium 심화 크롤링(1)

# 시간 처리 관련
import time
# bs4 임포트
from bs4 import BeautifulSoup
# selenium 관련 임포트
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

# 크롬 옵션
chrome_options = Options()
# Headless 모드 관련
chrome_options.add_argument("--headless")
# 사운드 뮤트
# chrome_options.add_argument("--mute-audio")

# webdriver 설정(Chrome, Firefox 등) - Headless 모드
browser = webdriver.Chrome('../webdriver/chrome/chromedriver.exe', options=chrome_options)

# webdriver 설정(Chrome, Firefox 등) - 일반 모드
# browser = webdriver.Chrome('./webdriver/chrome/chromedriver.exe')

# 크롬 브라우저 내부 대기
browser.implicitly_wait(5)

# 브라우저 사이즈
# minimize_window() : 최소화
# maximize_window() : 최대화
browser.set_window_size(1920, 1280)

# 페이지 이동
browser.get('https://www.youtube.com/watch?v=83IfZhO4Pd0&')

# 5초 대기
time.sleep(5)

# html 포커스 주기 위한 코드
# Explicitly wait(명시적 대기)
WebDriverWait(browser, 5) \
    .until(
    EC.presence_of_element_located((By.TAG_NAME, 'html'))).send_keys(Keys.PAGE_DOWN)

# 2초 대기
time.sleep(2)

# 페이지 내용
# print('Before Page Contents : {}'.format(browser.page_source))

# 페이지 이동 시 새로운 데이터 수신 완료 위한 대기 시간
scraoll_pause_time = 4

# 현재 화면 페이지 높이
# IE: document.body.scrollHeight
last_height = browser.execute_script("return document.documentElement.scrollHeight")

print()

# 모든 댓글 데이터가 수신 완료 될 때까지 반복
while True:
    # 스크롤바 이동
    browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    # 대기
    time.sleep(scraoll_pause_time)

    # 스크롤바 이동 -> 새로운 데이터 수신 -> 현재 렌더링 된 화면 높이 새로 구한다.
    new_height = browser.execute_script("return document.documentElement.scrollHeight")

    # 이전 높이, 새로운 높이 비교
    print('Last Height : {}, Current Height : {}'.format(last_height, new_height))

    # 새로운 데이터 수신이 없을 경우 종료
    if new_height == last_height:
        # While 종료
        break

    # 높이 변경
    last_height = new_height

# bs4 초기화
soup = BeautifulSoup(browser.page_source, "html.parser")

# 통계 리스트 선택자
top_level = soup.select('div#menu-container yt-formatted-string#text')
# 댓글 리스트 선택자
comment = soup.select('ytd-comment-renderer#comment')

# HTML 소스 확인
# print(soup.prettify())

print()
print()

# 전체 추천 카운트
print('Total Like Count : {}'.format(top_level[0].text.strip()))
# 전체 비추 카운트
print('Total Dislike Count : {}'.format(top_level[1].text.strip()))

# Dom 반복
for dom in comment:
    print()

    # 이미지 URL 정보
    img_src = dom.select_one('#img').get('src')
    print('Thumbnail Image URLS : {}'.format(img_src if img_src else 'None'))
    # 작성자
    print('Author : {}'.format(dom.select_one('#author-text > span').text.strip()))
    # 댓글 본문
    print('Content Text : {}'.format(dom.select_one('#content-text').text.strip()))
    # 좋아요
    print('Vote Positive Count : {}'.format(dom.select_one('#vote-count-middle').text.strip()))

    print()

# 브라우저 종료
browser.quit()
