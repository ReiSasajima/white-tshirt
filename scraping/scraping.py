from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os, signal
import sqlite3
import time


# データベースの接続
conn = sqlite3.connect('../manga.db')
cur = conn.cursor()

# tempテーブルの作成
# cur.execute("CREATE TABLE temp_magapoke('id'INTEGER NOT NULL,'title' TEXT NOT NULL,'author'TEXT,'img_url'TEXT,'note'TEXT,'summary'TEXT,'is_free'INTEGER,'service_name'TEXT,'cur_url'TEXT,PRIMARY KEY('id' AUTOINCREMENT))")

# # newテーブルの作成
# cur.execute("CREATE TABLE new_magapoke('id' INTEGER NOT NULL, 'title' TEXT NOT NULL, 'author' TEXT, 'img_url' TEXT, 'note' TEXT, 'summary' TEXT, 'is_free' INTEGER, 'service_name' TEXT, 'cur_url' TEXT, PRIMARY KEY('id' AUTOINCREMENT))")

# # 仮テーブルにコピー
# cur.execute("INSERT INTO temp_magapoke SELECT id, title, author, img_url, note, summary, is_free, service_name, cur_url FROM origin_magapoke")


options = Options() #option addargumentでブラウザ非表示でselenium実行
options.add_argument('--headless')

# chromeoption=optionsでブラウザ非表示を適用
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(10)
# マガポケのスクレイピング

days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
driver.get('https://pocket.shonenmagazine.com/series')
for day in days:
  for i in range(1, 200):
    if driver.find_elements_by_xpath(f'//*[@id="{day}"]/ul/li[{i}]'):
      # タイトルの取得
      title = driver.find_element_by_xpath(f'//*[@id="{day}"]/ul/li[{i}]/a/h4').text
      # 著者の取得
      author = driver.find_element_by_xpath(f'//*[@id="{day}"]/ul/li[{i}]/a/h5').text
      # 画像URLの取得
      ele = driver.find_element_by_xpath(f'//*[@id="{day}"]/ul/li[{i}]/a/div[1]/img')
      img_url = ele.get_attribute('src')
      # サービス名の取得
      service_name = 'magapoke'
      # is_freeをtrue(1)にする
      is_free = 1

      print(day, i)
      # 取得できているかの確認としてのprint
      print('タイトル:', title)
      print("著者:", author)
      print("表紙:", img_url)
      print('サービス名:', service_name)
      print("無料ですか？", is_free)
      # 詳細ページへ
      detail = driver.find_element_by_xpath(f'//*[@id="{day}"]/ul/li[{i}]/a')
      driver.execute_script('arguments[0].click();', detail)
      time.sleep(1)
      driver.implicitly_wait(10)
      
      # 詳細URLの取得
      cur_url = driver.current_url

      #あらすじ
      if driver.find_elements_by_class_name('series-header-description'):
        summary = driver.find_element_by_class_name('series-header-description').text
        print("あらすじ:",summary)
      else:
        None
      
      driver.back()

      # tempテーブルに追加または更新
      # cur.execute("INSERT OR REPLACE INTO temp_magapoke(title, author, img_url, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?);", (title, author, img_url, summary, is_free, service_name, cur_url))
      # conn.commit()

      # # 最新テーブルに追加
      # cur.execute("INSERT INTO new_magapoke(title, author, img_url, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?);", (title, author, img_url, summary, is_free, service_name, cur_url))
      # conn.commit()

      cur.execute("INSERT INTO origin_magapoke(title, author, img_url, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?);", (title, author, img_url, summary, is_free, service_name, cur_url))
      conn.commit()

      time.sleep(1)
      print()
    else:
      print()
      break

# 仮テーブルと更新テーブルの比較をして更新テーブルにないマンガを削除
# cur.execute("DELETE * FROM temp_magapoke LEFT OUTER JOIN new_magapoke ON temp_magapoke.title = new_magapoke.title WHERE new_magapoke.title IS NULL")

# オリジナルのテーブルに名前を変更
# cur.execute("ALTER TABLE temp_magapoke RENAME TO origin_magapoke;")
# cur.execute("DROP TABLE temp_magapoke;")
# cur.execute("DROP TABLE new_magapoke;")
# conn.commit()

  # chromeを開いたままpython seleniumを終了してchromeを開いたままにする
  # os.kill(driver.service.process.pid, signal.SIGTERM)