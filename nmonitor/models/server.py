# coding: utf-8
#!/usr/bin/env python

from torneira.core import meta
from torneira.core.meta import TorneiraSession
from torneira.models.base import Model, Repository
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relation
from sqlalchemy.orm.exc import NoResultFound

class ServerRepository(Repository):

    pass
	
class Server(Model, ServerRepository):

    __tablename__ = 'server'
    
    id = Column('server_id', Integer, primary_key=True)
    site_id = Column('site_id', Integer, ForeignKey('site.site_id'))
    name = Column('name', String)
    url = Column('url', String)