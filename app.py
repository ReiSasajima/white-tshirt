from flask import Flask, render_template, request
import sqlite3
from cs50 import SQL

# マガポケのデータベースに接続
db = SQL("sqlite:///manga.db")

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("test.html")
    elif request.method == 'POST':
        # name = "keyword"を取得
        keyword = request.form["keyword"]
        # kyewordと一致する作品名、著者名、写真をデータベースより見つける
        title = db.execute("SELECT title FROM magapoke WHERE title  = ? OR author = ?", keyword, keyword)
        author = db.execute("SELECT author FROM magapoke WHERE title = ? OR author = ?", keyword, keyword)
        img = db.execute("SELECT img FROM magapoke WHERE title = ? OR author = ?", keyword, keyword)
        # kyewordと一致する作品または著者のを数える
        book_db = db.execute(
            "SELECT title, author, img FROM magapoke WHERE title = ? OR author = ?", keyword, keyword)
        # 作品が見つからなければNot foundを表示
        if title == []:
            poster = 'Not Found'
            return render_template("test.html", poster=poster)
        elif author == []:
            poster = 'Not Found'
            return render_template("test.html", poster=poster)

        # 作品があれば表示
        book_list ="ヒットした本一覧"
        return render_template("test.html", book_list=book_list, database=book_db)
