from flask import Flask, render_template, request
import sqlite3
from cs50 import SQL
# マガポケのデータベースに接続
conn = sqlite3.connect('magapoke.db')
db = SQL("sqlite:///magapoke.db")
conn.close()

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("test.html")
    elif request.method == 'POST':
        # name = "keyword"を取得
        keyword = request.form["keyword"]
        # kyewordと一致する作品をデータベースより見つける
        #book_db = db.execute(
        #    "SELECT title, auther, img FROM magapoke WHERE title LIKE '%?%' OR auther LIKE '%?%'", keyword, keyword)
        # 作品が見つからなければNot foundを表示
        title = db.execute("SELECT title FROM magapoke WHERE title LIKE '%?%'", keyword)
        if title == None:
            poster = 'Not Found'
            return render_template("test.html", poster=poster)
        # 作品があれば表示
        return render_template("test.html", title=title)

