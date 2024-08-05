# -*- coding: utf-8 -*-

# postgreSQL 설치과정: https://www.guru99.com/ko/download-install-postgresql.html

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import platform
import time
import datetime
from datetime import date
from datetime import timedelta
from datetime import datetime as dt
from tqdm import tqdm
import requests
import re
import pandas as pd
import ssl
from selenium import webdriver
import subprocess
from selenium.webdriver.chrome.service import Service as ChromeService
from pathlib import Path
import os
from time import gmtime
from time import sleep
from time import strftime
import undetected_chromedriver as uc
from tabulate import tabulate
from pprint import pprint as pp
import json
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import random
from urllib import parse
import base64
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import urllib3
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import math
import sys
import pickle
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import psycopg2
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, insert, update, delete
from sqlalchemy.orm import sessionmaker, declarative_base

ssl._create_default_https_context = ssl._create_unverified_context

osName = platform.system()  # window 인지 mac 인지 알아내기 위한

C_END = "\033[0m"
C_BOLD = "\033[1m"
C_INVERSE = "\033[7m"
C_BLACK = "\033[30m"
C_RED = "\033[31m"
C_GREEN = "\033[32m"
C_YELLOW = "\033[33m"
C_BLUE = "\033[34m"
C_PURPLE = "\033[35m"
C_CYAN = "\033[36m"
C_WHITE = "\033[37m"
C_BGBLACK = "\033[40m"
C_BGRED = "\033[41m"
C_BGGREEN = "\033[42m"
C_BGYELLOW = "\033[43m"
C_BGBLUE = "\033[44m"
C_BGPURPLE = "\033[45m"
C_BGCYAN = "\033[46m"
C_BGWHITE = "\033[47m"

# db = psycopg2.connect(host='127.0.0.1', dbname='db', user='postgres', password='1234', port=5432)
# cursor = db.cursor()

# ======================================================================================================== #
# 해당 환경은 chrome 디버그 모드 환경에서 구동이 됩니다. (크롬 디버그 자료: https://blog.naver.com/moonbird_thinker/221981266201)
# 이 환경에서는 미리 필요한 로그인을 모두 하였을때는 더 편한 수행이 가능합니다. 따라서 아래와 같은 명령어는 윈도우 powershell 에서 한번 수행 후 실행을 시켜주면 더 좋습니다.
# & 'C:\Program Files\Google\Chrome\Application\chrome.exe' --remote-debugging-port=9245 --user-data-dir="C:\chrometemtp13
# 크롬 실행파일의 위치와 포트 번호는 본인의 환경에 맞게 수정하셔야 합니다.
# ======================================================================================================== #

# [사용자 입력 정보]
# ======================================================================================================== START

# [TISTORY] 업로드 대상이 되는 티스토리 블로그 주소(본인들의 주소를 적어주시면 됩니다.)
TISTORY_BLOG_ADDRESS = "https://pemtinfo2.tistory.com"

# 업로드 대상이 되는 카테고리 정보를 입력
TISTORY_CATEGORY_NAME = '분양정보'

# time 정보
PAUSE_TIME = 1  # 셀레니움 수행도중 중간중간 wait time
LOADING_WAIT_TIME = 3  # 페이지의 로딩 시간
LOGIN_WAIT_TIME = 180  # 로그인시 기다리는 시간
TWEET_WRITE_WAIT_TIME = 60  # 트위터의 경우 너무 짧은 주기로 발행을 하면 계정이 잠기는 현상이 있음 5분 정도가 적당, random.randint(20, 60)

fixed_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Whale/3.19.166.16 Safari/537.36'

# 티스토리 쿠키를 저장하기 위한 패스 지정
COOKIES_SAVE_PATH = f'tistory_cookie_save'  # TODO: 만약 상대 경로가 안된다면 절대경로를 사용하여 적어 주어야 함
# COOKIES_SAVE_PATH = f'/Users/taesub/Desktop/crawling/tistory/tistory_cookie_save'  # for mac

# db 정보
engine_name = 'postgresql'
user_id = 'postgres'
user_pw = '1234'
host = 'localhost'
ip = '5432'
db_name = 'postDB'
# db_table_name = 'first'

# [사용자 입력 정보]
# ======================================================================================================== END


def init_driver():
    if osName not in "Windows":
        try:
            subprocess.Popen([
                '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9224 --user-data-dir="~/Desktop/crawling/chromeTemp24"'],
                shell=True, stdout=subprocess.PIPE)  # 디버거 크롬 구동
        except FileNotFoundError:
            subprocess.Popen([
                '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9224 --user-data-dir="~/Desktop/crawling/chromeTemp24"'],
                shell=True, stdout=subprocess.PIPE)
    else:
        try:
            subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9224 '
                             r'--user-data-dir="C:\chromeTemp24"')  # 디버거 크롬 구동
        except FileNotFoundError:
            subprocess.Popen(
                r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9224 '
                r'--user-data-dir="C:\chromeTemp24"')

    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9224")

    service = ChromeService('C:\\Users\\ree31\\.wdm\\drivers\\chromedriver\\win64\\127.0.6533.89\\chromedriver-win32\\chromedriver.exe')  # 본인의 경로로 변경 하시기 바랍니다.
    # service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(LOADING_WAIT_TIME)
    return driver


def twitter_login(driver):
    try:
        driver.get('https://twitter.com/home')
        sleep(LOADING_WAIT_TIME)
        driver.find_element(By.CLASS_NAME, 'public-DraftStyleDefault-block.public-DraftStyleDefault-ltr')
        print(f'\n이미 로그인 되어있습니다.')
    except:
        driver.get('https://twitter.com/i/flow/login')
        sleep(LOADING_WAIT_TIME)

        try:
            # print(f'\n{C_BOLD}{C_RED}{C_BGBLACK}[주의: 3분안에 로그인을 완료해주세요!!!]{C_END}')
            pbar = tqdm(total=LOGIN_WAIT_TIME)
            for x in range(LOGIN_WAIT_TIME):
                sleep(1)
                try:
                    driver.find_element(By.CLASS_NAME, 'public-DraftStyleDefault-block.public-DraftStyleDefault-ltr')
                    break
                except:
                    pass
                pbar.update(1)
            pbar.close()
        except:
            print('3분안에 로그인 하지 못했습니다.\n')
            exit()


def twitter_backlink_post(db_data_df, db, core_table):
    print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 시작]', C_END)
    _driver = init_driver()
    sleep(PAUSE_TIME)
    print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 완료]', C_END)

    print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[트위터 로그인 수동 과정 시작(주의 : 3분 이내에 로그인 과정을 끝내야 합니다.)]', C_END)
    twitter_login(_driver)
    sleep(PAUSE_TIME)
    print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[트위터 로그인 수동 과정 완료]', C_END)

    print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[트위터 로그인 후 쿠키값 저장 및 세션 리턴 시작]', C_END)
    twitter_session = get_cookies_session(_driver, 'https://twitter.com/home')
    sleep(PAUSE_TIME)
    print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[트위터 로그인 후 쿠키값 저장 및 세션 리턴 완료]', C_END)

    # 트위터에 requests 글 작성시에 필요한 queryid 와 token (해당 정보는 크롬 도구(F12) 창의 Network에서 트윗을 작성하였을때 나오는 "CreateTweet" 에서 정보를 얻을 수 있음)
    query_id = "q88fRuxEq8t_M95MIQ53vw"
    bearer_token = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'

    now = datetime.datetime.now()
    title_data = now.strftime('%Y년 %m월 %d일')

    if len(db_data_df) == 0:
        print(f'\n트윗할 url 존재하지 않습니다. ({post_list_csv_path})에 트윗할 url 항목이 존재해야 합니다.')
        return

    # print(data['posturl'][0])
    # print(data['tweet'][0])

    message = ''
    message_check_count = 1
    for idx in range(len(db_data_df)):
        if db_data_df["tweet"].values[idx] == 'O':
            print(
                f'\n{idx + 1}. [SKIP] 해당 ({db_data_df["posturl"].values[idx]})은 이미 백링크가 완료된 리스트입니다. 다음으로 넘어가겠습니다.')
            continue

        message = f"💥 {db_data_df['title'].values[idx]} 🔰 🔰 🔰 {db_data_df['posturl'].values[idx]}"

        print(f'{idx + 1}. {message}')

        url = f'https://twitter.com/i/api/graphql/{query_id}/CreateTweet'
        params = {
            "variables": {
                "tweet_text": message,
                "dark_request": False,
                'media': {
                    'media_entities': [],
                    'possibly_sensitive': False,
                },
                'semantic_annotation_ids': [],
            },
            'features': {
                'tweetypie_unmention_optimization_enabled': True,
                'responsive_web_edit_tweet_api_enabled': True,
                'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
                'view_counts_everywhere_api_enabled': True,
                'longform_notetweets_consumption_enabled': True,
                'responsive_web_twitter_article_tweet_consumption_enabled': False,
                'tweet_awards_web_tipping_enabled': False,
                'longform_notetweets_rich_text_read_enabled': True,
                'longform_notetweets_inline_media_enabled': True,
                'responsive_web_graphql_exclude_directive_enabled': True,
                'verified_phone_label_enabled': False,
                'freedom_of_speech_not_reach_fetch_enabled': True,
                'standardized_nudges_misinfo': True,
                'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
                'responsive_web_media_download_video_enabled': False,
                'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
                'responsive_web_graphql_timeline_navigation_enabled': True,
                'responsive_web_enhance_cards_enabled': False,
            },
            'fieldToggles': {
                'withArticleRichContentState': False,
            },
            "queryId": query_id
        }

        headers = {
            'authority': 'twitter.com',
            'accept': '*/*',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': bearer_token,
            'content-type': 'application/json',
            # 'cookie': '_ga=GA1.2.104180137.1686933068; kdt=ACoXaAj8Zx4czgU0SXn7mgsJ0uxJaQY3JgpNh5KC; g_state={"i_l":0}; lang=en; _gid=GA1.2.1793506001.1688861827; dnt=1; guest_id=v1%3A168891094724921519; guest_id_marketing=v1%3A168891094724921519; guest_id_ads=v1%3A168891094724921519; gt=1678040252852891648; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCIPn7zqJAToMY3NyZl9p%250AZCIlN2QwMTQ3OTdlMGYxZTk2MDgzZGUwNmRmOWMzNTM4NzI6B2lkIiVjZmVk%250AZDgxZTE3ZTQ3MDY4ZDUzN2ExNWE4NmIwMjM5Nw%253D%253D--7dab1e2f27b145acd4f47ab096d61edeae466861; auth_token=10d1384190485edcd8d94d60a2378592dafb23d0; ct0=3228b3c71fc8937414dcce0ba86d8e62b2b5ee27023e38c4b0947a1f0dd72aed19f347aa1581371df0d87f591981d6cf987514768a74e542dd5ef2edef49ab901c6e0a186b1ffc2e2323eb6b238a6b6f; twid=u%3D1669820326572883969; att=1-yItAJhD6loA6BmcZQOaAg29cbfdzsfUlNWwUvR7a; personalization_id="v1_OjUERdLRXwlznWtmCNrHJg=="',
            'origin': 'https://twitter.com',
            'referer': 'https://twitter.com/home',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': fixed_user_agent,
            'x-client-uuid': '90c9b883-a013-48f4-a9c7-8934609f80e4',
            'x-csrf-token': twitter_session.cookies['ct0'],
            'x-twitter-active-user': 'yes',
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-client-language': 'en',
        }

        # print(f'x-csrf-token = > {twitter_session.cookies["ct0"]}')

        with twitter_session as s:
            # contents_info = s.post(url, json=params, headers=headers).json()
            # pp(contents_info)
            res = s.post(url, json=params, headers=headers)
            pp(res.json())
            if res.ok:
                print(f"성공 code:{res.status_code}")
                stmt = update(core_table).where(core_table.c.title == str(db_data_df["title"].values[idx])).values(tweet='O')
                with db.connect() as conn:
                    result = conn.execute(stmt)
                    conn.commit()

            else:
                print(f"실패 code:{res.status_code} reason:{res.reason} msg:{res.text}")
                stmt = update(core_table).where(core_table.c.title == str(db_data_df["title"].values[idx])).values(tweet='X')
                with db.connect() as conn:
                    result = conn.execute(stmt)
                    conn.commit()

        message = ''

        today_date = str(datetime.datetime.now())
        today_date = today_date[:today_date.rfind(
            ':')].replace('-', '.')
        print(f'현재 시간: ', today_date)
        print(
            f'다음 시작 시간: {strftime("%H:%M:%S", gmtime(TWEET_WRITE_WAIT_TIME))} 이후 다시 실행 됩니다.\n')
        sleep(TWEET_WRITE_WAIT_TIME)


def get_cookies_session(driver, url):
    driver.get(url)
    sleep(LOADING_WAIT_TIME)

    _cookies = driver.get_cookies()
    cookie_dict = {}
    for cookie in _cookies:
        cookie_dict[cookie['name']] = cookie['value']
        print(f"{cookie['name']} = {cookie['value']}")

    _session = requests.Session()
    headers = {
        'User-Agent': fixed_user_agent,
    }

    _session.headers.update(headers)
    _session.cookies.update(cookie_dict)  # 응답받은 cookies로  변경
    driver.close()
    driver.quit()

    return _session


def tistory_login(driver):
    driver.get('https://www.tistory.com/auth/login#')
    sleep(LOADING_WAIT_TIME)
    try:
        driver.find_element(By.CLASS_NAME, 'link_profile')
        print(f'\n이미 로그인 되어 다음 과정으로 넘어가겠습니다.')
    except:
        print(f'\n{C_BOLD}{C_RED}{C_BGBLACK}[주의: 3분안에 로그인을 완료해주세요!!!]{C_END}')
        pbar = tqdm(total=LOGIN_WAIT_TIME)
        for x in range(LOGIN_WAIT_TIME):
            sleep(1)
            try:
                driver.find_element(By.CLASS_NAME, 'link_profile')
                break
            except:
                pass
            pbar.update(1)
        pbar.close()


def get_tistory_session():
    try:
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 시작]', C_END)
        driver = init_driver()
        sleep(PAUSE_TIME)
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 완료]', C_END)

        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[로그인 수동 과정 시작(주의 : 3분 이내에 로그인 과정을 끝내야 합니다...)]', C_END)
        tistory_login(driver)
        sleep(PAUSE_TIME)
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[로그인 수동 과정 완료]', C_END)

        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[쿠키값 저장 및 세션 리턴 시작]', C_END)
        tistory_session = get_cookies_session(driver, f'{TISTORY_BLOG_ADDRESS}/manage')
        sleep(PAUSE_TIME)
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[쿠키값 저장 및 세션 리턴 완료]', C_END)

        return tistory_session, True
    except:
        return None, False


def init_session(retry):
    tistory_session = requests.session()
    if not os.path.exists(COOKIES_SAVE_PATH):
        Path(COOKIES_SAVE_PATH).touch(exist_ok=True)

    # 쿠키 불러오기
    if os.path.getsize(COOKIES_SAVE_PATH) > 0 and retry != 1:  # 파일안에 내용이 존재할때
        with open(COOKIES_SAVE_PATH, 'rb') as f:
            cookie_load = pickle.load(f)
        # 새로운 세션 생성
        saved_s = requests.session()

        # 기존에 있던 쿠키 불러오기
        saved_s.cookies.update(cookie_load)
        print(f'\nSaved Session : ', saved_s.cookies.get_dict())
        tistory_session = saved_s
    else:
        print(f'\nEmpty file or Expired Session')
        new_s, result = get_tistory_session()
        print(new_s)
        if result:
            print(f"\nSuccessful creation of new session")
            with open(COOKIES_SAVE_PATH, 'wb') as fc:
                pickle.dump(new_s.cookies, fc)
            print(f'\nNew Session : ', new_s.cookies.get_dict())
            tistory_session = new_s
        else:
            print(f"\nFailed to create a new session or other reason. please try again")
            sys.exit("exit...")

    return tistory_session


def get_tistory_count_info(tistory_session):
    # count : 일일 조회수, 전체 조회수 등을 의미하는 수
    headers = {
        'accept': '*/*',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'priority': 'u=1, i',
        'referer': f'{TISTORY_BLOG_ADDRESS}/manage',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': fixed_user_agent,
    }

    with tistory_session as s:
        response = s.get(
            f'{TISTORY_BLOG_ADDRESS}/manage/statistics/blog/count.json',
            headers=headers,
        )

        if response.ok:
            print(f'\ncount info 얻기 완료 ok code:{response.status_code}')
            try:
                return response.json()['data']['result']['total']
            except requests.exceptions.RequestException as e:
                print("OOps: Something Else", e)
                return None
        else:
            print(
                f"\ncount info 얻기 실패 fail code:{response.status_code} reason:{response.reason} msg:{response.text}")
            return None


def get_category_id(tistory_session):
    if TISTORY_CATEGORY_NAME == '':
        return ''

    headers = {
        'accept': '*/*',
        'accept-language': 'ko,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'priority': 'u=1, i',
        'referer': f'{TISTORY_BLOG_ADDRESS}/manage/category',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': fixed_user_agent,
    }

    with tistory_session as s:
        response = s.get(
            f'{TISTORY_BLOG_ADDRESS}/manage/category.json',
            headers=headers,
        )

        if response.ok:
            print(f'\ncategory info 얻기 완료 ok code:{response.status_code}')
            print(response.text)
            categories_info = response.json()['categories']
            for idx in range(len(categories_info)):
                if categories_info[idx]['name'] == TISTORY_CATEGORY_NAME:
                    _category_id = categories_info[idx]['id']
                    break
            if _category_id is not None:
                print(f'\ncategory id: {_category_id} [{TISTORY_CATEGORY_NAME}]')
                return _category_id
            else:
                print(f'\n입력한 카테고리 정보를 찾을수가 없습니다.')
                sys.exit("exit...")
        else:
            print(f"\ncount info 얻기 실패 fail code:{response.status_code} reason:{response.reason} msg:{response.text}")
            sys.exit("exit...")


def tistory_get_post_lists(tistory_session, db, core_table):

    db_data_df = pd.DataFrame(None)
    sql = 'SELECT * FROM "first"'
    db_data_df = pd.read_sql(sql, db)

    # conn = db.connect()

    # TODO: 메모: TOO MANY~~  이슈 발생시 chrome init() 시에 포트 변경해주기
    headers = {
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'Referer': f'{TISTORY_BLOG_ADDRESS}/manage/posts',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': fixed_user_agent,
        'sec-ch-ua-platform': '"Windows"',
    }

    page_number = 1
    total_post_count = 0
    while True:
        # if page_number > 3:  # 페이지의 가져오는 량을 조절하고 싶다면 여기서 컨트롤하면 가능
        #     break
        with tistory_session as s:
            response = s.get(
                f'{TISTORY_BLOG_ADDRESS}/manage/posts.json?category=-3&page={page_number}&searchKeyword=&searchType=title&visibility=all',
                headers=headers,
            )

            if response.ok:
                print(f'\nall post list 얻기 완료 ok code:{response.status_code}')
                post_info = response.json()
                # pp(post_info)
                if post_info['totalCount'] == 0:
                    print(f'\nno post list')
                    break
                if page_number == 1:
                    divided_portion = post_info['totalCount'] // post_info['count']
                    remainder = post_info['totalCount'] % post_info['count']
                    if remainder == 0:
                        total_pages = divided_portion
                    else:
                        total_pages = divided_portion + 1

                post_lists = []
                for i in range(post_info['count']):
                    temp_dict = {}
                    if post_info['items'][i]['visibility'] == 'PUBLIC':
                        title = post_info['items'][i]['title']
                        link = post_info['items'][i]['permalink']
                        temp_dict['title'] = title
                        temp_dict['posturl'] = link
                        # temp_dict['tweet'] = 'O'
                        print(f'{total_post_count + 1}. {title} | {link}')
                        post_lists.append(temp_dict)  # 엑셀에 저장하기 위한
                        # last_title_lists.append(title)  #
                        total_post_count = total_post_count + 1

                columns = ['title', 'posturl']
                df = pd.DataFrame(post_lists, columns=columns)
                df.insert(2, column='tweet', value='X')

                # print(post_lists)

                db_data_df = db_data_df._append(df)  # pre_df 에 하단으로 df 을 붙여줌
                db_data_df = db_data_df.drop_duplicates(subset=['title'], keep="first")  # (total dataFrame)에서 중복된 행을 제거

                if page_number == total_pages:
                    break
                page_number += 1
            else:
                print(
                    f"\nall post list 얻기 실패 fail code:{response.status_code} reason:{response.reason} msg:{response.text}")
        sleep(PAUSE_TIME)

    with db.connect() as conn:
        result = db_data_df.to_sql(name=core_table.name, con=conn, if_exists='replace', index=False)
        conn.commit()
    # db_data_df.to_sql(name=core_table.name, con=conn, if_exists='replace', index=False)
    # conn.close()

    return db_data_df


# main start
def main():
    try:
        print("\nSTART...")
        start_time = time.time()  # 시작 시간 체크
        now = dt.now()
        print("START TIME : ", now.strftime('%Y-%m-%d %H:%M:%S'))

        print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[DB 연결하기 시작]{C_END}')
        # PostgreSQL과 연결
        db = create_engine(f'{engine_name}://{user_id}:{user_pw}@{host}:{ip}/{db_name}')

        meta = MetaData()

        # 테이블 스키마에 맞게 Column 생성 후 테이블 선언
        core_table = Table(
            'first', meta,
            Column('title', String, primary_key=True),
            Column('posturl', String),
            Column('tweet', String),
        )

        meta.create_all(db)
        print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[DB 연결하기 완료]{C_END}')

        print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[티스토리 세션 정보 초기화 시작]{C_END}')
        tistory_session = init_session(0)
        sleep(PAUSE_TIME)
        print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[티스토리 세션 정보 초기화 완료]{C_END}')

        print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[티스토리 세션 유지 확인 및 다시금 업데이트 시작]{C_END}')
        view_counts = get_tistory_count_info(tistory_session)
        if view_counts is not None:
            print(f'세션이 잘 유지되고 있습니다.')
        else:
            print('세션이 만료되었습니다. 업데이트를 하도록 하겠습니다.')
            tistory_session = init_session(1)
        print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[티스토리 세션 유지 확인 및 다시금 업데이트 완료]{C_END}')

        print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[백링크 대상이 되는 티스토리 리스트를 가져오기 시작]{C_END}')
        db_data_df = tistory_get_post_lists(tistory_session, db, core_table)
        sleep(PAUSE_TIME)
        print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[백링크 대상이 되는 티스토리 리스트를 가져오기 완료]{C_END}')

        print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[본인 트위터 에 백링크 글 쓰기 시작]{C_END}')
        twitter_backlink_post(db_data_df, db, core_table)
        print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[본인 트위터 에 백링크 글 쓰기 완료]{C_END}')

    finally:
        # driver.close()  # 마지막 창을 닫기 위해서는 해당 주석 제거
        # driver.quit()
        end_time = time.time()  # 종료 시간 체크
        ctime = end_time - start_time
        time_list = str(timedelta(seconds=ctime)).split(".")
        print("\n실행시간(초)", ctime)
        print("실행시간 (시:분:초)", time_list)
        print("\nEND...")


# main end
if __name__ == '__main__':
    main()
    # 아래의 schedule 모듈을 사용하면 원하는 시간대에 수행을 시킬 수 있음 지금은 비활성화
    # schedule.every(12).hours.do(main)  # 12시간에 한번씩
    # schedule.every().hour.at(":15").do(main)  # 매시간 42분에 작업 실행
    # schedule.every(10).minutes.do(main)  # 10분에 한번씩
    # schedule.every().day.at('03:00:00').do(main)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
