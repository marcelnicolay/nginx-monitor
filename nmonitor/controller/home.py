# coding: utf-8
#!/usr/bin/env python

from torneira.controller import BaseController, render_to_extension
from torneira.core.meta import TorneiraSession
from tornado.web import HTTPError
from nmonitor.models.site import Site

import math
import settings

class HomeController(BaseController):
    
    def index(self, **kw):
        
        sites = Site().all()
        return self.render_to_template("sites.html", sites=sites)