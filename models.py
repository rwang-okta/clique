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

    def is_active(self):
        return True

    def get_id(self):
        return self.email