# 두번째 방법. sqlalchemy - ORM 사용

from sqlalchemy import create_engine, Column, INTEGER, VARCHAR
from sqlalchemy.orm import sessionmaker, declarative_base

# PostgreSQL과 연결
db = create_engine("postgresql+psycopg2://postgres:1234@127.0.0.1:5432/postDB")

# 세션 :
Session = sessionmaker(db)
session = Session()

Base = declarative_base()


class First(Base):
    __tablename__ = 'testDB'

    title = Column('title', VARCHAR(256), primary_key=True)
    posturl = Column('posturl', VARCHAR(256), nullable=False)
    tweet = Column('tweet', VARCHAR(4))


# Create
Base.metadata.create_all(db)

# Drop
# First.__table__.drop(db)

# # 1) SELECT ALL
# res = session.query(First).all()
#
# for i in res:
#     print(i.title, i.posturl, i.tweet)

# 2) INSERT
# data1 = First(title='title1', posturl='posturl1', tweet='')
# session.add(data1)

# 3) UPDATE
# session.query(First).filter(First.title == 'title1').update({'title': 'title1', 'posturl': 'posturl1', 'tweet': 'O'})
# session.query(First).filter(First.title == 'title1').update({'tweet': 'X'})

# 4) DELETE
# session.query(First).filter(First.title == 'title1').delete()

# 결과 저장
session.commit()