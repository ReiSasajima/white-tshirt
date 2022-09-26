from cs50 import SQL

# マガポケのデータベースに接続
db = SQL("sqlite:///manga.db")

# アイコン表示 初期状態は0、1でサービス内で読める 順番は対応
service_name = ["origin_booklive", "origin_cmoa", "origin_ebookjapan", "origin_jumpplus", "origin_line", "origin_magapoke", "origin_oukoku", "origin_piccoma", "origin_ynjn"]
available_services = [0, 0, 0, 0, 0, 0, 0, 0, 0]
# テスト用表示
print(available_services)

num = len(available_services)
title = "犬と屑"

for i in range(0, num):
    test = db.execute("SELECT service_name FROM ? WHERE title = ?", service_name[i], title)
    # 作品名が各テーブルに存在すれば1に変更
    if test != []:
        available_services[i] = 1
# テスト用表示
print(available_services)

