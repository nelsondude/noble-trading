from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker



engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)

print(User.__table__)

Base.metadata.create_all(engine)

ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
print(ed_user.name)
print(ed_user.password)
print(str(ed_user.id))

# Communicating with the Database
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
session.add(ed_user)

# print(session.query(User))

our_user = session.query(User).filter_by(name='ed').first()
print(our_user)

session.add_all([
    User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')])

# print(session.query(User))
ed_user.password = 'moresecure'
print(session.dirty)
session.commit()
print(str(ed_user.id))

# Roll Back
ed_user.name = 'Edwardo'

fake_user = User(name='fakeuser', fullname='Invalid', password='12345')
session.add(fake_user)
print(session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all())
session.rollback()
print(session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all())


# Querying
for name, fullname in session.query(User.name, User.fullname):
    print(name, fullname)

# Returning Lists/Scalars
query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
print(query.all())
print(query.count())


# Foreign Keys

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address

User.addresses = relationship(
    "Address", order_by=Address.id, back_populates="user")

# Create Tables in Database
Base.metadata.create_all(engine)

# Working with related objects
jack = User(name='jack', fullname='Jack Bean', password='gjffdd')
jack.addresses = [
               Address(email_address='jack@google.com'),
                Address(email_address='j25@yahoo.com')]
# Cascading since it creates an Address as well
session.add(jack)
session.commit()

# Join Querying
for u, a in session.query(User, Address).\
                    filter(User.id==Address.user_id).\
                    filter(Address.email_address=='jack@google.com').\
                    all():
    print(u)
    print(a)

# SQL Join Syntax
print(session.query(User).join(Address).\
        filter(Address.email_address=='jack@google.com').\
        all())

# Alias's
from sqlalchemy.orm import aliased

adalias1 = aliased(Address)
adalias2 = aliased(Address)
for username, email1, email2 in \
    session.query(User.name, adalias1.email_address, adalias2.email_address).\
    join(adalias1, User.addresses).\
    join(adalias2, User.addresses).\
    filter(adalias1.email_address=='jack@google.com').\
    filter(adalias2.email_address=='j25@yahoo.com'):
    print(username, email1, email2)

# Deleting Objects
session.delete(jack)
print(session.query(User).filter_by(name='jack').count())


# RESTARTING THE SESSION

session.close()
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    addresses = relationship("Address", back_populates='user',
                    cascade="all, delete, delete-orphan")
    def __repr__(self):
       return "<User(name='%s', fullname='%s', password='%s')>" % (
                               self.name, self.fullname, self.password)


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="addresses")
    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address

jack = session.query(User).get(5)
session.delete(jack)
print(session.query(Address).filter(
   Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])
).count())


# Many To Many Relationship
from sqlalchemy import Table, Text
# association table
post_keywords = Table('post_keywords', Base.metadata,
    Column('post_id', ForeignKey('posts.id'), primary_key=True),
    Column('keyword_id', ForeignKey('keywords.id'), primary_key=True)
)

class BlogPost(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    headline = Column(String(255), nullable=False)
    body = Column(Text)

    # Many to many relationship
    keywords = relationship('Keyword',
                           secondary=post_keywords,
                           back_populates='posts')

    def __init__(self, headline, body, author):
        self.author = author
        self.headline = headline
        self.body = body

    def __repr__(self):
        return "Blogpost( %r, %r, %r)" % (self.headline, self.body, self.author)


class Keyword(Base):
    __tablename__ = 'keywords'
    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)
    posts = relationship('BlogPost',
                         secondary=post_keywords,
                         back_populates='keywords')
    def __init__(self, keyword):
        self.keyword = keyword

# Add Another Relationship
BlogPost.author = relationship(User, back_populates="posts")
User.posts = relationship(BlogPost, back_populates="author", lazy="dynamic")

Base.metadata.create_all(engine)

wendy = session.query(User).\
                filter_by(name='wendy').\
                one()
post = BlogPost("Wendy's Blog Post", "This is a test", wendy)
session.add(post)

# Add Some Keywords
post.keywords.append(Keyword('wendy'))
post.keywords.append(Keyword('firstpost'))

print(session.query(BlogPost).\
            filter(BlogPost.keywords.any(keyword='firstpost')).\
            all())