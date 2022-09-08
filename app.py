from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("test.html")
    elif request.method == 'POST':
        # name = "keyword"を取得
        keyword = request.form["keyword"]
        # kyewordと一致する作品をデータベースより見つける
        title = db.execute("SELECT title FROM magapoke WHERE id = ?", id)
        auther = db.execute("SELECT auther FROM magapoke WHERE id = ?", id)
        img = db.execute("SELECT  FROM magapoke WHERE  = ?", id)
        return render_template("test.html", keyword=keyword)

