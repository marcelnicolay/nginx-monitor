# coding: utf-8
#!/usr/bin/env python

from torneira.core import meta
from torneira.core.meta import TorneiraSession
from torneira.models.base import Model, Repository
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relation
from sqlalchemy.orm.exc import NoResultFound
from nmonitor.models.server import Server

class UserRepository(Repository):

    @staticmethod
    def doLogin(login, password):
        
        session = TorneiraSession()
        
        try:
            user = session.query(User).filter(User.login == login).filter(User.password==password).one()
            return user
        except NoResultFound:
            return None
	
class User(Model, UserRepository):

    __tablename__ = 'user'
    
    id = Column('user_id', Integer, primary_key=True)
    login = Column('login', String)
    password = Column('password', String)