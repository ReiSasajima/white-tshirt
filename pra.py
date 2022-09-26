# cs50のライブラリでSQLを操作している。
from cs50 import SQL

# データベースに接続
db = SQL("sqlite:///manga.db")

keyword = "犬"

# ペアレントテーブルから重複しないようにタイトルのみ選択
titles = db.execute(
    "SELECT title FROM parent WHERE title LIKE ? OR author LIKE ? GROUP BY title", ('%'+keyword+'%',), ('%'+keyword+'%',))

print(type(titles))

# 作品名だけのリスト
title_list = []
for i in titles:
    title_list.append(i["title"])
print(title_list)
print(len(title_list))

test = ["犬と屑", "プールと犬"]

# 作品名の数だけプレースホルダの確保
stmt_formats = ','.join(['%s'] * (len(title_list)-1) )
# ペアレントテーブルから重複しないようにタイトル、著者、あらすじ、写真を選択
#name_db = db.execute(f"SELECT title, author, img_url, summary FROM parent IN {tuple(test)}")
#test_db = db.execute(
#    "SELECT title, author, img_url, summary FROM parent WHERE title IN ?", title_list)
book_db = db.execute(
    "SELECT title, author, img_url, summary FROM parent WHERE title IN (%s)" % stmt_formats, tuple(title_list))



