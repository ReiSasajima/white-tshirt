from flask import Flask, redirect, render_template, request, session
from datetime import timedelta
from werkzeug.security import check_password_hash, generate_password_hash
# cs50のライブラリでSQLを操作している。
from cs50 import SQL

# マガポケのデータベースに接続
db = SQL("sqlite:///manga.db")

app = Flask(__name__)

# 各サービスのテーブル名を含むタプル(プログラム内で変更不可)ー－現在はリスト
service = ["origin_magapoke", "origin_line", "origin_oukoku"]
favorite_db = []

# sessionの暗号化
app.secret_key = 'abcdefghijklmn'
# session継続時間は60分
app.permanent_session_lifetime = timedelta(minutes=60)

# 初期ページ
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("sample.html")
        # お気に入り登録用
        # return render_template("rin.html")
    elif request.method == 'POST':
        # ユーザーの入力 = "keyword"を取得
        keyword = request.form["keyword"]
        # kyewordと一致する作品名、著者名、写真をデータベースより見つける(部分一致対応)
        book_db = db.execute(
            "SELECT title, author, img_url, summary FROM origin_magapoke WHERE title LIKE ? OR author LIKE ?", ('%'+keyword+'%',), ('%'+keyword+'%',))
        # 作品が見つからなければNot foundを表示
        if book_db == []:
            poster = 'Not Found'
            return render_template("result.html", poster=poster)
        # 作品があれば表示
        book_list ="ヒットした本一覧"
        return render_template("result.html", book_list=book_list, database=book_db)
        # お気に入り登録の確認用
        # return render_template("rin.html", book_list=book_list, database=book_db)

@app.route("/mypage", methods=["GET", "POST"])
def mypage():
    # sessionを通してログインしているユーザーを確認
    usrsname = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]
    name = usrsname["username"] + "さんこんにちは"
    # お気に入りされた本一覧を表示する
    # ログインユーザのお気に入りの本のタイトルを獲得
    favorite_db = db.execute(
    "SELECT origin_magapoke.title, origin_magapoke.author, origin_magapoke.img_url FROM origin_magapoke INNER JOIN favorite ON origin_magapoke.title = favorite.title")

    if request.method == 'GET':
        return render_template("mypage.html", favorite_db=favorite_db)
    elif request.method == 'POST':
        # ユーザーの入力 = "keyword"を取得
        keyword = request.form["keyword"]
        # kyewordと一致する作品名、著者名、写真をデータベースより見つける(部分一致対応)
        book_db = db.execute(
            "SELECT title, author, img_url, summary FROM origin_magapoke WHERE title LIKE ? OR author LIKE ?", ('%'+keyword+'%',), ('%'+keyword+'%',))
        # 作品が見つからなければNot foundを表示
        if book_db == []:
            poster = 'Not Found'
            return render_template("mypage.html", favorite_db=favorite_db, name=name, poster=poster)
        # 作品があれば表示
        book_list ="ヒットした本一覧"
        return render_template("mypage.html",favorite_db=favorite_db, name=name, book_list=book_list, database=book_db)





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
            #return render_template("login.html", poster=poster)

        # session更新
        user_id = db.execute("SELECT id FROM users WHERE username = ?", username)[0]
        session["user_id"] = user_id["id"]

        name = username

        return render_template("mypage.html", name=name)

@app.route("/logout")
def logout():
    # sessionのクリア
    session.clear()
    return redirect("/")


@app.route("/add_favorite/<title>", methods=["POST"])
def add_favorite(title):
    favorite_book = db.execute("SELECT user_id, title FROM favorite WHERE user_id = ? AND title = ?", session["user_id"], title)
    # まだお気に入りしていなければお気に入り登録 like = 1でお気に入り like=0で解除
    if favorite_book == []:
        like = 1
        # ボタン判定用
        judege = 1
        db.execute("INSERT INTO favorite(user_id, title, like) VALUES (?, ?, ?)", session["user_id"], title, like)
    else:
        #ボタン判定用
        judege = 0
        db.execute("DELETE FROM favorite WHERE user_id = ? AND title = ?", session["user_id"], title)

    return render_template("mypage.html", judege=judege)


