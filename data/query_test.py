# 查询结果
import  sys
sys.path.append('/home/ywy/tornado_fk1')
from data.connect import session
from data.user_modules import User, UserDetails


rs = session.query(User).filter(User.username=='budong')
#print(rs)   #打印的是sql语句。
# print(rs, type(rs))

rs = session.query(User).filter(User.username=='budong')[0]
#print(rs)

rs = session.query(User).filter(User.username=='budong').first() #这打印的和上面的一样
#print(rs)

rs = session.query(User).filter(User.username=='budong').all()   #这返回的是列表
# print(rs, type(rs[0]))
# print(getattr(rs[0], 'username'), rs[0].username)  rs[0]是一个类

rs = session.query(User.username).filter(User.username=='budong')
#print(rs)    #打印的也是sql语句

rs = session.query(User.username).filter(User.username=='budong')[0]
#print(rs) #打印的元祖

rs = session.query(User.username).filter(User.username=='budong').all()
#print(rs)   返回的也是一个列表






# 条件查询

# 过滤条件
# print( session.query(User).filter_by(username='budong').all() )
# print( session.query(User).filter(User.username=='budong').all() )
# print( session.query(User).filter(User.username!='budong').all() )
# print( session.query(User).all() )
#print( session.query(User.username).filter(User.username=='tuple').one() )
#print( session.query(User).get(3))  #得到第三条数据

# 模糊匹配
# print( session.query(User.id).filter(User.username.like('budong%')).all() )
# print( session.query(User.id).filter(User.username.notlike('budong%')).all() )

# print( session.query(User.id).filter(User.username.in_(['budong', 'tuple'])).all() )
# print( session.query(User.id).filter(User.username.notin_(['budong', 'tuple'])).all() )

# print( session.query(User.id).filter(User.username==None).all() )
# print( session.query(User.id).filter(User.username.is_(None)).all() )

# print( session.query(User.id).filter(User.username!=None).all() )
# print( session.query(User.id).filter(User.username.isnot(None)).all() )
# print( session.query(User.id).filter(User.username.isnot(None), User.id!=0).all() )
from sqlalchemy import or_
# print( session.query(User.username).filter(or_(User.username.isnot(None),User.password=='qwe123')).all() )

# 限制查询结果数
# print( session.query(User.username).filter(User.username!='budong').all() )
# print( session.query(User.username).filter(User.username!='budong').limit(2).all() ) # 限制
# print( session.query(User.username).filter(User.username!='budong').offset(1).all() ) # 偏移量
# print( session.query(User.username).filter(User.username!='budong').slice(1,3).all() ) # 切片

# 排序
# from sqlalchemy import desc
# print( session.query(User.username).filter(User.username!='budong').order_by(User.id).all() )
# print( session.query(User.username).filter(User.username!='budong').order_by(User.username).limit(3).all() )
# print( session.query(User.username).filter(User.username!='budong').order_by(desc(User.username)).all() )




#聚合函数
from sqlalchemy import func,extract
# print( session.query(User.password,func.count(User.id)).group_by(User.password).all() )
# print( session.query(User.password,func.count(User.id)).group_by(User.password).\
#        having(func.count(User.id)>1).all() )

# print( session.query(User.password,func.sum(User.id)).group_by(User.password).all() )
# print( session.query(User.password,func.max(User.id)).group_by(User.password).all() )
# print( session.query(User.password,func.min(User.id)).group_by(User.password).all() )
#
# print( session.query(extract('minute',User.creatime).label('minute'),\
#                      func.count(User.id)).group_by('minute').all() )   # 提取时间中的分钟来比较
# print( session.query(extract('day',User.creatime).label('day'),\
#                      func.count('*')).group_by('day').all() )

#多表查询

# print( session.query(UserDetails,User) )  #cross join
# print( session.query(UserDetails,User).filter(UserDetails.id==User.id).all() )  #
# print( session.query(UserDetails,User).filter(UserDetails.id==User.id) )  #cross join
# print( session.query(User.username,UserDetails.lost_login).\
#        join(UserDetails,UserDetails.id==User.id) )  #inner join
# print( session.query(User.username,UserDetails.lost_login).\
#        outerjoin(UserDetails,UserDetails.id==User.id).all() )  #left join

q1 = session.query(User.id)
q2 = session.query(UserDetails.id)
# print(q1.union(q2))

from sqlalchemy import all_,any_
sql_0 = session.query(UserDetails.lost_login).subquery()
# print( session.query(User, sql_0.c.lost_login).all() )
# print( session.query(User).filter(User.creatime > all_(sql_0)).all() )
# print( session.query(User).filter(User.creatime > any_(sql_0)).all() )

#原生sql
sql_1='''
    select * from `user`
'''
row = session.execute(sql_1)
print(row,dir(row))
print(row.fetchone())
print(row.fetchmany())
print(row.fetchall())

for i in row:
    pass
    print(i)




