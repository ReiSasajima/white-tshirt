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
# sessionの暗号化
app.secret_key = 'abcdefghijklmn'
# session継続時間は60分
app.permanent_session_lifetime = timedelta(minutes=60)

keyword = "犬"

for i in service:
            book_db = db.execute(
            "SELECT title, author, service_name FROM ? WHERE title LIKE ? OR author LIKE ?",i , ('%'+keyword+'%',), ('%'+keyword+'%',))

for i in book_db:
    print(f"{i}")
