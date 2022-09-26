from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os, signal
import time
import sqlite3

# option addargumentでブラウザ非表示でselenium実行
options = Options()
options.add_argument('--headless')

def piccomaScraping():
  # データベースの接続
  conn = sqlite3.connect('../manga.db')
  cur = conn.cursor()

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
        print("page:", i)
        # タイトルの取得
        if driver.find_elements_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]/a/div/div/div[2]/span'):
          title = driver.find_element_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]/a/div/div/div[2]/span').text
        else:
          title = ''
        print("title:", title)
        # 画像URLの取得
        ele = driver.find_element_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]/a/div/div/div[1]/img')
        img_url = ele.get_attribute('src')
        print("表紙:", img_url)

        # 期間限定、無料枠などの情報取得
        note = driver.find_element_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]/a/div/div/p/span').text
        print("備考欄:", note)
        
        # 漫画リストのクリック(詳細ページへ)
        detail  = driver.find_element_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]/a')
        driver.execute_script('arguments[0].click();', detail)
        driver.implicitly_wait(10)
        # 著者名の取得
        author = driver.find_element_by_xpath('//*[@id="js_author"]/li/a').text
        print("著者:", author)
        # あらすじの取得
        if driver.find_elements_by_xpath('//*[@id="js_productDesc"]/p'):
          summary = driver.find_element_by_xpath('//*[@id="js_productDesc"]/p').text
        else:
          summary = ''
        print("あらすじ:", summary)
        # 詳細URLの取得
        cur_url = driver.current_url
        print("URL:", cur_url)
        # サービス名の取得
        service_name = 'piccoma'
        # is_freeをtrue(1)にする
        is_free = 1

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

def piccomaRefresh():
  # データベースの接続
  conn = sqlite3.connect('../manga.db')
  cur = conn.cursor()
  #tempテーブルが存在していたら一旦削除
  cur.execute("DROP TABLE IF EXISTS temp_piccoma")
  cur.execute("DELETE FROM sqlite_sequence WHERE name = 'temp_piccoma';")
  # tempテーブルの作成
  cur.execute("CREATE TABLE temp_piccoma('id'INTEGER NOT NULL,'title' TEXT NOT NULL UNIQUE,'author'TEXT,'img_url'TEXT,'note'TEXT,'summary'TEXT,'is_free'INTEGER,'service_name'TEXT,'cur_url'TEXT,PRIMARY KEY('id'))")
  
  # tempテーブルにコピー
  cur.execute("INSERT INTO temp_piccoma SELECT id, title, author, img_url, note, summary, is_free, service_name, cur_url FROM origin_piccoma")
  #tempテーブルが存在していたら一旦削除
  cur.execute("DROP TABLE IF EXISTS new_piccoma")
  cur.execute("DELETE FROM sqlite_sequence WHERE name = 'temp_piccoma';")
  # newテーブルの作成(titleのUNIQUEはずす)
  cur.execute("CREATE TABLE new_piccoma('title' TEXT NOT NULL, 'author' TEXT, 'img_url' TEXT, 'note' TEXT, 'summary' TEXT, 'is_free' INTEGER, 'service_name' TEXT, 'cur_url' TEXT)")

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
        print("page:", i)
        # タイトルの取得
        if driver.find_elements_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]/a/div/div/div[2]/span'):
          title = driver.find_element_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]/a/div/div/div[2]/span').text
        else:
          title = ''
        print("title:", title)
        # 画像URLの取得
        ele = driver.find_element_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]/a/div/div/div[1]/img')
        img_url = ele.get_attribute('src')
        print("表紙:", img_url)

        # 期間限定、無料枠などの情報取得
        note = driver.find_element_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]/a/div/div/p/span').text
        print("備考欄:", note)
        
        # 漫画リストのクリック(詳細ページへ)
        detail  = driver.find_element_by_xpath(f'//*[@id="ajax_infScroll"]/li[{i}]/a')
        driver.execute_script('arguments[0].click();', detail)
        driver.implicitly_wait(10)
        # 著者名の取得
        author = driver.find_element_by_xpath('//*[@id="js_author"]/li/a').text
        print("著者:", author)
        # あらすじの取得
        if driver.find_elements_by_xpath('//*[@id="js_productDesc"]/p'):
          summary = driver.find_element_by_xpath('//*[@id="js_productDesc"]/p').text
        else:
          summary = ''
        print("あらすじ:", summary)
        # 詳細URLの取得
        cur_url = driver.current_url
        print("URL:", cur_url)
        # サービス名の取得
        service_name = 'piccoma'
        # is_freeをtrue(1)にする
        is_free = 1

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
        # tempテーブルに追加または更新
        cur.execute("INSERT INTO temp_piccoma(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (title) DO UPDATE SET title = title, author = author, img_url = img_url, note = note, summary = summary, is_free = is_free, service_name = service_name, cur_url = cur_url ;", (title, author, img_url, note, summary, is_free, service_name, cur_url))
        conn.commit()

        # 最新テーブルに追加
        cur.execute("INSERT INTO new_piccoma(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (title, author, img_url, note, summary, is_free, service_name, cur_url))
        conn.commit()
      else:
        print()
        break
  # chromeを開いたままpython seleniumを終了してchromeを開いたままにする
  # os.kill(driver.service.process.pid, signal.SIGTERM)
  