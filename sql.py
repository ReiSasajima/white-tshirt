from cs50 import SQL

# マガポケのデータベースに接続
db = SQL("sqlite:///manga.db")

title = db.execute("SELECT title FROM favorite WHERE user_id = ? AND like = ?", 7, 1)
favorite_db = []
for row in title:
    favorite_db.append(db.execute(
        "SELECT title, author, img_url, summary FROM origin_magapoke WHERE title = ? ", row["title"]))
for row in favorite_db:
    print(row[0]["title"])

example = db.execute(
    "SELECT origin_magapoke.title, origin_magapoke.author FROM origin_magapoke INNER JOIN favorite ON origin_magapoke.title = favorite.title")

keyword = "犬"
book_db = db.execute(
            "SELECT title, author FROM origin_magapoke WHERE title LIKE ? OR author LIKE ?", ('%'+keyword+'%',), ('%'+keyword+'%',))
print(type(example))
print(example)
print(type(book_db))
print(book_db)




