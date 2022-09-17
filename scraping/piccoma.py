from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os, signal
import time
import sqlite3

# def piccoma():
# データベースの接続
conn = sqlite3.connect('../manga.db')
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
  # スクロールする
  scrolls = 1
  # ３冊以上無料→２冊丸ごと無料、1冊まるごと無料の順番で回る
  driver.get(f'https://piccoma.com/web/more/product/list/T/F/{j}/K')
  # 件数を取得
  number = driver.find_element_by_xpath('//*[@id="js_headerNav"]/h1/span[2]').text
  # 「）」「（」「,」を取り除く
  page = number.strip('（）').replace(',', '')
  # pageの文字列を数値に変換
  for i in range(1, int(page)+1):
    if driver.find_elements_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]'):
      # タイトルの取得
      title = driver.find_element_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]/a/div/div/div[2]/span').text
      # 画像URLの取得
      ele = driver.find_element_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]/a/div/div/div[1]/img')
      img_url = ele.get_attribute('src')
      # 期間限定、無料枠などの情報取得
      note = driver.find_element_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]/a/div/div/p/span').text
      # 取得できているか確認のためのprint
      print(i, title, note, img_url)
      # 漫画リストのクリック(詳細ページへ)
      detail  = driver.find_element_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]/a')
      driver.execute_script('arguments[0].click();', detail)
      # 著者名の取得
      author = driver.find_element_by_xpath('//*[@id="js_author"]/li/a').text
      # あらすじの取得
      summary = driver.find_element_by_xpath('//*[@id="js_productDesc"]/p').text
      # 詳細URLの取得
      cur_url = driver.current_url
      # サービス名の取得
      service_name = 'piccoma'
      # is_freeをtrue(1)にする
      is_free = 1

      print(author, summary)

      cur.execute("INSERT INTO origin_piccoma(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (title, author, img_url, note, summary, is_free, service_name, cur_url))
      conn.commit()

      # ブラウザ戻る
      driver.back()
      # スクレイピングでBANされないためのsleep
      time.sleep(1)
      driver.implicitly_wait(10)
      # スクロールしないと全てのliが表示されないためのスクロール
      # driver.execute_script("window.scrollBy(0, 1000);")
      for scroll in range(scrolls+1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.2)

      scrolls += 1
    else:
      print()
      break

# chromeを開いたままpython seleniumを終了してchromeを開いたままにする
# os.kill(driver.service.process.pid, signal.SIGTERM)