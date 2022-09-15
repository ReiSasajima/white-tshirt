from cs50 import SQL

# マガポケのデータベースに接続
db = SQL("sqlite:///manga.db")


sample = "sample"
user_id = db.execute("SELECT id FROM users WHERE username = ?", sample)
print(user_id)
