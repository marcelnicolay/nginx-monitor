# coding: utf-8
#!/usr/bin/env python

from torneira.controller import BaseController, render_to_extension
from torneira.core.meta import TorneiraSession
from tornado.web import HTTPError
from nmonitor.controller import authenticated
from nmonitor.models.server import Server
from nmonitor.models.site import Site

import math
import settings

class ServerController(BaseController):
    
    @authenticated
    def index(self, user, **kw):
        
        server_id = kw.get("server_id")
        server = Server().get(int(server_id)) if server_id else None
        sites = Site().all()
        
        return self.render_to_template("new_server.html", server=server, sites=sites, user=user)
    
    @authenticated
    def create(self, **kw):

        server_id = kw.get("server_id")
        server = Server().get(int(server_id)) if server_id else Server()
        
        if kw.get("delete"):
            server.delete()
            kw.get("request_handler").redirect("/")
            
        elif kw.get("save"):
            server.name = kw.get("name")
            server.url = kw.get("url")
            server.site_id = kw.get('site_id')
            server.save()
            kw.get("request_handler").redirect("/server/%s/edit" % server.id)
            
        return
        