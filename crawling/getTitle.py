
# 셀레니움
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from datetime import datetime


def getTitle_Sel():
    URL = "http://www.seoulmetro.co.kr/kr/board.do?menuIdx=546"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(URL)
    x_path = ['//*[@id="contents"]/div[2]/table/tbody/tr[', ']/td[2]/a']
    nextList = "#contents > div.paging-area > a:nth-child("

    try:
        run = True
        running = True
        i = 1
        pg = 1
        nextbtn = 4
        dataList = []
        urlList = []

        while run:
            while running:

                date = driver.find_element(by=By.XPATH, value='//*[@id="contents"]/div[2]/table/tbody/tr[' + str(i) +']/td[4]')

                date = date.text

                gno = driver.find_element(by=By.XPATH, value='//*[@id="contents"]/div[2]/table/tbody/tr[' + str(i) + ']/td[1]')
                if gno.text == "NOTICE":
                    a = False
                else :
                    a = True

                # print(date)  

                if checkDate(date) == 2 and a:
                    run = False
                    running = False
                if checkDate(date) == 0 or checkDate(date) == 1 and a:
                
                    #contents > div.tbl-box1 > table > tbody > tr:nth-child(1) > td.num.t-disn.bd1
                
                    # 제목 수집
                    title = driver.find_element(by=By.XPATH, value=x_path[0] + str(i) + x_path[1])

                    if "시위" in title.text or "집회" in title.text or "지연" in title.text:
                        data = title.text
                        url = title.get_attribute("href")
                        dataList.append(data)
                        urlList.append(url)
                    
                # 페이지 번호가 1일때만 11개 나머지는 10개씩 보기
                if pg == 1 and i == 11:
                    i = 1
                    break
                elif i == 10:
                    i = 1
                    break
                i += 1
            # 마지막 페이지이면 next 버튼 누르고 버튼 번호 초기화
            if nextbtn == 13:
                ok = driver.find_element(by=By.CSS_SELECTOR, value="#contents > div.paging-area > a.btn_next")
                ok.click()
                nextbtn = 4
            else :
                # 다음 페이지 번호 클릭
                sel = nextList+str(nextbtn)+")"
                ok = driver.find_element(by=By.CSS_SELECTOR, value=sel)
                ok.click()  
                nextbtn+= 1
            pg += 1
        return dataList, urlList
            

    except Exception:
        print("error")
        pass


# 날짜 비교
def checkDate(text):
    # datetime 타입으로 변환 
    date = datetime.strptime(text, "%Y-%m-%d")
    today = datetime.now()
    # today = datetime.strptime("2023-04-28", "%Y-%m-%d")

    if today == date:
        return 0
    elif  today < date:
        return 1
    else :
        return 2
    
# 고정 공지인지 확인
def checkGno(driver, i):
    gno = driver.find_element(by=By.XPATH, value='//*[@id="contents"]/div[2]/table/tbody/tr[' + str(i) + ']/td[1]')
    if gno.text == "NOTICE":
        return False
    else :
        return True
    


# if __name__ == "__main__":
#     a, b = getTitle_Sel()
#     print(a)
#     print(b)
    