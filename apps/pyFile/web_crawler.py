from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
def crawling():
    # 브라우저 꺼짐 방지 옵션
    download_dir = os.path.abspath("./hwpFile")

    # 브라우저 꺼짐 방지 옵션 및 다운로드 경로 설정
    chrome_options = Options()
    #헤드리스모드(크롤링시 나오는 gui 안나오게)
    chrome_options.add_argument('--headless')
    chrome_options.add_experimental_option("detach", True)
    prefs = {'download.default_directory': download_dir}
    chrome_options.add_experimental_option('prefs', prefs)

    driver = webdriver.Chrome(options=chrome_options)
    #가정통신문
    # https://smc.sen.hs.kr/19805/subMenu.do
    #가정통신문(교육청)
    #https://smc.sen.hs.kr/193373/subMenu.do

    # 웹페이지 해당 주소 이동
    driver.get("https://smc.sen.hs.kr/19805/subMenu.do")

    # //*[@id="board_area"]/table/tbody/tr[2]/td[2]/a
    # //*[@id="board_area"]/table/tbody/tr[3]/td[2]/a

    time.sleep(4)  # 페이지 로드를 위한 대기
    try:
        for i in range(6,16,1):
            print()
            button = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div/form/div[2]/table/tbody/tr[{i}]/td[2]/a')  # XPath를 통해 요소 찾기
            button.click()  # 요소 클릭
            time.sleep(3)
            driver.find_element(By.XPATH, '//*[@id="fileListTable"]/tbody/tr/td[5]/a[1]').click()
            time.sleep(2)
            driver.refresh()
            print(i)
    finally:
        print('끝')

# crawling()