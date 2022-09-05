from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os, signal
import time
import sqlite3

# データベースの接続
conn = sqlite3.connect('manga.db')
cur = conn.cursor()

# option addargumentでブラウザ非表示でselenium実行
options = Options()
options.add_argument('--headless')

# chromeoption=optionsでブラウザ非表示を適用
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(10)

for page in range(1, 110):
  for list in range(1, 85):
    driver.get(f'https://booklive.jp/index/no-charge/category_id/U/page_no/{page}/exadult/1')
    ele = driver.find_element_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/div[1]/div/a/img')
    imgurl = 'https:' + ele.get_attribute('data-src')
    title = driver.find_element_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/p/a').text
    print(list, title, imgurl)
    time.sleep(1)


# chromeウィンドウを閉じる
# driver.close()