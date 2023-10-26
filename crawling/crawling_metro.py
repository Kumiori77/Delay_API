import requests
import pandas as pd
import numpy as np
# import DB
import re
from datetime import datetime
from bs4 import BeautifulSoup
from . import metro_function as mf
from . import getTitle as GT

def search():
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    url = "http://www.seoulmetro.co.kr/kr/board.do?menuIdx=546"
    response = requests.get(url=url, headers=hdr)

    # urlList, titleList = new_file.get_url(response)  # response 값을 전달
    titleList, urlList = GT.getTitle_Sel() # response 값을 전달
    # print(urlList)
    # print(titleList)

    # urlList = ["http://www.seoulmetro.co.kr/kr/board.do?menuIdx=546&bbsIdx=2216084"]
    # 'http://www.seoulmetro.co.kr/kr/board.do?menuIdx=546&bbsIdx=2216084'
    # "http://www.seoulmetro.co.kr/kr/board.do?menuIdx=546&bbsIdx=2216084"
    # titleList = ["aaa", "bbb"]

    for i in range(len(urlList)):
        maintext = mf.get_mainText(str(urlList[i]))
        start, end = mf.start_end_date_sel(maintext)
        number = mf.read_station_csv_file(maintext)
        mf.go_DB(titleList[i], start, end, number, maintext, str(urlList[i]))

# search()