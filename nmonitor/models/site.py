# coding: utf-8
#!/usr/bin/env python

from torneira.core import meta
from torneira.core.meta import TorneiraSession
from torneira.models.base import Model, Repository
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relation
from sqlalchemy.orm.exc import NoResultFound

class SiteRepository(Repository):

    pass        
	
class Site(Model, SiteRepository):

    __tablename__ = 'site'
    
    id = Column('site_id', Integer, primary_key=True)
    name = Column('name', String)