from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date
from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True)
    password = Column(String(120))
    name = Column(String(120))

    def __init__(self, email=None, password=None, name=None):
        self.email = email
        self.password = password
        self.name = name

    def __repr__(self):
        return '<User %r>' % (self.email)


class Creds(Base):
    __tablename__ = 'creds'
    id = Column(Integer, primary_key=True)
    oan_app_name = Column(String(120))
    app_version = Column(String(120))
    team = Column(String(120))
    team_contact = Column(String(120))
    login_url = Column(String(120))
    username = Column(String(120))
    password = Column(String(120))
    api_token = Column(String(120))
    security_qa = Column(String(120))
    comments = Column(String(120))
    automation = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id'))
    checkout = Column(Date)
    expire = Column(Date)

    def __repr__(self):
        return '<Creds %r>' % (self.username)

# db = SQLAlchemy(app)

#ROLE_USER = 0
#ROLE_ADMIN = 1

#class User(db.Model):
#    id = db.Column(db.Integer, primary_key = True)
#    nickname = db.Column(db.String(64), index = True, unique = True)
#    email = db.Column(db.String(120), index = True, unique = True)
#    role = db.Column(db.SmallInteger, default = ROLE_USER)

#    def __repr__(self):
#        return '<User %r>' % (self.nickname)

