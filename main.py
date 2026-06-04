import psycopg2
from sqlalchemy import create_engine,Column,Integer,String,Boolean,asc,desc
from sqlalchemy.orm import DeclarativeBase,sessionmaker
import random,time
from datetime import  datetime as dt
from faker import Faker

engine=create_engine('postgresql+psycopg2://postgres:1234@localhost/users')
Session=sessionmaker(engine)
fake=Faker('ru_RU')

class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    age=Column(Integer,nullable=False)
    studying=Column(Boolean,nullable=False)
    money=Column(Integer,default=1111)

    def user_info(self):
        return (f'{self.id}. {self.name} - {self.age} years old, {"in studying" if self.studying else "not in studying"}'
                f' {self.money}$')



class Dogs(Base):
    __tablename__ = 'dogs'
    id=Column(Integer,primary_key=True)
    breed=Column(String,nullable=False)
    name=Column(String,nullable=False)
    owner=Column(Boolean,nullable=False)
    age=Column(Integer,nullable=False)
    color=Column(String,nullable=False)


Base.metadata.create_all(engine)

# with Session() as session:
#     user=Users(name='Ola',age=77,studying=False,money=62142)
#     session.add(user)
#     session.commit()

# with Session() as session:
#     start=dt.now()
#     for x in range(50000):
#         name=fake.first_name()
#         age=random.randint(0, 120)
#         studying=True if age in range(6, 26) else False
#         money=random.randint(52, 999999)
#         user=Users(name=name, age=age, studying=studying, money=money)
#         session.add(user)
#     session.commit()
#     print(dt.now()-start)

# with Session() as session:
#     users=session.query(Users).all()
#     for user in users:
#         print(user.user_info())

with Session() as session:
    user=session.get(Users,10000) # способ получения информации о пользователе через первичный ключ
    print(user.user_info())


with Session() as session:
    session.query(Users).filter(Users.id==98993).update({'age':89})
    session.query(Users).filter(Users.id==99558).delete()
    session.commit()


with Session() as session:
    some_users=session.query(Users).filter(Users.id<=99999, Users.name=='Александр').order_by(asc(Users.money))
    all_users=session.query(Users).all()
    for user in some_users:
        print(user.user_info())

    kolvo_users=some_users.count()
    vse_users=len(all_users)
    print(round(kolvo_users/vse_users*100,2),'%')
    print(kolvo_users)
    print(vse_users)