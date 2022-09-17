from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os, signal
import sqlite3
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def magapoke():
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
  # マガポケのスクレイピングおよびデータベースへの追加
  days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
  driver.get('https://pocket.shonenmagazine.com/series')
  for day in days:
    for i in range(1, 200):
      if driver.find_elements_by_xpath(f'//*[@id="{day}"]/ul/li[{i}]'):
        # タイトルの取得
        title = driver.find_element_by_xpath(f'//*[@id="{day}"]/ul/li[{i}]/a/h4')
        # 著者の取得
        author = driver.find_element_by_xpath(f'//*[@id="{day}"]/ul/li[{i}]/a/h5')
        # 画像URLの取得
        ele = driver.find_element_by_xpath(f'//*[@id="{day}"]/ul/li[{i}]/a/div[1]/img')
        imgurl = ele.get_attribute('src')
        # 取得できているかの確認としてのprint
        print('タイトル:', title.text)
        print("著者:", author.text)
        print("表紙:", imgurl)
        # 詳細ページへ
        detail = driver.find_element_by_xpath(f'//*[@id="{day}"]/ul/li[{i}]/a')
        driver.execute_script('arguments[0].click();', detail)
        
        driver.implicitly_wait(10)

        if driver.find_elements_by_class_name('series-header-description'):
          summary = driver.find_element_by_class_name('series-header-description').text
          print("あらすじ:",summary)
        else:
          None
        
        driver.implicitly_wait(10)
        time. sleep(3)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#page-viewer > section.series-information.type-episode > div.series-contents > div.js-readable-product-list > div.first-readable-product-list.js-first-readable-product-list > ul")))
        # //*[@id="page-viewer"]/section[5]/div[2]/div[2]/div[2]/ul
        for list in range(10):
          # 詳細ページ内のエピソードブロックの確認
          if driver.find_elements_by_xpath(f'//*[@id="page-viewer"]/section[5]/div[2]/div[2]/div[2]/ul/li[{list}]'):
            label = driver.find_element_by_xpath(f'//*[@id="page-viewer"]/section[5]/div[2]/div[2]/div[2]/ul/li[{list}]/a/div[2]/span[2]').text
            
            if label == "無料":
              episode = driver.find_element_by_class_name('series-episode-list-title').text
              print(title.text, author.text, imgurl)
              print(label)
              print(episode)
              print(summary)
            else:
              print()
              None
          else:
            print()
            None
            

        driver.back()

        
        # cur.execute("INSERT INTO magapoke (title, author, img) VALUES(?, ?, ?);", (title.text, author.text, imgurl))
        # conn.commit()
      else:
        print()
        break



  # chromeを開いたままpython seleniumを終了してchromeを開いたままにする
  # os.kill(driver.service.process.pid, signal.SIGTERM)