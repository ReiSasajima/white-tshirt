from flask import Flask, redirect, render_template, request, session
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash
# cs50のライブラリでSQLを操作している。
from cs50 import SQL

# マガポケのデータベースに接続
db = SQL("sqlite:///manga.db")

app = Flask(__name__)

# 各サービスのテーブル名を含むタプル(プログラム内で変更不可)
service = ["origin_magapoke", "origin_line", "origin_oukoku"]
NUM = len(service)

keyword = "犬"

# 全テーブルから重複しないようにタイトルのみ選択
titles = db.execute(
    "SELECT title FROM parent WHERE title LIKE ? OR author LIKE ? GROUP BY title", ('%'+keyword+'%',), ('%'+keyword+'%',))
# 全テーブルから重複しないようにタイトル、著者、あらすじ、写真を選択
book_db = db.execute(
    "SELECT title, author, img_url, summary FROM origin_magapoke WHERE title ?", titles)
