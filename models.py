from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Date
from database import Base


class User(Base):
    __tablename__ = 'users'
    email = Column(String(120), unique=True, primary_key=True)
    password = Column(String(120))

    def __init__(self, email=None, password=None):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.email)

    def is_active(self):
        return True

    def get_id(self):
        return self.email

class Creds(Base):
    __tablename__ = 'creds'
    id = Column(Integer, primary_key=True)
    org = Column(String(120))
    oan_app_name = Column(String(120))
    #app_version = Column(String(120))
    team = Column(String(120))
    team_contact = Column(String(120))
    login_url = Column(String(120))
    username = Column(String(120))
    password = Column(String(120))
    #api_token = Column(String(120))
    #security_qa = Column(String(120))
    comment = Column(String(120))
    #automation = Column(Boolean)
    user = Column(String(120))
    checkout = Column(Date)
    expire = Column(Date)

    def __init__(self, oan_app_name=None, comment=None, user=None,  login_url=None, username=None, password=None, checkout=None, expire=None):
        self.oan_app_name = oan_app_name
        self.comment = comment
        self.user = user
        self.login_url = login_url;
        self.username = username;
        self.password = password;
        self.checkout = checkout
        self.expire = expire

    def __repr__(self):
        return '<Creds %r>' % (self.username)