from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os, signal
import time
import sqlite3

# option addargumentでブラウザ非表示でselenium実行
options = Options()
options.add_argument('--headless')

def bookliveScraping():
  # データベースの接続
  conn = sqlite3.connect('../manga.db')
  cur = conn.cursor()

  cur.execute("CREATE TABLE IF NOT EXISTS origin_booklive")

  # chromeoption=optionsでブラウザ非表示を適用
  driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

  driver.implicitly_wait(10)

  for page in range(1, 110):
    for list in range(1, 85):
      driver.get(f'https://booklive.jp/index/no-charge/category_id/U/page_no/{page}/exadult/1')
      print("page:", page, "list:", list)

      # 表紙
      if driver.find_elements_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/div[1]/div/a/img'):
        ele = driver.find_element_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/div[1]/div/a/img')
        img_url = 'https:' + ele.get_attribute('data-src')
      else: 
        img_url = ''
      print("表紙:", img_url)

      # タイトル
      if driver.find_elements_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/p/a'):
        title = driver.find_element_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/p/a').text
      else:
        title = ''
      print("タイトル:", title)

      # 著者
      if driver.find_elements_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/div[2]'):
        author = driver.find_element_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/div[2]').text
      else:
        author = ''
      print("著者:", author)

      # 詳細ページへ
      if driver.find_elements_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/div[1]/div/a'):
        detail = driver.find_element_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/div[1]/div/a')
        driver.execute_script('arguments[0].click();', detail)
      else:
        None
      driver.implicitly_wait(10)

      # あらすじ
      if driver.find_elements_by_class_name('product_text'):
        summary = driver.find_element_by_class_name('product_text').text
      else:
        summary = ''
      print("あらすじ:", summary)

      # 詳細URLの取得
      cur_url = driver.current_url
      print("詳細URL:", cur_url)
      #is_freeに1
      is_free = 1
      print("無料ですか：", is_free)
      #service_name
      service_name = 'booklive'
      print("サービス名:", service_name)
      #note
      note = ''

      cur.execute("INSERT INTO origin_booklive(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (title, author, img_url, note, summary, is_free, service_name, cur_url))
      conn.commit()
      # 空白
      print()

      driver.back()

      time.sleep(1)

def bookliveRefresh():
  # データベースの接続
  conn = sqlite3.connect('./manga.db')
  cur = conn.cursor()
  #tempテーブルが存在していたら一旦削除
  cur.execute("DROP TABLE IF EXISTS temp_booklive")
  cur.execute("DELETE FROM sqlite_sequence WHERE name = 'temp_booklive';")
  # tempテーブルの作成
  cur.execute("CREATE TABLE temp_booklive('id'INTEGER NOT NULL,'title' TEXT NOT NULL UNIQUE,'author'TEXT,'img_url'TEXT,'note'TEXT,'summary'TEXT,'is_free'INTEGER,'service_name'TEXT,'cur_url'TEXT,PRIMARY KEY('id'))")
  
  # tempテーブルにコピー
  cur.execute("INSERT INTO temp_booklive SELECT id, title, author, img_url, note, summary, is_free, service_name, cur_url FROM origin_booklive")
  #tempテーブルが存在していたら一旦削除
  cur.execute("DROP TABLE IF EXISTS new_booklive")
  cur.execute("DELETE FROM sqlite_sequence WHERE name = 'temp_booklive';")
  # newテーブルの作成(titleのUNIQUEはずす)
  cur.execute("CREATE TABLE new_booklive('title' TEXT NOT NULL, 'author' TEXT, 'img_url' TEXT, 'note' TEXT, 'summary' TEXT, 'is_free' INTEGER, 'service_name' TEXT, 'cur_url' TEXT)")

  # chromeoption=optionsでブラウザ非表示を適用
  driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
  driver.implicitly_wait(10)

  for page in range(1, 110):
    for list in range(1, 85):
      driver.get(f'https://booklive.jp/index/no-charge/category_id/U/page_no/{page}/exadult/1')
      print("page:", page, "list:", list)
      
      # 表紙
      if driver.find_elements_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/div[1]/div/a/img'):
        ele = driver.find_element_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/div[1]/div/a/img')
        img_url = 'https:' + ele.get_attribute('data-src')
      else: 
        img_url = ''
      print("表紙:", img_url)

      # タイトル
      if driver.find_elements_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/p/a'):
        title = driver.find_element_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/p/a').text
      else:
        title = ''
      print("タイトル:", title)

      # 著者
      if driver.find_elements_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/div[2]'):
        author = driver.find_element_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/div[2]').text
      else:
        author = ''
      print("著者:", author)

      # 詳細ページへ
      if driver.find_elements_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/div[1]/div/a'):
        detail = driver.find_element_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/div[1]/div/a')
        driver.execute_script('arguments[0].click();', detail)
      else:
        None
      driver.implicitly_wait(10)

      # あらすじ
      if driver.find_elements_by_class_name('product_text'):
        summary = driver.find_element_by_class_name('product_text').text
      else:
        summary = ''
      print("あらすじ:", summary)

      # 詳細URLの取得
      cur_url = driver.current_url
      print("詳細URL:", cur_url)
      #is_freeに1
      is_free = 1
      print("無料ですか：", is_free)
      #service_name
      service_name = 'booklive'
      print("サービス名:", service_name)

      note = ''

      # tempテーブルに追加または更新
      cur.execute("INSERT INTO temp_booklive(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (title) DO UPDATE SET title = title, author = author, img_url = img_url, note = note, summary = summary, is_free = is_free, service_name = service_name, cur_url = cur_url ;", (title, author, img_url, note, summary, is_free, service_name, cur_url))
      conn.commit()

      # 最新テーブルに追加
      cur.execute("INSERT INTO new_booklive(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (title, author, img_url, note, summary, is_free, service_name, cur_url))
      conn.commit()
      # 空白
      print()
      driver.back()

      driver.implicitly_wait(10)
  # 仮テーブルと更新テーブルの比較をして更新テーブルにないマンガを削除
  cur.execute("DELETE FROM temp_booklive WHERE title IN (SELECT temp_booklive.title FROM temp_booklive LEFT OUTER JOIN new_booklive ON temp_booklive.title = new_booklive.title WHERE new_booklive.title IS NULL)")

  # オリジナルのテーブルを削除
  cur.execute("DROP TABLE origin_booklive")

  # オリジナルのテーブルに名前を変更
  cur.execute("ALTER TABLE temp_booklive RENAME TO origin_booklive;")
  conn.commit()
  # Newテーブルの削除
  cur.execute("DROP TABLE new_booklive;")
  conn.commit()

  #削除済みテーブル分のデータ削除
  cur.execute("VACUUM;")
