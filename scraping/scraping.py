from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os, signal
import sqlite3
import time

def scraping():
  # データベースの接続
  conn = sqlite3.connect('manga.db')
  cur = conn.cursor()
  
  cur.execute("CREATE TABLE temp_magapoke(id integer, title text, author text,  ")
  # cur.execute("INSERT INTO magapoke (title, author, img) VALUES(?, ?, ?);", (title.text, author.text, imgurl))
        # conn.commit()
  # option addargumentでブラウザ非表示でselenium実行
  options = Options()
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
        title = driver.find_element_by_xpath(f'//*[@id="{day}"]/ul/li[{i}]/a/h4')
        # 著者の取得
        author = driver.find_element_by_xpath(f'//*[@id="{day}"]/ul/li[{i}]/a/h5')
        # 画像URLの取得
        ele = driver.find_element_by_xpath(f'//*[@id="{day}"]/ul/li[{i}]/a/div[1]/img')
        imgurl = ele.get_attribute('src')
        # サービス名の取得
        service_name = 'magapoke'
        # is_freeをtrue(1)にする
        is_free = 1
        # 取得できているかの確認としてのprint
        print('タイトル:', title.text)
        print("著者:", author.text)
        print("表紙:", imgurl)
        print('サービス名:', service_name)
        # 詳細ページへ
        detail = driver.find_element_by_xpath(f'//*[@id="{day}"]/ul/li[{i}]/a')
        driver.execute_script('arguments[0].click();', detail)
        
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
        
        # 仮テーブルに追加または更新
        cur.execute("INSERT OR REPLACE INTO temp_magapoke(title, author, img, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (title.text, author.text, imgurl, summary, is_free, service_name, cur_url))
        # 最新テーブルに追加
        cur.execute("INSERT OR REPLACE INTO new_magapoke(title, author, img, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (title.text, author.text, imgurl, summary, is_free, service_name, cur_url))

        conn.commit()
      else:
        print()
        break

def recreate():
    # データベースの接続
    conn = sqlite3.connect('manga.db')
    cur = conn.cursor()
    # 仮テーブルの作成
    cur.execute("CREATE TABLE temp_magapoke(id INTEGER, title TEXT, author TEXT, img TEXT, summary TEXT, is_free INTEGER, service_name TEXT, cur_url TEXT")
    # 最新テーブルの作成
    cur.execute("CREATE TABLE new_magapoke(id INTEGER, title TEXT, author TEXT, img TEXT, summary TEXT, is_free INTEGER, service_name TEXT, cur_url TEXT")

    # 仮テーブルにコピー
    cur.execute("INSERT INTO temp_magapoke SELECT * FROM origin_magapoke")

def refresh():
    # データベースの接続
    conn = sqlite3.connect('manga.db')
    cur = conn.cursor()

    # 仮テーブルと更新テーブルの比較をして更新テーブルにないマンガを削除
    cur.execute("DELETE * FROM temp_magapoke LEFT OUTER JOIN new_magapoke ON temp_magapoke.title = new_magapoke.title WHERE new_magapoke.title IS NULL")

    # オリジナルのテーブルに名前を変更
    cur.execute("ALTER TABLE temp_magapoke RENAME TO magapoke")
    conn.commit()






  # chromeを開いたままpython seleniumを終了してchromeを開いたままにする
  # os.kill(driver.service.process.pid, signal.SIGTERM)