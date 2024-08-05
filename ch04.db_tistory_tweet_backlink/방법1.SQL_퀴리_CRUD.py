# 첫번째 방법. SQL 쿼리를 통한 CRUD

import psycopg2

# database connection 생성
db = psycopg2.connect(host='localhost', dbname='postDB', user='postgres', password='1234', port=5432)

# 커서 생성
cursor = db.cursor()

# CREATE TABLE
# create_query = "CREATE TABLE testDB (id INT PRIMARY KEY, title VARCHAR(32), posturl VARCHAR(32), tweet VARCHAR(32));"
create_query = "CREATE TABLE testDB (title VARCHAR(32) PRIMARY KEY, posturl VARCHAR(32), tweet VARCHAR(32));"

# INSERT DATA
# insert_query = "INSERT INTO testDB VALUES(0, 'sql_post_title1', 'sql_post_postUrl', '');"
insert_query = "INSERT INTO testDB VALUES('sql_post_title1', 'sql_post_postUrl1', 'X');"

# UPDATE DATA
# update_query = """
#             UPDATE testDB
#             SET id = 1,
#                 title = 'sql_post_title1',
#                 posturl = 'sql_post_postUrl',
#                 tweet = 'M',
#             WHERE id = 1,;
#             """
update_query = """
            UPDATE testDB
            SET title = 'sql_post_title1',
                posturl = 'sql_post_postUrl1',
                tweet = 'O'
            WHERE title = 'sql_post_title1';
            """

# DELETE DATA
# delete_query = "DELETE FROM first WHERE id = 1;"
delete_query = "DELETE FROM first WHERE title = 'sql_post_title1';"

# SQL 쿼리 실행
cursor.execute(create_query)
# cursor.execute(insert_query)
# cursor.execute(update_query)
# cursor.execute(delete_query)

# COMMIT 통한 변경 내용 확정
db.commit()