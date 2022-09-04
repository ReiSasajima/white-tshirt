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
driver.maximize_window()

for j in range(0, 3):
  # ３冊以上無料→２冊丸ごと無料、1冊まるごと無料の順番で回る
  driver.get(f'https://piccoma.com/web/more/product/list/T/F/{j}/K')
  # 件数を取得
  number = driver.find_element_by_xpath('//*[@id="js_headerNav"]/h1/span[2]').text
  # 「）」「（」を取り除いく
  page = number.strip('（').strip('）')
  # pageの文字列を数値に変換
  for i in range(1, int(page)+1):
    if driver.find_elements_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]'):
      # タイトルの取得
      title = driver.find_element_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]/a/div/div/div[2]/span').text
      # 画像URLの取得
      ele = driver.find_element_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]/a/div/div/div[1]/img')
      imgurl = ele.get_attribute('src')
      # 期間限定、無料枠などの情報取得
      note = driver.find_element_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]/a/div/div/p/span').text
      # 取得できているか確認のためのprint
      print(i, title, note, imgurl)
      # スクレイピングでBANされないためのsleep
      time.sleep(0.5)
      # スクロールしないと全てのliが表示されないためのスクロール
      driver.execute_script("window.scrollBy(0, 200);")
    else:
      print()
      break

