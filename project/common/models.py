from sqlalchemy import create_engine, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///sqlite.db', echo=False)
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    trading = relationship("Trading", uselist=False, back_populates="user")
    checking = relationship("Checking", uselist=False, back_populates="user")

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)


class Trading(Base):
    __tablename__ = 'trading'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="trading")

    balance = Column(Float(precision=3), default=10000.00)

class Trade(Base):
    __tablename__ = 'trade'
    id = Column(Integer, primary_key=True)
    sender = relationship("User", back_populates="trade")
    receiver = relationship("User", back_populates="trade")
    amount = Column(Float(precision=3))
    status = Column(String)  #pending, accepted, declined


'''
For each user, there will be a list of trades seperated by whether the user was the sender or the receiver
Sender trades:
- There will be pending, accepted, and declined trades
- If accepted, the money will be successfully transferred
- If declined, then either receiver didnt have enough money, sender didnt have enough money, or was simply declined!x
- If pending, simply display trade amount and a pending status

Receiver trades:
- There will be pending, accepted, and declined trades
- If pending, display 2 buttons, one that says accept and one that says decline
- If accepted, initiate the trade transfer and show in accepted trades
- If declined, display as a declined trade

'''


class Checking(Base):
    __tablename__ = 'checking'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="checking")

    balance = Column(Float(precision=3), default=10000.00)



Base.metadata.create_all(engine)


# Communicating with the Database
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


