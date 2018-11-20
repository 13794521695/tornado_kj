from datetime import datetime

from sqlalchemy.orm import relationship
import  sys
sys.path.append(r'/home/ywy/tornado_fk1/')
from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey, Table
from  data.connect import  Base,session

class User(Base):           #类对应一个表
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(20),nullable=False)
    password = Column(String(50))
    creatime = Column(DateTime,default=datetime.now)
    _locked = Column(Boolean,default=False,nullable=False)

    @classmethod          #类方法其实就是类自己的方法，调用：类名+方法
    def all(cls):
        return session.query(cls).all()

    @classmethod
    def by_id(cls,id):
        return session.query(cls).filter_by(id=id).all()


    @classmethod
    def by_name(cls,name):
        return session.query(cls).filter_by(username=name).all()

    @property
    def locked(self):         #property 把一个方法变为属性调用，这是访问属性
        return self._locked

    @locked.setter           #修改属性只能通过这种方法。
    def locked(self,value):
        assert isinstance(value,bool)
        self._locked = value

    def __repr__(self):
        return "<User(id='%s',username='%s',password='%s',creatime='%s',_locked='%s')>"%(
            self.id,
            self.username,
            self.password,
            self.creatime,
            self._locked
        )                  #五个字段。

class UserDetails(Base):
    __tablename__='user_details'
    id = Column(Integer,primary_key=True,autoincrement=True)
    id_card = Column(Integer,nullable=True,unique=True)
    lost_login = Column(DateTime)
    login_num = Column(Integer,default=0)
    user_id = Column(Integer,ForeignKey('user.id'), unique=True)

    userdetail = relationship('User',backref='details',uselist=False,cascade='all')

    def __repr__(self):
        return '<UserDetails(id=%s,id_card=%s,last_login=%s,login_num=%s,user_id=%s)>'%(
            self.id,
            self.id_card,
            self.lost_login,
            self.login_num,
            self.user_id
        )


user_article = Table('user_article', Base.metadata,
                     Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
                     Column('article_id', Integer, ForeignKey('article.id'), primary_key=True)
                     )
#中间表，多对多需要借助这个中间表  复合主键

class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(500), nullable=True)
    create_time = Column(DateTime, default=datetime.now)

    article_user = relationship('User', backref='article', secondary=user_article)
#user_article是多对多的关系

    def __repr__(self):
        return 'Article(id=%s, content=%s, creat_time=%s)' % (
            self.id,
            self.content,
            self.create_time
        )






if __name__=='__main__':
    Base.metadata.create_all()              #创建表

