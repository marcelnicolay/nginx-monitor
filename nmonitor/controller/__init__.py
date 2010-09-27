# coding: utf-8
#!/usr/bin/env python

from tornado.web import HTTPError
from torneira.core.meta import TorneiraSession
from nmonitor.models.user import User

import logging

def authenticated(fn):
    def authenticated_fn(self, *args, **kw):
        
        request_handler = kw.get('request_handler')
        user_id = request_handler.get_secure_cookie('NMONITOR_ID')
        user = None
        
        if user_id:
            user = User().get(int(user_id))
        
        if user:
                
            return fn(self, user=user, *args, **kw)
        
        else:
            request_handler.redirect("/")
            return

    return authenticated_fn