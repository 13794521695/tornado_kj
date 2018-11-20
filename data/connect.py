'''
sqlalchemy
'''
from sqlalchemy import create_engine

HOSTNAME='192.168.237.131'
PORT='3306'
DATABASE='mydb'
USERNAME='ywy'
PASSWORD='123456'

db_url='mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME,
    PASSWORD,
    HOSTNAME,
    PORT,
    DATABASE
)

engine = create_engine(db_url)   #连接数据库

#创建映像
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(engine)

#创建会话
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(engine)
session = Session()


if __name__=='__main__':
    connection = engine.connect()
    result = connection.execute('select 1')
    print(result.fetchone())