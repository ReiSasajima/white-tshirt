from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os, signal
import time
import sqlite3

def lineScraping():
  # データベースの接続
  conn = sqlite3.connect('../manga.db')
  cur = conn.cursor()

  # option addargumentでブラウザ非表示でselenium実行
  options = Options()
  options.add_argument('--headless')

  # chromeoption=optionsでブラウザ非表示を適用
  driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
  # driver = webdriver.Chrome(ChromeDriverManager().install())

  driver.get('https://manga.line.me/periodic/gender_ranking?gender=0')

  list = 1
  while driver.find_elements_by_xpath(f'/html/body/div[1]/div/div[2]/div/section/div/ol/li[{list}]'):
    # タイトル
    title = driver.find_element_by_xpath(f'/html/body/div[1]/div/div[2]/div/section/div/ol/li[{list}]/a/span[2]').text
    print("作品名",title)

    # 画像URL
    img_url = driver.find_element_by_xpath(f'/html/body/div[1]/div/div[2]/div/section/div/ol/li[{list}]/a/div/img').get_attribute('src')
    print("画像",img_url)
    

    note = driver.find_element_by_class_name('mdCMN05InfoList').text
    print("備考欄", note)

    # 詳細ページへ
    detail = driver.find_element_by_xpath(f'/html/body/div[1]/div/div[2]/div/section/div/ol/li[{list}]/a')
    driver.execute_script('arguments[0].click();', detail)
    # 作者
    author = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/article/section[1]/div/div[2]/dl/dd[2]/a').text
    print("作者",author)
    # 詳細URL
    cur_url = driver.current_url
    print(cur_url)

    #あらすじ
    summary = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/article/section[1]/div/div[2]/div[2]/p[1]').text
    print(summary)
    # サービス名
    service_name = 'lineManga'
    print(service_name)

    is_free = 1
    print(is_free)

    cur.execute("INSERT INTO line(title, author, img_url, note, summary, is_free, service_name, cur_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (title, author, img_url, note, summary, is_free, service_name, cur_url))
    conn.commit()

    driver.back()

    list += 1

    # スクロールしないと全てのliが表示されないためのスクロール
    # driver.execute_script("window.scrollBy(0, 200);")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(1)

