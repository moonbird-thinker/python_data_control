from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, insert, update, delete
from sqlalchemy.orm import sessionmaker, declarative_base

# 세번째 방법. sqlalchemy - Core 사용
# PostgreSQL과 연결
db = create_engine("postgresql+psycopg2://postgres:1234@127.0.0.1:5432/postDB")

# 세션 :
Session = sessionmaker(db)
session = Session()

meta = MetaData()

# 테이블 스키마에 맞게 Column 생성 후 테이블 선언
core_table = Table(
    'testDB', meta,
    Column('title', String, primary_key=True),
    Column('posturl', String),
    Column('tweet', String),
)

meta.create_all(db)

# # 1) SELECT ALL
# res = core_table.select()
# result = session.execute(res)
#
# for row in result:
#     print(row)e

# # 2) INSERT
# # INSERT 1건
# stmt = insert(core_table).values(title="title2", posturl="posturl2", tweet="")
#
# with db.connect() as conn:
#     result = conn.execute(stmt)
#     conn.commit()

# # -----------------------------------------------------------------------------
#e
# # INSERT 다수
# stmt = insert(core_table)
# data_list = [
#     {"title": "title3", "posturl": "posturl3", "gender": "M", "tweet": ""},
#     {"title": "title4", "posturl": "posturl4", "gender": "F", "tweet": ""}
#    ]
#
# with db.connect() as conn:
#     result = conn.execute(stmt, data_list)
#     conn.commit()

# 3) UPDATE
stmt = update(core_table).where(core_table.c.title == 'title3').values(tweet='O')

with db.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()

# 4) DELETE
# stmt = delete(core_table).where(core_table.c.title == 'title3')
#
# with db.connect() as conn:
#     result = conn.execute(stmt)
#     conn.commit()