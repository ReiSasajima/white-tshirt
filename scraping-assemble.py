#scrapingフォルダから各々のサイト用のスクレイピングモジュールをインポート 
from scraping.ynjn import ynjnRefresh
from scraping.booklive import bookliveRefresh
from scraping.oukoku import oukokuScraping, oukokuRefresh
from scraping.cmoa import cmoaScraping, cmoaRefresh
from scraping.jumpplus import jumpplusScraping, jumpplusRefresh
from scraping.line import lineScraping, lineRefresh
from scraping.scraping import magapokeScraping, magapokeRefresh
from scraping.piccoma import piccomaScraping, piccomaRefresh
from scraping.ebookjapan import ebookjapanScraping, ebookjapanRefresh

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import os, signal
import time
import sqlite3

# job = cron.new(command='python3 ./scraping-assemble.py')
# 毎週日曜、午前2時にCRONセット
#左から分(0~59)・時(0~23)・日(1~31)・月(1~12)・曜日(0~7)
# job.setall('0 2 * * 7')

magapokeRefresh() #マガポケのスクレイピング関数
# cur.execute("DELETE FROM sqlite_sequence WHERE name = 'origin_magapoke' ")

ebookjapanRefresh()
# ynjnrefresh() #やんじゃんのスクレイピング関数
ynjnRefresh()
# oukokuRefresh() #まんが王国のスクレイピング関数
oukokuRefresh()
# jumpplusRefresh() #ジャンププラスのスクレイピング関数
jumpplusRefresh()
cmoaRefresh() #コミックシーモアのスクレイピング関数
# piccomaRefresh() #ピッコマのスクレイピング関数
piccomaRefresh()
# bookliveRefresh() #bookliveのスクレイピング関数
bookliveRefresh()
# lineRefresh() #liveマンガのスクレイピング関数
lineRefresh()