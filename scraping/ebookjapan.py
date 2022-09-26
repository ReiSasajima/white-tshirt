from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os, signal
import time
import sqlite3

# option addargumentでブラウザ非表示でselenium実行
options = Options()
options.add_argument('--headless')

def ebookjapanScraping():
  # データベースの接続
  conn = sqlite3.connect('../manga.db')
  cur = conn.cursor()

  # chromeoption=optionsでブラウザ非表示を適用
  driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
  driver.implicitly_wait(10)

  for page in range(1, 118):
    driver.get(f'https://ebookjapan.yahoo.co.jp/free/books/?useTitle=1&page={page}')
    for list in range(1, 59):
      if driver.find_elements_by_xpath(f'//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul/li[{list}]'):
        # 表紙URL
        ele = driver.find_element_by_xpath(f'''//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul
        /li[{list}]/div/a/div[1]/img''')
        img_url = ele.get_attribute('data-src')
        # タイトル
        title = driver.find_element_by_xpath(f'//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul/li[{list}]/div/a/div[2]/p').text
        #備考欄
        if driver.find_elements_by_xpath(f'//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul/li[{list}]/div/div/a'):
          note  = driver.find_element_by_xpath(f'''//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul
          /li[{list}]/div/div/a''').text

          if "無料" in note:
            print("Page:", page,"List:", list)
            print("タイトル",title)
            print("表紙", img_url)

            #is_freeを1にする
            is_free = 1
            print("無料ですか？:", is_free)

            #サービス名
            service_name = 'ebookjapan'
            print('サービス名:', service_name)

            # 詳細ページへ
            if driver.find_elements_by_xpath(f'''//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul/li[{list}]/div/a'''):
              detail = driver.find_element_by_xpath(f'//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul/li[{list}]/div/a')
              driver.execute_script('arguments[0].click();', detail)
            else:
              None
            driver.implicitly_wait(10)

            # 詳細URL
            cur_url = driver.current_url
            print("CUR_URL:", cur_url)

            # 作者
            if driver.find_elements_by_xpath('//*[@id="wrapper"]/div[4]/div[1]/div/div[1]/div/div[1]/div[3]/p[1]/a'):
              author = driver.find_element_by_xpath('//*[@id="wrapper"]/div[4]/div[1]/div/div[1]/div/div[1]/div[3]/p[1]/a').text
            else:
              author = ''
            print("作者:", author)
            
            #スクロール
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(10)
            
            # あらすじ
            if driver.find_elements_by_class_name('overview__summary'):
              summary = driver.find_element_by_class_name('overview__summary').text
            else:
              summary = ''
            print("あらすじ:", summary)

            cur.execute("INSERT INTO origin_ebookjapan(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (title, author, img_url, note, summary, is_free, service_name, cur_url))
            conn.commit()

            # ブラウザバック
            driver.back()
            driver.implicitly_wait(10)
          else:
            time.sleep(1)
            None
        else:
          driver.implicitly_wait(10)
          None
      else:
        print()
        break


def ebookjapanRefresh():
# データベースの接続
  conn = sqlite3.connect('./manga.db')
  cur = conn.cursor()
#tempテーブルが存在していたら一旦削除
  cur.execute("DROP TABLE IF EXISTS temp_ebookjapan")
  cur.execute("DELETE FROM sqlite_sequence WHERE name = 'temp_ebookjapan';")
# tempテーブルの作成
  cur.execute("CREATE TABLE temp_ebookjapan('id'INTEGER NOT NULL,'title' TEXT NOT NULL UNIQUE,'author'TEXT,'img_url'TEXT,'note'TEXT,'summary'TEXT,'is_free'INTEGER,'service_name'TEXT,'cur_url'TEXT,PRIMARY KEY('id'))")
  
# tempテーブルにコピー
  cur.execute("INSERT INTO temp_ebookjapan SELECT id, title, author, img_url, note, summary, is_free, service_name, cur_url FROM origin_ebookjapan")
#tempテーブルが存在していたら一旦削除
  cur.execute("DROP TABLE IF EXISTS new_ebookjapan")
  cur.execute("DELETE FROM sqlite_sequence WHERE name = 'temp_ebookjapan';")
# newテーブルの作成
  cur.execute("CREATE TABLE new_ebookjapan('title' TEXT NOT NULL, 'author' TEXT, 'img_url' TEXT, 'note' TEXT, 'summary' TEXT, 'is_free' INTEGER, 'service_name' TEXT, 'cur_url' TEXT)")

# chromeoption=optionsでブラウザ非表示を適用
  driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
  driver.implicitly_wait(10)

  for page in range(1, 118):
    driver.get(f'https://ebookjapan.yahoo.co.jp/free/books/?useTitle=1&page={page}')
    for list in range(1, 59):
      if driver.find_elements_by_xpath(f'//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul/li[{list}]'):
        # 表紙URL
        ele = driver.find_element_by_xpath(f'''//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul
        /li[{list}]/div/a/div[1]/img''')
        img_url = ele.get_attribute('data-src')
        # タイトル
        title = driver.find_element_by_xpath(f'//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul/li[{list}]/div/a/div[2]/p').text
        if driver.find_elements_by_xpath(f'//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul/li[{list}]/div/div/a'):
          note  = driver.find_element_by_xpath(f'''//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul
          /li[{list}]/div/div/a''').text
          if "無料" in note:
            print("Page:", page,"List:", list)
            print("タイトル",title)
            print("表紙", img_url)

            #is_freeを1にする
            is_free = 1
            print("無料ですか？:", is_free)

            #サービス名
            service_name = 'ebookjapan'
            print('サービス名:', service_name)

            # 詳細ページへ
            if driver.find_elements_by_xpath(f'''//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul/li[{list}]/div/a'''):
              detail = driver.find_element_by_xpath(f'//*[@id="wrapper"]/div[4]/div[1]/div/div/div/div[3]/div[1]/ul/li[{list}]/div/a')
              driver.execute_script('arguments[0].click();', detail)
            else:
              None
            driver.implicitly_wait(10)

            # 詳細URL
            cur_url = driver.current_url
            print("CUR_URL:", cur_url)

            # 作者
            if driver.find_elements_by_xpath('//*[@id="wrapper"]/div[4]/div[1]/div/div[1]/div/div[1]/div[3]/p[1]/a'):
              author = driver.find_element_by_xpath('//*[@id="wrapper"]/div[4]/div[1]/div/div[1]/div/div[1]/div[3]/p[1]/a').text
            else:
              author = ''
            print("作者:", author)
            
            #スクロール
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.implicitly_wait(10)
            
            # あらすじ
            if driver.find_elements_by_class_name('overview__summary'):
              summary = driver.find_element_by_class_name('overview__summary').text
            else:
              summary = ''
            print("あらすじ:", summary)

            # ブラウザバック
            driver.back()
            driver.implicitly_wait(10)

            # tempテーブルに追加または更新
            cur.execute("INSERT INTO temp_ebookjapan(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?) ON CONFLICT (title) DO UPDATE SET title = title, author = author, img_url = img_url, note = note, summary = summary, is_free = is_free, service_name = service_name, cur_url = cur_url ;", (title, author, img_url, note, summary, is_free, service_name, cur_url))
            conn.commit()

            # 最新テーブルに追加
            cur.execute("INSERT INTO new_ebookjapan(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (title, author, img_url, note, summary, is_free, service_name, cur_url))
            conn.commit()
          else:
            driver.implicitly_wait(10)
            None
        else:
          driver.implicitly_wait(10)
          None
      else:
        print()
        break
  # 仮テーブルと更新テーブルの比較をして更新テーブルにないマンガを削除
  cur.execute("DELETE FROM temp_ebookjapan WHERE title IN (SELECT temp_ebookjapan.title FROM temp_ebookjapan LEFT OUTER JOIN new_ebookjapan ON temp_ebookjapan.title = new_ebookjapan.title WHERE new_ebookjapan.title IS NULL)")

  # オリジナルのテーブルを削除
  cur.execute("DROP TABLE origin_ebookjapan")

  # オリジナルのテーブルに名前を変更
  cur.execute("ALTER TABLE temp_ebookjapan RENAME TO origin_ebookjapan;")
  conn.commit()
  # Newテーブルの削除
  cur.execute("DROP TABLE new_ebookjapan;")
  conn.commit()

  #削除済みテーブル分のデータ削除
  cur.execute("VACUUM;")
