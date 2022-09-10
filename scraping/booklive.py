from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os, signal
import time
import sqlite3

# データベースの接続
conn = sqlite3.connect('manga.db')
cur = conn.cursor()

# option addargumentでブラウザ非表示でselenium実行
options = Options()
options.add_argument('--headless')

# chromeoption=optionsでブラウザ非表示を適用
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(10)

for page in range(1, 110):
  for list in range(1, 85):
    driver.get(f'https://booklive.jp/index/no-charge/category_id/U/page_no/{page}/exadult/1')
    # 表紙
    ele = driver.find_element_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/div[1]/div/a/img')
    imgurl = 'https:' + ele.get_attribute('data-src')
    # タイトル
    title = driver.find_element_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/p/a').text
    # 著者
    author = driver.find_element_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/div[2]').text

    print(list, title, author, imgurl)
    # 詳細ページ
    detail = driver.find_element_by_xpath(f'//*[@id="main_content"]/section/div[2]/div/div/section/div[2]/div/ul/li[{list}]/div/div[1]/div/a')
    driver.execute_script('arguments[0].click();', detail)
    # あらすじ
    summary = driver.find_element_by_class_name('product_text').text
    print(summary)

    driver.back()

    time.sleep(1)


# chromeウィンドウを閉じる
# driver.close()