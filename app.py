from flask import Flask, render_template, request
import sqlite3

# マガポケのデータベースに接続
conn = sqlite3.connect('magapoke.db')
db = SQL("sqlite:///magapoke.db")

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("test.html")
    elif request.method == 'POST':
        # name = "keyword"を取得
        keyword = request.form["keyword"]
        # kyewordと一致する作品をデータベースより見つける
        title = db.execute("SELECT title FROM magapoke WHERE title LIKE %keyword% OR auther LIKE %keyword%")
        auther = db.execute("SELECT auther FROM magapoke WHERE title LIKE %keyword% OR auther LIKE %keyword%")
        img = db.execute("SELECT  img FROM magapoke WHERE titleLIKE %keyword% OR auther LIKE %keyword%")
        # 作品が見つからなければNot foundを表示
        if title == None and auther == None and img == None:
            poster = 'Not Found'
            return render_template("test.html", poster=poster)
        # 作品があれば表示
        return render_template("test.html", title=title, auther=auther, img=img)

