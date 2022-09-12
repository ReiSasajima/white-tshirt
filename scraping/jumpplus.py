from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os, signal
import time
import sqlite3

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
def jumpplus():
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
        # タイトル
        title  = driver.find_element_by_xpath(f'//*[@id="page-jumpPlus-series-list"]/article/ul[{day}]/li[{list}]/a/h2').text
        # 著者
        author = driver.find_element_by_xpath(f'//*[@id="page-jumpPlus-series-list"]/article/ul[{day}]/li[{list}]/a/h3').text
        # 表紙
        imgurl = driver.find_element_by_xpath(f'//*[@id="page-jumpPlus-series-list"]/article/ul[{day}]/li[{list}]/a/div/img').get_attribute('src')
        print(day, list, title, author, imgurl)

        detail = driver.find_element_by_xpath(f'//*[@id="page-jumpPlus-series-list"]/article/ul[{day}]/li[{list}]/a')
        driver.execute_script('arguments[0].click();', detail)
        if driver.find_elements_by_class_name('series-header-description'):
          # あらすじ
          summary = driver.find_element_by_class_name('series-header-description').text
          print(summary)
        else:
          None

        driver.back()

        time.sleep(1)
      else:
        break







