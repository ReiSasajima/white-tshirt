from cs50 import SQL

# マガポケのデータベースに接続
db = SQL("sqlite:///manga.db")

index_book = db.execute("SELECT title, author, img_url, summary FROM origin_magapoke ORDER BY RANDOM() LIMIT 10")


print(index_book)