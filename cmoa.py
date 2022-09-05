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
# コミックシーモアの無料ページへ
driver.get('https://www.cmoa.jp/freecontents/?page=1')
# 表紙の取得
ele = driver.find_element_by_xpath('//*[@id="freeTitle"]/div[2]/ul[1]/li[1]/div[2]/a')
imgurl = ele.get_attribute('src')
# タイトル取得
title = driver.find_element_by_xpath('//*[@id="freeTitle"]/div[2]/ul[1]/li[1]/div[3]/div[2]/a').text
print(title, imgurl)
#freeTitle > div.fixBox > ul:nth-child(1) > li:nth-child(1) > div.thum_box > a
