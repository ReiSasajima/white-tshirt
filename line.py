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

driver.get('https://manga.line.me/periodic/gender_ranking?gender=0')

list = 1
while driver.find_elements_by_xpath(f'/html/body/div[1]/div/div[2]/div/section/div/ol/li[{list}]'):
  title = driver.find_element_by_xpath(f'/html/body/div[1]/div/div[2]/div/section/div/ol/li[{list}]/a/span[2]').text
  imgurl = driver.find_element_by_xpath(f'/html/body/div[1]/div/div[2]/div/section/div/ol/li[{list}]/a/div/img').get_attribute('src')
  print(list, title, imgurl)
  list += 1
  # スクロールしないと全てのliが表示されないためのスクロール
  driver.execute_script("window.scrollBy(0, 200);")
  time.sleep(1)

