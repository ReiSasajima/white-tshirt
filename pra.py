# cs50のライブラリでSQLを操作している。
from cs50 import SQL

# マガポケのデータベースに接続
db = SQL("sqlite:///manga.db")

app = Flask(__name__)

# 各サービスのテーブル名を含むタプル(プログラム内で変更不可)
service = ["origin_magapoke", "origin_line", "origin_oukoku"]

# 漫画一覧のプログラムテスト
book = []
keyword = "犬"
for i in service:
    book.append(db.execute("SELECT title, author, service_name FROM ? WHERE title LIKE ?", i, ('%'+keyword+'%',)))

for i in book:
    print(i)

