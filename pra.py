from werkzeug.security import check_password_hash, generate_password_hash

password = "rin"
hash = generate_password_hash(password)
reslut = check_password_hash(hash, password)

if not reslut:
    print("パスワード不一致")
else:
    print("パスワード一致")