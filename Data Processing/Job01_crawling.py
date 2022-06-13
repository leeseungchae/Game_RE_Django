from selenium import webdriver
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
import re
import csv

option = webdriver.ChromeOptions()
# option.add_argument('headless')
option.add_argument('lang=ko_KR')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')
option.add_argument('disable-gpu')
driver = webdriver.Chrome('./chromedriver', options=option)
driver.implicitly_wait(2)
driver.maximize_window()

url = 'https://play.google.com/store/apps/collection/cluster?clp=ogoQCAkSBEdBTUUqAggCUgIIAQ%3D%3D:S:ANO1ljKygT0&gsr=ChOiChAICRIER0FNRSoCCAJSAggB:S:ANO1ljLjwLA&hl=ko&gl=US'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}
SCROLL_PAUSE_SEC = 1


def scrool_basic(): # step 1 메인 페이지(검색) 최대 스크롤
    driver.get(url)
    last_height = driver.execute_script("return document.body.scrollHeight")  #현재위치 정보 얻기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  #가장 밑으로 내리기
    time.sleep(SCROLL_PAUSE_SEC)
    new_height = driver.execute_script("return document.body.scrollHeight")   # 현재위치 정보 얻기
    while True:
        while new_height != last_height:   # 새로운위치 != 마지막위치
            last_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # 1초 대기
            time.sleep(SCROLL_PAUSE_SEC)
            # 스크롤 다운 후 스크롤 높이 다시 가져옴
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:  #최대 스크롤 할시 종료
                break
        break

def scrool():  # step 2 리뷰 페이지 최대 스크롤
    url2 = driver.current_url + "&showAllReviews=true"  #모든 리뷰 보기
    driver.get(url2)
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_SEC)
    new_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        while new_height != last_height:
            last_height = driver.execute_script("return document.body.scrollHeight")

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 1초 대기
            time.sleep(SCROLL_PAUSE_SEC)
            # 스크롤 다운 후 스크롤 높이 다시 가져옴
            new_height = driver.execute_script("return document.body.scrollHeight")
            print(last_height)
            print(new_height)

            try:
                driver.find_element_by_xpath(
                    '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/div[2]/div[2]/div/span/span').click()
                 # 더보기 버튼 킄릭

            except:  #더보기 버튼 없을 경우 실행
                print(1)
                review_all = driver.find_elements_by_class_name('UD7Dzf')
                if not review_all:
                    print("pass")
                    pass
                else:
                    for i , review in enumerate (review_all):
                        reviews.append(review.text)
                        se = len(review_all)
                        resp = requests.get(url2, headers=headers)
                        soup = BeautifulSoup(resp.text, 'html.parser')
                        title = soup.find("h1", {"class": "AHFaub"}).get_text()
                        genre = soup.find("span", {"class": "T32cc UAO9ie"}).find_next_sibling().get_text()
                        score = soup.find("div", {"class": "pf5lIe"})
                        if score == float:
                            score = float(str(score)[47:50])
                        else:
                            score is None
                        for n in range(0, se):
                            titles.append(title)
                            genres.append(genre)
                            scores.append(score)
        return

titles = []
reviews = []
scores = []
genres = []

df=pd.DataFrame()
for i in range(1, 151):

    driver.get(url)
    if i <=50:  #51부터 페이지 순서가 바뀜
        driver.find_element_by_xpath(
        f'//*[@id="fcxH9b"]/div[4]/c-wiz/div/c-wiz/div/c-wiz/c-wiz/c-wiz/div/div[2]/div[{i}]/c-wiz/div/div/div[1]/div/div/a').click()
        scrool()
        df_game = pd.DataFrame({'title': titles, 'reviews': reviews, 'scores': scores, 'genres': genres})
        df_game.to_csv('./crawlingdata/game_data_new_49.csv', encoding='utf-8-sig', header='false', mode='w')
        print(i)
        print(df_game['title'].tail(1))

    else :
        i = i-50
        for i in range(i,151):
            scrool_basic()
            driver.find_element_by_xpath(f'//*[@id="fcxH9b"]/div[4]/c-wiz/div/c-wiz/div/c-wiz/c-wiz/c-wiz/div/div[2]/c-wiz[{i}]/div/div/div[1]/div/div/a').click()
            scrool()
            df_game = pd.DataFrame({'title': titles, 'reviews': reviews, 'scores': scores, 'genres': genres})
            df_game.to_csv('./crawlingdata/157.csv', encoding='utf-8-sig', header='false', mode='w')
            print(i+50)
            print(df_game['title'].tail(1))
            if i == 150:
                driver.close()
                break

    print(df_game)


