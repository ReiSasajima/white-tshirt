#scrapingフォルダから各々のサイト用のスクレイピングモジュールをインポート
from scraping import booklive, oukoku, cmoa, jumpplus, line, magapoke, piccoma, scraping, ynjn 
from crontab import CronTab
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os, signal
import time
import sqlite3

# インスタンスの生成
cron = CronTab()
# ジョブを生成してコマンドを設定する
job = cron.new(command='python3 ./scraping-assemble.py')
# 毎週日曜、午前2時にCRONセット
job.setall('0 2 * * 7')
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

def main():
  ynjn() #やんじゃんのスクレイピング関数
  oukoku() #まんが王国のスクレイピング関数
  jumpplus() #ジャンププラスのスクレイピング関数
  cmoa() #コミックシーモアのスクレイピング関数
  piccoma() #ピッコマのスクレイピング関数
  booklive() #bookliveのスクレイピング関数
  line() #liveマンガのスクレイピング関数
  # magapoke() #マガポケのスクレイピング関数
  scraping() #マガポケのスクレイピング関数