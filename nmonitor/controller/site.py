# coding: utf-8
#!/usr/bin/env python

from torneira.controller import BaseController, render_to_extension
from torneira.core.meta import TorneiraSession
from tornado.web import HTTPError
from nmonitor.models.site import Site
from nmonitor.models.user import User
from nmonitor.controller import authenticated

import math
import settings

class SiteController(BaseController):
    
    def view_site(self, site_id, **kw):
        
        site = Site().get(int(site_id))
        request_handler = kw.get('request_handler')
        user_id = request_handler.get_secure_cookie('NMONITOR_ID')
        user = None
        
        if user_id:
            user = User().get(int(user_id))
        
        
        return self.render_to_template("site.html", site=site, user=user)
    
    @authenticated
    def index(self, user, **kw):
        
        site_id = kw.get("site_id")
        site = Site().get(int(site_id)) if site_id else None
        
        return self.render_to_template("new_site.html", site=site, user=user)
    
    @authenticated
    def create(self, **kw):

        site_id = kw.get("site_id")
        site = Site().get(int(site_id)) if site_id else Site()
        
        if kw.get("delete"):
            site.delete()
            kw.get("request_handler").redirect("/")
            
        elif kw.get("save"):
            site.name = kw.get("name")
            site.save()
            kw.get("request_handler").redirect("/site/%s/edit" % site.id)
            
        return
        