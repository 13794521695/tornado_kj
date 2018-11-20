import  sys
from data.connect import session
from data.user_modules import User   #导入表


def add_user():      #增加数据
    person = User(username='budong', password='qwe123')
    session.add(person)
    session.add_all([User(username='tuple', password=2),
                     User(username='which', password=3)])  #添加多条数据。
    session.commit()


def search_user():
    #查询所有
    rows = session.query(User).all()
    print(rows)

    #查询第一条
    rows = session.query(User).first()
    print(rows)

    #查询name='budong'的数据
    rows = session.query(User).filter(User.username=='budong').all()      #返回列表
    print(rows)


def update_user():
    rows = session.query(User).filter(User.username=='budong').update({User.password:1})
    session.commit()


def delete_user():
    rows = session.query(User).filter(User.username=='budong')[0]
    print(rows.username)
    session.delete(rows)
    session.commit()


if __name__ == '__main__':
    add_user()
    #search_user()
    # update_user()
    #delete_user()