from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os, signal
import time
import sqlite3

def ynjnScraping():
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
  
  # やんじゃん！無料キャンペーンサイト
  driver.get('https://ynjn.jp/')
  detailBtn = driver.find_element_by_xpath('//*[@id="layout"]/div/section[5]/div/div/div[2]/button')
  
  driver.execute_script('arguments[0].click();', detailBtn)

  num = driver.find_element_by_xpath('//*[@id="layout"]/div/section/div/div[2]/div/div').text
  num = int(num.strip('件'))
  for list in range(1, num+1):
    # タイトル
    title = driver.find_element_by_xpath(f'//*[@id="layout"]/div/section/div/div[2]/div/ul/li[{list}]/div/a/div/div[2]').text
    print("タイトル:", title)
    # 備考欄
    note = driver.find_element_by_xpath(f'//*[@id="layout"]/div/section/div/div[2]/div/ul/li[{list}]/div/a/div/div[3]').text
    print("備考欄:", note)
    # 表紙
    img_url = driver.find_element_by_xpath(f'//*[@id="layout"]/div/section/div/div[2]/div/ul/li[{list}]/div/a/div/div[1]/img').get_attribute('src')
    print("表紙:", img_url)
    # 詳細ページへ
    detailPage = driver.find_element_by_xpath(f'//*[@id="layout"]/div/section/div/div[2]/div/ul/li[{list}]/div/a')
    driver.execute_script('arguments[0].click();', detailPage)
    driver.implicitly_wait(10)

    # 詳細URL
    cur_url = driver.current_url
    # サービス名
    service_name = 'ynjn'
    # is_free
    is_free = 1
    # 作者
    author = driver.find_element_by_class_name('title__detailSubTitle').text
    print("作者:", author)

    # あらすじ
    summary  = driver.find_element_by_class_name('title__explanation').text
    print("あらすじ:", summary)
    
    cur.execute("INSERT INTO origin_ynjn(title, author, img_url, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?);", (title, author, img_url, summary, is_free, service_name, cur_url))
    conn.commit()
    driver.back()

    driver.implicitly_wait(10)

def ynjnRefresh():
  # データベースの接続
  conn = sqlite3.connect('./manga.db')
  cur = conn.cursor()
  # option addargumentでブラウザ非表示でselenium実行
  options = Options()
  options.add_argument('--headless')
  #tempテーブルが存在していたら一旦削除
  cur.execute("DROP TABLE IF EXISTS temp_ynjn")
  cur.execute("DELETE FROM sqlite_sequence WHERE name = 'temp_ynjn';")
  # tempテーブルの作成
  cur.execute("CREATE TABLE temp_ynjn('id'INTEGER NOT NULL,'title' TEXT NOT NULL UNIQUE,'author'TEXT,'img_url'TEXT,'note'TEXT,'summary'TEXT,'is_free'INTEGER,'service_name'TEXT,'cur_url'TEXT,PRIMARY KEY('id'))")
  
  # tempテーブルにコピー
  cur.execute("INSERT INTO temp_ynjn SELECT id, title, author, img_url, note, summary, is_free, service_name, cur_url FROM origin_ynjn")
  #tempテーブルが存在していたら一旦削除
  cur.execute("DROP TABLE IF EXISTS new_ynjn")
  cur.execute("DELETE FROM sqlite_sequence WHERE name = 'temp_ynjn';")
  # newテーブルの作成(titleのUNIQUEはずす)
  cur.execute("CREATE TABLE new_ynjn('title' TEXT NOT NULL, 'author' TEXT, 'img_url' TEXT, 'note' TEXT, 'summary' TEXT, 'is_free' INTEGER, 'service_name' TEXT, 'cur_url' TEXT)")
  # chromeoption=optionsでブラウザ非表示を適用
  driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
  # driver = webdriver.Chrome(ChromeDriverManager().install())
  driver.implicitly_wait(10)
  # やんじゃん！無料キャンペーンサイト
  driver.get('https://ynjn.jp/')
  detailBtn = driver.find_element_by_xpath('//*[@id="layout"]/div/section[5]/div/div/div[2]/button')
  
  driver.execute_script('arguments[0].click();', detailBtn)

  num = driver.find_element_by_xpath('//*[@id="layout"]/div/section/div/div[2]/div/div').text
  num = int(num.strip('件'))
  for list in range(1, num+1):
    # タイトル
    title = driver.find_element_by_xpath(f'//*[@id="layout"]/div/section/div/div[2]/div/ul/li[{list}]/div/a/div/div[2]').text
    print("タイトル:", title)
    # 備考欄
    note = driver.find_element_by_xpath(f'//*[@id="layout"]/div/section/div/div[2]/div/ul/li[{list}]/div/a/div/div[3]').text
    print("備考欄:", note)
    # 表紙
    img_url = driver.find_element_by_xpath(f'//*[@id="layout"]/div/section/div/div[2]/div/ul/li[{list}]/div/a/div/div[1]/img').get_attribute('src')
    print("表紙:", img_url)
    # 詳細ページへ
    detailPage = driver.find_element_by_xpath(f'//*[@id="layout"]/div/section/div/div[2]/div/ul/li[{list}]/div/a')
    driver.execute_script('arguments[0].click();', detailPage)
    driver.implicitly_wait(10)

    # 詳細URL
    cur_url = driver.current_url
    # サービス名
    service_name = 'ynjn'
    # is_free
    is_free = 1
    # 作者
    author = driver.find_element_by_class_name('title__detailSubTitle').text
    print("作者:", author)

    # あらすじ
    summary  = driver.find_element_by_class_name('title__explanation').text
    print("あらすじ:", summary)
  # tempテーブルに追加または更新
    cur.execute("INSERT INTO temp_ynjn(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (title) DO UPDATE SET title = title, author = author, img_url = img_url, note = note, summary = summary, is_free = is_free, service_name = service_name, cur_url = cur_url ;", (title, author, img_url, note, summary, is_free, service_name, cur_url))
    conn.commit()

    # 最新テーブルに追加
    cur.execute("INSERT INTO new_ynjn(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (title, author, img_url, note, summary, is_free, service_name, cur_url))
    conn.commit()
    # 空白
    print()
    driver.back()

    driver.implicitly_wait(10)
    # 仮テーブルと更新テーブルの比較をして更新テーブルにないマンガを削除
    cur.execute("DELETE FROM temp_ynjn WHERE title IN (SELECT temp_ynjn.title FROM temp_ynjn LEFT OUTER JOIN new_ynjn ON temp_ynjn.title = new_ynjn.title WHERE new_ynjn.title IS NULL)")

    # オリジナルのテーブルを削除
    cur.execute("DROP TABLE origin_ynjn")

    # オリジナルのテーブルに名前を変更
    cur.execute("ALTER TABLE temp_ynjn RENAME TO origin_ynjn;")
    conn.commit()
    # Newテーブルの削除
    cur.execute("DROP TABLE new_ynjn;")
    conn.commit()

    #削除済みテーブル分のデータ削除
    cur.execute("VACUUM;")
