from flask import Flask, redirect, render_template, request, session
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash
# cs50のライブラリでSQLを操作している。
from cs50 import SQL

# マガポケのデータベースに接続
db = SQL("sqlite:///manga.db")

app = Flask(__name__)

# sessionの暗号化
app.secret_key = 'abcdefghijklmn'
# session継続時間は60分
app.permanent_session_lifetime = timedelta(minutes=60)

# 初期ページ
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("sample.html")
    elif request.method == 'POST':
        # ユーザーの入力 = "keyword"を取得
        keyword = request.form["keyword"]
        # kyewordと一致する作品名、著者名、写真をデータベースより見つける(部分一致対応)
        book_db = db.execute(
            "SELECT title, author, img_url FROM origin_magapoke WHERE title LIKE ? OR author LIKE ?", ('%'+keyword+'%',), ('%'+keyword+'%',))
        # 作品が見つからなければNot foundを表示
        if book_db == []:
            poster = 'Not Found'
            return render_template("sample.html", poster=poster)
        # 作品があれば表示
        book_list ="ヒットした本一覧"
        return render_template("sample.html", book_list=book_list, database=book_db)

@app.route("/mypage", methods=["GET", "POST"])
def mypage():
    # sessionを通してログインしているユーザーを確認
    name = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
    if request.method == 'GET':
        return render_template("mypage.html")
    elif request.method == 'POST':
        # ユーザーの入力 = "keyword"を取得
        keyword = request.form["keyword"]
        # kyewordと一致する作品名、著者名、写真をデータベースより見つける(部分一致対応)
        book_db = db.execute(
            "SELECT title, author, img_url FROM origin_magapoke WHERE title LIKE ? OR author LIKE ?", ('%'+keyword+'%',), ('%'+keyword+'%',))
        # 作品が見つからなければNot foundを表示
        if book_db == []:
            poster = 'Not Found'
            return render_template("mypage.html", name=name, poster=poster)
        # 作品があれば表示
        book_list ="ヒットした本一覧"
        return render_template("mypage.html", name=name, book_list=book_list, database=book_db)





@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == 'POST':
        # ユーザー名、パスワード2回分を取得
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # ユーザ名、パスワードが入力されているか確認
        if not username:
            poster = "ユーザ名を入力してください"
            return render_template("register.html", poster1=poster)
        if not password:
            poster = "パスワードを入力してください"
            return render_template("register.html", poster2=poster)
        if not confirmation:
            poster = "確認用パスワードを入力してください"
            return render_template("register.html", poster3=poster)
        if password != confirmation:
            poster = "パスワードと再確認用パスワードが一致しません"
            return render_template("register.html", poster3=poster)
        # パスワードのハッシュ化
        hash = generate_password_hash(password)

        # ユーザ名、ハッシュ化されたパスワードをuserに格納
        try:
            db.execute("INSERT INTO users(username, hash) VALUES (?, ?)", username, hash)
        # すでに登録済みであればposterで返す
        except:
            poster = "このユーザー名は既に使用されています"
            return render_template("register.html", poster=poster)

        # session user_id 登録
        user_id = user_id = db.execute("SELECT id FROM users WHERE username = ?", username)[0]
        session["user_id"] = user_id["id"]

        poster = "登録成功"
        return render_template("sample.html", poster=poster)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        # ユーザ名、パスワードを取得
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            poster = "ユーザー名を入力してください"
            return render_template("login.html", poster1=poster)
        if not password:
            poster = "パスワードを入力してください"
            return render_template("login.html", poster2=poster)

        # ユーザ名と一致する（ユーザー名、ハッシュ化されたパスワード)を取得
        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        #check_password = db.execute("SELECT hash FROM users WHERE username = ?", username)

        # ユーザー名、ハッシュ化されたパスワードがあっているか判定

        if user == [] or not check_password_hash(user[0]["hash"], password):
            poster = "ユーザー名またはパスワードが違います"
            # エラー確認用
            if user == []:
                poster1 = "ユーザ名が違います"
            if not check_password_hash(user[0]["hash"], password):
                poster2 = "パスワードが違います"
            return render_template("login.html", poster=poster, poster1=poster1, poster2=poster2)

        # session更新
        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)[0]
        session["user_id"] = user_id["id"]

        name = username + "さんこんにちは"

        return render_template("mypage.html", name=name)

@app.route("/logout")
def logout():
    # sessionのクリア
    session.clear()
    return redirect("/")



