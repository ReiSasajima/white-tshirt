from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os, signal
import time
import sqlite3

# option addargumentでブラウザ非表示でselenium実行
options = Options()
options.add_argument('--headless')

freeJumpplus = 'https://shonenjumpplus.com/series'

def jumpplusScraping():
  # データベースの接続
  conn = sqlite3.connect('../manga.db')
  cur = conn.cursor()

  # chromeoption=optionsでブラウザ非表示を適用
  driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
  driver.implicitly_wait(10)

  # ジャンプ+連載一覧へ
  driver.get(freeJumpplus)
  # ulが曜日、liがマンガごと
  for day in range(1, 9):
    for list in range(1, 40):
      if driver.find_elements_by_xpath(f'//*[@id="page-jumpPlus-series-list"]/article/ul[{day}]/li[{list}]'):
        print("曜日:",day)
        print("list:", list)
        # タイトル
        title  = driver.find_element_by_xpath(f'//*[@id="page-jumpPlus-series-list"]/article/ul[{day}]/li[{list}]/a/h2').text
        print("作品名:",title)
        # 著者
        author = driver.find_element_by_xpath(f'//*[@id="page-jumpPlus-series-list"]/article/ul[{day}]/li[{list}]/a/h3').text
        print("著者:", author)
        # 表紙
        img_url = driver.find_element_by_xpath(f'//*[@id="page-jumpPlus-series-list"]/article/ul[{day}]/li[{list}]/a/div/img').get_attribute('src')
        print("表紙:", img_url)
        #備考欄
        note = ''
        #is_freeに1
        is_free = 1
        print('無料ですか:', is_free)
        #サービス名
        service_name = 'jumpplus'
        print('サービス名:', service_name)
        # 詳細ページ
        detail = driver.find_element_by_xpath(f'//*[@id="page-jumpPlus-series-list"]/article/ul[{day}]/li[{list}]/a')
        driver.execute_script('arguments[0].click();', detail)
        driver.implicitly_wait(10)

        # 詳細URL
        cur_url = driver.current_url
        print("URL:", cur_url)

        if driver.find_elements_by_class_name('series-header-description'):
          # あらすじ
          summary = driver.find_element_by_class_name('series-header-description').text
        else:
          summary = ''
        print("あらすじ:", summary)

        cur.execute("INSERT INTO origin_jumpplus(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (title, author, img_url, note, summary, is_free, service_name, cur_url))
        conn.commit()
        driver.back()

        driver.implicitly_wait(10)
      else:
        break

def jumpplusRefresh():

  # データベースの接続
  conn = sqlite3.connect('../manga.db')
  cur = conn.cursor()
  #tempテーブルが存在していたら一旦削除
  cur.execute("DROP TABLE IF EXISTS temp_jumpplus")
  cur.execute("DELETE FROM sqlite_sequence WHERE name = 'temp_jumpplus';")
  # tempテーブルの作成
  cur.execute("CREATE TABLE temp_jumpplus('id'INTEGER NOT NULL,'title' TEXT NOT NULL UNIQUE,'author'TEXT,'img_url'TEXT,'note'TEXT,'summary'TEXT,'is_free'INTEGER,'service_name'TEXT,'cur_url'TEXT,PRIMARY KEY('id'))")
  
  # tempテーブルにコピー
  cur.execute("INSERT INTO temp_jumpplus SELECT id, title, author, img_url, note, summary, is_free, service_name, cur_url FROM origin_jumpplus")
  #tempテーブルが存在していたら一旦削除
  cur.execute("DROP TABLE IF EXISTS new_jumpplus")
  cur.execute("DELETE FROM sqlite_sequence WHERE name = 'temp_jumpplus';")
  # newテーブルの作成(titleのUNIQUEはずす)
  cur.execute("CREATE TABLE new_jumpplus('title' TEXT NOT NULL, 'author' TEXT, 'img_url' TEXT, 'note' TEXT, 'summary' TEXT, 'is_free' INTEGER, 'service_name' TEXT, 'cur_url' TEXT)")

  # chromeoption=optionsでブラウザ非表示を適用
  driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
  driver.implicitly_wait(10)

  # ジャンプ+連載一覧へ
  driver.get(freeJumpplus)
  # ulが曜日、liがマンガごと
  for day in range(1, 9):
    for list in range(1, 40):
      if driver.find_elements_by_xpath(f'//*[@id="page-jumpPlus-series-list"]/article/ul[{day}]/li[{list}]'):
        print("曜日:",day)
        print("list:", list)
        # タイトル
        title  = driver.find_element_by_xpath(f'//*[@id="page-jumpPlus-series-list"]/article/ul[{day}]/li[{list}]/a/h2').text
        print("作品名:",title)
        # 著者
        author = driver.find_element_by_xpath(f'//*[@id="page-jumpPlus-series-list"]/article/ul[{day}]/li[{list}]/a/h3').text
        print("著者:", author)
        # 表紙
        img_url = driver.find_element_by_xpath(f'//*[@id="page-jumpPlus-series-list"]/article/ul[{day}]/li[{list}]/a/div/img').get_attribute('src')
        print("表紙:", img_url)
        #備考欄
        note = ''
        #is_freeに1
        is_free = 1
        print('無料ですか:', is_free)
        #サービス名
        service_name = 'jumpplus'
        print('サービス名:', service_name)
        # 詳細ページ
        detail = driver.find_element_by_xpath(f'//*[@id="page-jumpPlus-series-list"]/article/ul[{day}]/li[{list}]/a')
        driver.execute_script('arguments[0].click();', detail)
        driver.implicitly_wait(10)

        # 詳細URL
        cur_url = driver.current_url
        print("URL:", cur_url)

        if driver.find_elements_by_class_name('series-header-description'):
          # あらすじ
          summary = driver.find_element_by_class_name('series-header-description').text
        else:
          summary = ''
        print("あらすじ:", summary)

        # tempテーブルに追加または更新
        cur.execute("INSERT INTO temp_jumpplus(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (title) DO UPDATE SET title = title, author = author, img_url = img_url, note = note, summary = summary, is_free = is_free, service_name = service_name, cur_url = cur_url ;", (title, author, img_url, note, summary, is_free, service_name, cur_url))
        conn.commit()

        # 最新テーブルに追加
        cur.execute("INSERT INTO new_jumpplus(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (title, author, img_url, note, summary, is_free, service_name, cur_url))
        conn.commit()
        driver.back()

        driver.implicitly_wait(10)
      else:
        break
  # 仮テーブルと更新テーブルの比較をして更新テーブルにないマンガを削除
  cur.execute("DELETE FROM temp_jumpplus WHERE title IN (SELECT temp_jumpplus.title FROM temp_jumpplus LEFT OUTER JOIN new_jumpplus ON temp_jumpplus.title = new_jumpplus.title WHERE new_jumpplus.title IS NULL)")

  # オリジナルのテーブルを削除
  cur.execute("DROP TABLE origin_jumpplus")

  # オリジナルのテーブルに名前を変更
  cur.execute("ALTER TABLE temp_jumpplus RENAME TO origin_jumpplus;")
  conn.commit()
  # Newテーブルの削除
  cur.execute("DROP TABLE new_jumpplus;")
  conn.commit()

  #削除済みテーブル分のデータ削除
  cur.execute("VACUUM;")