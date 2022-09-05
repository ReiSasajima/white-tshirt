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
# やんじゃん！無料キャンペーンサイト
driver.get('https://ynjn.jp/titles/feature/?d=193')
num = driver.find_element_by_xpath('//*[@id="layout"]/div/section/div/div[2]/div/div').text
num = int(num.strip('件'))
for list in range(1, num+1):
  title = driver.find_element_by_xpath(f'//*[@id="layout"]/div/section/div/div[2]/div/ul/li[{list}]/div/a/div/div[2]').text
  imgurl = driver.find_element_by_xpath(f'//*[@id="layout"]/div/section/div/div[2]/div/ul/li[{list}]/div/a/div/div[1]/img').get_attribute('src')
  print(title, imgurl)
  time.sleep(1)
