# cs50のライブラリでSQLを操作している。
from cs50 import SQL

# マガポケのデータベースに接続
db = SQL("sqlite:///manga.db")

# 各サービスのテーブル名を含むタプル(プログラム内で変更不可)
service = ["origin_magapoke", "origin_line", "origin_oukoku"]

keyword = "犬"

# ペアレントテーブルから重複しないようにタイトルのみ選択
titles = db.execute(
    "SELECT title FROM parent WHERE title LIKE ? OR author LIKE ? GROUP BY title", ('%'+keyword+'%',), ('%'+keyword+'%',))
print(titles)
# ペアレントテーブルから重複しないようにタイトル、著者、あらすじ、写真を選択
book_db = db.execute(
    "SELECT title, author, img_url, summary FROM origin_magapoke WHERE title ?", titles)


