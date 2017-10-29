from sqlalchemy import create_engine, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
from uuid import UUID
import datetime, json

engine = create_engine('sqlite:///sqlite.db', echo=False)
Base = declarative_base()


class OutputMixin(object):
    RELATIONSHIPS_TO_DICT = False

    def __iter__(self):
        return self.to_dict().iteritems()

    def to_dict(self, rel=None, backref=None):
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        res = {column.key: getattr(self, attr)
               for attr, column in self.__mapper__.c.items()}
        if rel:
            for attr, relation in self.__mapper__.relationships.items():
                # Avoid recursive loop between to tables.
                if backref == relation.table:
                    continue
                value = getattr(self, attr)
                if value is None:
                    res[relation.key] = None
                elif isinstance(value.__class__, DeclarativeMeta):
                    res[relation.key] = value.to_dict(backref=self.__table__)
                else:
                    res[relation.key] = [i.to_dict(backref=self.__table__)
                                         for i in value]
        return res

    def to_json(self, rel=None):
        def extended_encoder(x):
            if isinstance(x, datetime):
                return x.isoformat()
            if isinstance(x, UUID):
                return str(x)
        if rel is None:
            rel = self.RELATIONSHIPS_TO_DICT
        return json.dumps(self.to_dict(rel), default=extended_encoder)


class User(OutputMixin, Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    trading = relationship("Trading", uselist=False, back_populates="user")
    checking = relationship("Checking", uselist=False, back_populates="user")

    # received_trades = relationship('Trade', back_populates='user')
    # sent_trades = relationship('Trade', back_populates='user')


    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)


class Trade(OutputMixin, Base):
    __tablename__ = 'trade'
    id = Column(Integer, primary_key=True)

    sender_id = Column(Integer, ForeignKey('user.id'))
    sender = relationship("User", foreign_keys=[sender_id])
    sender_account = Column(String)

    receiver_id = Column(Integer, ForeignKey('user.id'))
    receiver = relationship("User", foreign_keys=[receiver_id])
    receiver_account = Column(String)

    amount = Column(Float(precision=3))
    status = Column(String, default="pending")  #pending, accepted, declined


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


class Trading(Base):
    __tablename__ = 'trading'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="trading")

    balance = Column(Float(precision=3), default=10000.00)


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


