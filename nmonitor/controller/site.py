# coding: utf-8
#!/usr/bin/env python

from torneira.controller import BaseController, render_to_extension
from torneira.core.meta import TorneiraSession
from tornado.web import HTTPError
from nmonitor.models.site import Site

import math
import settings

class SiteController(BaseController):
    
    def view_site(self, site_id, **kw):
        
        site = Site().get(int(site_id))
        
        return self.render_to_template("site.html", site=site)
    
    def index(self, **kw):
        
        site_id = kw.get("site_id")
        site = Site().get(int(site_id)) if site_id else None
        
        return self.render_to_template("new_site.html", site=site)
    
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
        