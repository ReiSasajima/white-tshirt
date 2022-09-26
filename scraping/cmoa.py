from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os, signal
import time
import sqlite3

# option addargumentでブラウザ非表示でselenium実行
options = Options()
options.add_argument('--headless')

loginID = 'mail'
loginPass = 'password'
freeCmoa = 'https://www.cmoa.jp/?_ga=2.75982876.88208316.1662363585-1869714350.1662363585'

def cmoaScraping():
  
  # データベースの接続
  conn = sqlite3.connect('../manga.db')
  cur = conn.cursor()


  # chromeoption=optionsでブラウザ非表示を適用
  driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
  driver.implicitly_wait(10)

  # コミックシーモアの無料ページへ
  driver.get(freeCmoa)
  time.sleep(3)
  #ログインボタン
  login = driver.find_element_by_xpath('//*[@id="home"]/header/div[1]/div[7]/a[2]')
  driver.execute_script('arguments[0].click();', login)
  time.sleep(3)
  #id入力
  id = driver.find_element_by_xpath('//*[@id="email"]')
  id.send_keys(loginID)
  time.sleep(3)
  #パスワード
  password = driver.find_element_by_xpath('//*[@id="password"]')
  password.send_keys(loginPass)
  time.sleep(3)
  #ログインボタン
  loginBtn = driver.find_element_by_xpath('//*[@id="submitBtn"]/p')
  driver.execute_script('arguments[0].click();', loginBtn)
  driver.implicitly_wait(10)

  # 無料コミックへ
  freeBtn = driver.find_element_by_xpath('//*[@id="navi_left"]/section[3]/section/ul/li[5]/a')
  driver.execute_script('arguments[0].click();', freeBtn)
  time.sleep(3)

  # タイトル取得
  # 表紙の取得(ulが列、liが先頭からの順番)
  for page in range(1, 726):
    driver.get(f'https://www.cmoa.jp/freecontents/?page={page}')
    time.sleep(2)

    for column in range(1, 7):
      for row in range(1, 6):
        # 漫画が存在するかのif文
        if driver.find_elements_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]'):
          # タイトル
          if driver.find_elements_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[3]/div[2]/a'):
            title = driver.find_element_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[3]/div[2]/a').text
          else:
            title = ''
          # 表紙
          if driver.find_elements_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[2]/a/img'):
            ele = driver.find_element_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[2]/a/img')
            img_url = ele.get_attribute('src')
          else:
            img_url = ''
          # 作者
          author = driver.find_element_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[3]/div[3]/a[1]').text
          # オプション文言
          note = driver.find_element_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[3]/div[1]/a').text
          
          if note != "立読み増量":
            print('page:', page, 'column:', column, 'row', row)
            print("タイトル",title)
            print("著者:", author)
            print("備考欄",note)
            print("表紙",img_url)
            
            # 詳細ページへ
            detail = driver.find_element_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[2]/a')
            driver.execute_script('arguments[0].click();', detail)
            driver.implicitly_wait(10)

            # 詳細URLの取得
            cur_url = driver.current_url
            print("URL:", cur_url)

            # あらすじ
            if driver.find_elements_by_id('comic_description'):
              summary = driver.find_element_by_id('comic_description').text
            else:
              summary = ''
            print("あらすじ:", summary)
            
            #is_freeに1
            is_free = 1
            print("無料ですか:", is_free)
            #サービス名
            service_name = 'cmoa'
            print("サービス名", service_name)

            cur.execute("INSERT INTO origin_cmoa(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (title, author, img_url, note, summary, is_free, service_name, cur_url))
            conn.commit()

            # 空白
            print()
            driver.back()
            time.sleep(1)
          else:
            None
        else:
          break

  # chromeウィンドウを閉じる
  driver.close()
  # chromeを開いたままpython seleniumを終了してchromeを開いたままにする
  # os.kill(driver.service.process.pid, signal.SIGTERM)

def cmoaRefresh():
  # データベースの接続
  conn = sqlite3.connect('./manga.db')
  cur = conn.cursor()

  #tempテーブルが存在していたら一旦削除
  cur.execute("DROP TABLE IF EXISTS temp_cmoa")
  cur.execute("DELETE FROM sqlite_sequence WHERE name = 'temp_cmoa';")
  # tempテーブルの作成
  cur.execute("CREATE TABLE temp_cmoa('id'INTEGER NOT NULL,'title' TEXT NOT NULL UNIQUE,'author'TEXT,'img_url'TEXT,'note'TEXT,'summary'TEXT,'is_free'INTEGER,'service_name'TEXT,'cur_url'TEXT,PRIMARY KEY('id'))")
  # tempテーブルにコピー
  cur.execute("INSERT INTO temp_cmoa SELECT id, title, author, img_url, note, summary, is_free, service_name, cur_url FROM origin_cmoa")
  #newテーブルが存在していたら一旦削除
  cur.execute("DROP TABLE IF EXISTS new_cmoa")
  cur.execute("DELETE FROM sqlite_sequence WHERE name = 'new_cmoa';")
  # newテーブルの作成(newテーブルではtitleがUNIQUEにしない)
  cur.execute("CREATE TABLE new_cmoa('title' TEXT NOT NULL, 'author' TEXT, 'img_url' TEXT, 'note' TEXT, 'summary' TEXT, 'is_free' INTEGER, 'service_name' TEXT, 'cur_url' TEXT)")
  
  # chromeoption=optionsでブラウザ非表示を適用
  driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
  driver.implicitly_wait(10)

  # コミックシーモアの無料ページへ
  driver.get(freeCmoa)
  time.sleep(3)
  #ログインボタン
  login = driver.find_element_by_xpath('//*[@id="home"]/header/div[1]/div[7]/a[2]')
  driver.execute_script('arguments[0].click();', login)
  time.sleep(3)
  #id入力
  id = driver.find_element_by_xpath('//*[@id="email"]')
  id.send_keys(loginID)
  time.sleep(3)
  #パスワード
  password = driver.find_element_by_xpath('//*[@id="password"]')
  password.send_keys(loginPass)
  time.sleep(3)
  #ログインボタン
  loginBtn = driver.find_element_by_xpath('//*[@id="submitBtn"]/p')
  driver.execute_script('arguments[0].click();', loginBtn)
  driver.implicitly_wait(10)

  # 無料コミックへ
  freeBtn = driver.find_element_by_xpath('//*[@id="navi_left"]/section[3]/section/ul/li[5]/a')
  driver.execute_script('arguments[0].click();', freeBtn)
  time.sleep(3)

  # タイトル取得
  # 表紙の取得(ulが列、liが先頭からの順番)
  1,726
  for page in range(1, 726):
    driver.get(f'https://www.cmoa.jp/freecontents/?page={page}')
    driver.implicitly_wait(10)

    for column in range(1, 7):
      for row in range(1, 6):
        # 漫画が存在するかのif文
        if driver.find_elements_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]'):
          # タイトル
          if driver.find_elements_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[3]/div[2]/a'):
            title = driver.find_element_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[3]/div[2]/a').text
          else:
            title = ''
          # 表紙
          if driver.find_elements_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[2]/a/img'):
            ele = driver.find_element_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[2]/a/img')
            img_url = ele.get_attribute('src')
          else:
            img_url = ''
          # 作者
          author = driver.find_element_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[3]/div[3]/a[1]').text
          # オプション文言
          note = driver.find_element_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[3]/div[1]/a').text
          
          if note != "立読み増量":
            print('page:', page, 'column:', column, 'row', row)
            print("タイトル",title)
            print("著者:", author)
            print("備考欄",note)
            print("表紙",img_url)
            
            # 詳細ページへ
            detail = driver.find_element_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[2]/a')
            driver.execute_script('arguments[0].click();', detail)
            driver.implicitly_wait(10)

            # 詳細URLの取得
            cur_url = driver.current_url
            print("URL:", cur_url)

            # あらすじ
            if driver.find_elements_by_id('comic_description'):
              summary = driver.find_element_by_id('comic_description').text
            else:
              summary = ''
            print("あらすじ:", summary)
            
            #is_freeに1
            is_free = 1
            print("無料ですか:", is_free)
            #サービス名
            service_name = 'cmoa'
            print("サービス名", service_name)

            # tempテーブルに追加または更新
            cur.execute("INSERT INTO temp_cmoa(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (title) DO UPDATE SET title = title, author = author, img_url = img_url, note = note, summary = summary, is_free = is_free, service_name = service_name, cur_url = cur_url ;", (title, author, img_url, note, summary, is_free, service_name, cur_url))
            conn.commit()

            # 最新テーブルに追加
            cur.execute("INSERT INTO new_cmoa(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (title, author, img_url, note, summary, is_free, service_name, cur_url))
            conn.commit()
            # 空白
            print()
            driver.back()
          else:
            None
        else:
          break
  # 仮テーブルと更新テーブルの比較をして更新テーブルにないマンガを削除
  cur.execute("DELETE FROM temp_cmoa WHERE title IN (SELECT temp_cmoa.title FROM temp_cmoa LEFT OUTER JOIN new_cmoa ON temp_cmoa.title = new_cmoa.title WHERE new_cmoa.title IS NULL)")

  # オリジナルのテーブルを削除
  cur.execute("DROP TABLE origin_cmoa")

  # オリジナルのテーブルに名前を変更
  cur.execute("ALTER TABLE temp_cmoa RENAME TO origin_cmoa;")
  conn.commit()
  # Newテーブルの削除
  cur.execute("DROP TABLE new_cmoa;")
  conn.commit()

  #削除済みテーブル分のデータ削除
  cur.execute("VACUUM;")
