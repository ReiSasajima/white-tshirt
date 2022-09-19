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
favorite_book = db.execute("SELECT title FROM favorite WHERE user_id = ? AND like = ?", 7, 1)[0]
favorite_title = favorite_book
print(type(favorite_title ))
print(f"{favorite_title }")

keyword = "犬"
book_db = db.execute(
            "SELECT title, author, img_url, summary FROM origin_magapoke WHERE title LIKE ? OR author LIKE ?", ('%'+keyword+'%',), ('%'+keyword+'%',))
print(type(book_db))
print(book_db)

