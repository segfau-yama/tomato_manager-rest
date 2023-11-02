import psycopg2

# データベースに接続
connection = psycopg2.connect(
    "postgresql://postgres:lYRIXz15NSpu371JXmo4@containers-us-west-119.railway.app:6442/research")

with connection:
    with connection.cursor() as cursor:
        # レコードを挿入
        sql = "DELETE FROM datas_judgement"
        cursor.execute(sql)

    # コミットしてトランザクション実行
    connection.commit()
