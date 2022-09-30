from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os, signal
import time
import sqlite3

def oukokuScraping():
  # データベースの接続
  conn = sqlite3.connect('../manga.db')
  cur = conn.cursor()

  # cur.execute("CREATE TABLE IF NOT EXISTS origin_oukoku('id'INTEGER NOT NULL,'title' TEXT NOT NULL UNIQUE, 'author' TEXT, 'img_url' TEXT, ")

  # option addargumentでブラウザ非表示でselenium実行
  options = Options()
  options.add_argument('--headless')

  # chromeoption=optionsでブラウザ非表示を適用
  driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
  # driver = webdriver.Chrome(ChromeDriverManager().install())
  driver.implicitly_wait(10)
  # まんが王国無料ページへ
  # driver.get('https://comic.k-manga.jp/search/jikkuri')
  # まんが王国無料漫画113ページ分の切り替え
  for j in range(1, 113+1):
    driver.get(f'https://comic.k-manga.jp/search/jikkuri?search_option%5Bsort%5D=popular&page={j}')
    driver.implicitly_wait(10)
    for i in range(1, 51):
      if driver.find_elements_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]'):
        print("page:", j, "list:", i)
        # タイトル
        if driver.find_elements_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a/h2'):
          title = driver.find_element_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a/h2').text
        print("タイトル:", title)
        # 表紙
        ele = driver.find_element_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a/img')
        img_url = ele.get_attribute('src')
        print("表紙URL:", img_url)
        
        #備考欄1
        if driver.find_elements_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a/div/aside[1]'):
          note1 = driver.find_element_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a/div/aside[1]').text
        else:
          note1 = ("")
        #備考欄2
        if driver.find_elements_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a/div/aside[2]'):
          note2 = driver.find_element_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a/div/aside[2]').text
        else:
          note2 = ("")
        # 備考欄3
        if driver.find_elements_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a/div/aside[3]'):
          note3 = driver.find_element_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a/div/aside[3]').text
        else:
          note3 = ("")
        
        # 備考欄をまとめる
        note = (note1 + note2 + note3)
        print("備考欄", note)
        # 詳細ページへ
        detail = driver.find_element_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a')
        driver.execute_script('arguments[0].click();', detail)
        driver.implicitly_wait(10)

        # 詳細URLの取得
        cur_url = driver.current_url
        print("URL:", cur_url)
        # 作者
        author = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/section[1]/div[1]/div[2]/dl/dd[1]/a').text
        print("作者:", author)
        # あらすじ
        summary = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/section[1]/div[6]/p').text
        print("あらすじ:", summary)
        # サービス名
        service_name = 'manga-oukoku'
        print("サービス名:", service_name)
        #is_freeに1
        is_free = 1
        print("無料ですか?", is_free)

        cur.execute("INSERT INTO origin_oukoku(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (title, author, img_url, note, summary, is_free, service_name, cur_url))
        conn.commit()
        print()

        # 前のページに戻る
        driver.back()

      else:
        print()
        break
    driver.implicitly_wait(10)
  time.sleep(1)

def oukokuRefresh():
  conn = sqlite3.connect('./manga.db')
  cur = conn.cursor()
  # tempテーブルの作成
  cur.execute("CREATE TABLE temp_oukoku('id'INTEGER NOT NULL,'title' TEXT NOT NULL UNIQUE,'author'TEXT,'img_url'TEXT,'note'TEXT,'summary'TEXT,'is_free'INTEGER,'service_name'TEXT,'cur_url'TEXT,PRIMARY KEY('id'))")
  
  # # tempテーブルにコピー
  cur.execute("INSERT INTO temp_oukoku SELECT id, title, author, img_url, note, summary, is_free, service_name, cur_url FROM origin_oukoku")

  # newテーブルの作成
  cur.execute("CREATE TABLE new_oukoku('title' TEXT NOT NULL UNIQUE, 'author' TEXT, 'img_url' TEXT, 'note' TEXT, 'summary' TEXT, 'is_free' INTEGER, 'service_name' TEXT, 'cur_url' TEXT)")

  # chromeoption=optionsでブラウザ非表示を適用
  driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
  # driver = webdriver.Chrome(ChromeDriverManager().install())
  driver.implicitly_wait(10)
  for j in range(1, 113+1):
    driver.get(f'https://comic.k-manga.jp/search/jikkuri?search_option%5Bsort%5D=popular&page={j}')
    driver.implicitly_wait(10)
    for i in range(1, 51):
      if driver.find_elements_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]'):
        print("page:", j, "list:", i)
        # タイトル
        if driver.find_elements_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a/h2'):
          title = driver.find_element_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a/h2').text
        print("タイトル:", title)
        # 表紙
        ele = driver.find_element_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a/img')
        img_url = ele.get_attribute('src')
        print("表紙URL:", img_url)
        
        #備考欄1
        if driver.find_elements_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a/div/aside[1]'):
          note1 = driver.find_element_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a/div/aside[1]').text
        else:
          note1 = ("")
        #備考欄2
        if driver.find_elements_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a/div/aside[2]'):
          note2 = driver.find_element_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a/div/aside[2]').text
        else:
          note2 = ("")
        # 備考欄3
        if driver.find_elements_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a/div/aside[3]'):
          note3 = driver.find_element_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a/div/aside[3]').text
        else:
          note3 = ("")
        
        # 備考欄をまとめる
        note = (note1 + note2 + note3)
        print("備考欄", note)
        # 詳細ページへ
        detail = driver.find_element_by_xpath(f'//*[@id="contents"]/section/div[2]/section[1]/div/ul/li[{i}]/a')
        driver.execute_script('arguments[0].click();', detail)
        driver.implicitly_wait(10)

        # 詳細URLの取得
        cur_url = driver.current_url
        print("URL:", cur_url)
        # 作者
        author = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/section[1]/div[1]/div[2]/dl/dd[1]/a').text
        print("作者:", author)
        # あらすじ
        summary = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/section[1]/div[6]/p').text
        print("あらすじ:", summary)
        # サービス名
        service_name = 'manga-oukoku'
        print("サービス名:", service_name)
        #is_freeに1
        is_free = 1
        print("無料ですか?", is_free)

        cur.execute("INSERT INTO temp_oukoku(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (title) DO UPDATE SET title = title, author = author, img_url = img_url, note = note, summary = summary, is_free = is_free, service_name = service_name, cur_url = cur_url ;", (title, author, img_url, note, summary, is_free, service_name, cur_url))
        conn.commit()

        # # 最新テーブルに追加
        cur.execute("INSERT INTO new_oukoku(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (title, author, img_url, note, summary, is_free, service_name, cur_url))
        conn.commit()
        print()

        # 前のページに戻る
        driver.back()

      else:
        print()
        break
    driver.implicitly_wait(10)
  time.sleep(1)
