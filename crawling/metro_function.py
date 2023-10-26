import requests
import pandas as pd
import numpy as np
from . import dateGetter as DG
from datetime import datetime
from bs4 import BeautifulSoup
from django.db.models import Q
from api.models import Delay

RealTitle = ""
number = []

url2 = ""
title = ""
maintext = ""

text = ""
date_list = []

def get_url(response):  # response 변수를 매개변수로 추가
    global url2
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        today = datetime.now()
        # today = "2023-04-28"
        today = datetime.strptime(today, "%Y-%m-%d")

        urlList = []
        titleList = []

        for i in range(1, 11):
            title = soup.select_one('#contents > div.tbl-box1 > table > tbody > tr:nth-child(' + str(i) + ') > td.td-lf.bd2 > a')
            day = soup.select_one('#contents > div.tbl-box1 > table > tbody > tr:nth-child(' + str(i) + ') > td.t-disn.bd5')

            day = datetime.strptime(day.get_text(), "%Y-%m-%d")
            # print(day)
            if today == day:
                # print("오늘")
                text = title.get_text()
                RealTitle = text
                # jiyeon = ['급경사', '회계', '안전', '집회']
                if '시위' in text or '집회' in text or '지연' in text:
                    # print(text)
                    # print(title['href'])
                    titleList.append(RealTitle)
                    url2 = "http://www.seoulmetro.co.kr/kr/" + title['href']
                    urlList.append(url2)

        return urlList, titleList,

def get_mainText(url):
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    response = requests.get(url=url, headers=hdr)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # 제목
        title = soup.select_one('#board-top > article > div > table > tbody > tr:nth-child(3) > td > div.textarea-area > div')

        # 본문
        maintext = title.text
        # print("maintext : " + maintext)
        return maintext

def start_end_date_sel(maintext):

    date_list = []
    date_list = DG.get_date(maintext, date_list)
    DG.check_year(date_list)
    # print(date_list)

    if len(date_list) > 0:
        start = date_list[0]
        if len(date_list) == 1:
            end = date_list[0]
        else:
            end = date_list[-1]
        return start, end
    else :
        return "", ""

def read_station_csv_file(maintext):
    number = []
    df1 = pd.read_csv('stationNumber.csv', encoding='cp949')
    stations = np.array(df1['station'])
    numbers = np.array(df1['number'])

    for i in range(len(stations)):
        if stations[i] in maintext:
            number.append(numbers[i])
    return number

def go_DB(RealTitle, start, end, number, maintext, url):
    # data = [RealTitle, start, end, number, maintext, url]
    
    # 이미 있는 데이터인지 확인하기
    q = Q(title=RealTitle, start=start, end=end)
    old_data = Delay.objects.filter(q)

    if len(old_data) > 0:
        # print("데이터 있음")
        pass

    else :
        # print("데이터 없음")   
        for num in number:
            sql = Delay(title=RealTitle, start=start, end=end, number=num, text=maintext, link=url)
            sql.full_clean()
            sql.save() 



# if __name__ == "__main__":
#     # s, e = start_end_date_sel("서울교통공사에서 알려드립니다. 2023.8.23.(수) 19:30 부터 22:00까지(예정) 시청역에서 「전국장애인차별철폐연대」의 시위가 예정되어 있습니다. 이로 인해 시위가 발생한 해당구간 열차운행이 상당시간 지연될 수 있으며, 상황에 따라 해당역을 무정차 통과할 예정이오니, 이점 참고하여 열차를 이용해 주시기 바랍니다. ")
#     s, e = start_end_date_sel("2022-11-22 13:00~ 2024-11-21 09:00")
#     print(s)
#     print(e)
#     print(type(s))