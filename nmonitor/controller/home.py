# coding: utf-8
#!/usr/bin/env python

from torneira.controller import BaseController, render_to_extension
from torneira.core.meta import TorneiraSession
from tornado.web import HTTPError
from nmonitor.models.site import Site
from nmonitor.models.user import User

import math
import settings

class HomeController(BaseController):
    
    def index(self, **kw):
        
        sites = Site().all()

        request_handler = kw.get('request_handler')
        user_id = request_handler.get_secure_cookie('NMONITOR_ID')
        user = None
        
        if user_id:
            user = User().get(int(user_id))
            
        return self.render_to_template("sites.html", sites=sites, user=user)
    
    def login(self, **kw):

        login = kw.get('login')
        password = kw.get('password')
        request_handler = kw.get('request_handler')
        
        user = User.doLogin(login=login,password=password)
        if user:
            request_handler.set_secure_cookie(name="NMONITOR_ID", value=str(user.id), path="/", expires_days=None)
        
        request_handler.redirect("/")
        return