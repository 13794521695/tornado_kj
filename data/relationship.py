from .user_modules import session, User, UserDetails, Article

if __name__ == '__main__':
    rows = session.query(User).get(1)
    print(rows)
    print(dir(rows))
    print(rows.details)
    print(rows.article)

    rows = session.query(UserDetails).get(1)
    print(rows)
    print(dir(rows))
    print(rows.userdetail)

    # session.query(UserDetails).filter(UserDetails.user_id==1).update({UserDetails.user_id:3})
    # session.commit()


