from sqlalchemy import Column, String
from database import Base

class User(Base):
    __tablename__ = 'users'
    email = Column(String(120), unique=True, primary_key=True)
    password = Column(String(120), unique=True)

    def __init__(self, email=None, password=None):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.email)

#db = SQLAlchemy(app)

#ROLE_USER = 0
#ROLE_ADMIN = 1

#class User(db.Model):
#    id = db.Column(db.Integer, primary_key = True)
#    nickname = db.Column(db.String(64), index = True, unique = True)
#    email = db.Column(db.String(120), index = True, unique = True)
#    role = db.Column(db.SmallInteger, default = ROLE_USER)

#    def __repr__(self):
#        return '<User %r>' % (self.nickname)

