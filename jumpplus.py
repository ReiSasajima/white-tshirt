from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os, signal
import time
import sqlite3

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

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
# ジャンプ+連載一覧へ
driver.get('https://shonenjumpplus.com/series')
# ulが曜日、liがマンガごと
for day in range(1, 9):
  for list in range(1, 40):
    if driver.find_elements_by_xpath(f'//*[@id="page-jumpPlus-series-list"]/article/ul[{day}]/li[{list}]'):
      title  = driver.find_element_by_xpath(f'//*[@id="page-jumpPlus-series-list"]/article/ul[{day}]/li[{list}]/a/h2').text
      imgurl = driver.find_element_by_xpath(f'//*[@id="page-jumpPlus-series-list"]/article/ul[{day}]/li[{list}]/a/div/img').get_attribute('src')
      print(day, list, title, imgurl)
      time.sleep(1)
    else:
      break




# もっと見るボタンの確認と押下
# if driver.find_elements_by_xpath('//*[@id="page-viewer"]/section[5]/div[2]/div[2]/section/button'):
#     moreBtn = driver.find_element_by_xpath('//*[@id="page-viewer"]/section[5]/div[2]/div[2]/section/button')
#     driver.execute_script('arguments[0].click();', moreBtn)
# else:
#   None
# # 漫画のliがあるか
# if driver.find_elements_by_xpath('//*[@id="page-viewer"]/section[5]/div[2]/div[2]/div[2]/ul/li[1]'):
#   # メモ書きがあるか
#   if driver.find_element_by_xpath('//*[@id="page-viewer"]/section[5]/div[2]/div[2]/div[2]/ul/li[1]/a/div[2]/span[2]'):
#     # メモ書きがあれば、文言が無料かどうか
#     note = driver.find_element_by_xpath('//*[@id="page-viewer"]/section[5]/div[2]/div[2]/div[2]/ul/li[1]/a/div[2]/span[2]').text
#     if note == '無料':
#       # タイトルの取得
#       title = driver.find_element_by_xpath('//*[@id="page-viewer"]/section[5]/div[2]/div[2]/div[2]/ul/li[1]/a/div[2]/h4')
#       # 表紙の獲得
#       imgurl = driver.find_element_by_xpath('//*[@id="page-viewer"]/section[5]/div[1]/div[1]/img').get_attribute('src')
#       print(title, imgurl)
#     else:
#       None
#   else:
#     None
# else:
#   None







