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
driver.get('https://www.cmoa.jp/?_ga=2.75982876.88208316.1662363585-1869714350.1662363585')
time.sleep(3)

login = driver.find_element_by_xpath('//*[@id="home"]/header/div[1]/div[7]/a[2]')
driver.execute_script('arguments[0].click();', login)
time.sleep(3)


id = driver.find_element_by_xpath('//*[@id="email"]')
id.send_keys('sasajimarei@gmail.com')
time.sleep(3)

password = driver.find_element_by_xpath('//*[@id="password"]')
password.send_keys('ssjm01Irvine')

time.sleep(3)

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
        title = driver.find_element_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[3]/div[2]/a').text
        # 表紙
        ele = driver.find_element_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[2]/a/img')
        # 作者
        author = driver.find_element_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[3]/div[3]/a[1]').text
        imgurl = ele.get_attribute('src')
        # オプション文言
        note = driver.find_element_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[3]/div[1]/a').text
        
        if note != "立読み増量":
          print(title, author)
          print(note)
          print(imgurl)
          
          # 詳細ページ
          detail = driver.find_element_by_xpath(f'//*[@id="freeTitle"]/div[2]/ul[{column}]/li[{row}]/div[2]/a')
          driver.execute_script('arguments[0].click();', detail)
          driver.implicitly_wait(5)
          # あらすじ
          summary = driver.find_element_by_id('comic_description').text
          print("あらすじ", summary)
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