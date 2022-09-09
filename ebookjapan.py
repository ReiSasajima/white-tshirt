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

for page in range(1, 118):
  driver.get(f'https://ebookjapan.yahoo.co.jp/free/books/?useTitle=1&page={page}')
  for list in range(1, 59):
    if driver.find_elements_by_xpath(f'//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul/li[{list}]'):
      # 表紙
      ele = driver.find_element_by_xpath(f'//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul/li[{list}]/div/a/div[1]/img')
      imgurl = ele.get_attribute('data-src')
      # タイトル
      title = driver.find_element_by_xpath(f'//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul/li[{list}]/div/a/div[2]/p').text
      note  = driver.find_element_by_xpath(f'//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul/li[{list}]/div/div/a').text
      if "無料" in note:
        print(page, list, title)
        print(imgurl)
        # 詳細ページへ
        detail = driver.find_element_by_xpath(f'//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul/li[{list}]/div/a')
        driver.execute_script('arguments[0].click();', detail)

        driver.implicitly_wait(5)
        # 作者
        author = driver.find_element_by_xpath('//*[@id="wrapper"]/div[4]/div[1]/div/div[1]/div/div[1]/div[3]/p[1]/a').text
        print(author)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.implicitly_wait(5)
        # あらすじ
        # summary = driver.find_element_by_class_name('overview__summary').text
        # print(summary)
        # ブラウザバック
        driver.back()

        time.sleep(1)
      else:
        time.sleep(1)
        None

    else:
      print()
      break