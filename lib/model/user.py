# -*- coding: utf-8 -*-

from sqlalchemy import Column, ColumnDefault
from sqlalchemy.types import Unicode, Integer, Boolean
from sqlalchemy import func

from passlib.hash import sha512_crypt

from lib.model import Base

__all__ = ['User']

class User(Base):
    __tablename__ = 'user'

    username = Column(Unicode, nullable=False, primary_key=True)
    email = Column(Unicode)
    name = Column(Unicode)
    passwd = Column(Unicode)
    is_admin = Column(Boolean, default=0)

    @staticmethod
    def get(session, username):
        return session.query(User).filter(User.username == username).first()    

    @staticmethod
    def get_all(session):
        return session.query(User)

    @staticmethod
    def get_all_admin(session):
        return session.query(User).filter(User.is_admin == True)

    @staticmethod
    def authenticate(session, username, password):
        u = User.get(session, username)

        if u is not None:
            h = u.passwd
            return h is not None and sha512_crypt.verify(password, h)

        return False

    @staticmethod
    def user_exists(session, username):
        return session.query(User).filter(User.username == username).count() 

    @staticmethod
    def set_password(session, username, new_password):
        new_hash = sha512_crypt.encrypt(new_password)

        u = User.get(session, username)

        if u is not None:
            u.passwd = new_hash
