# coding: utf-8
#!/usr/bin/env python

from torneira.controller import BaseController, render_to_extension
from torneira.core.meta import TorneiraSession
from tornado.web import HTTPError
from nmonitor.models.site import Site

import math
import settings

class SiteController(BaseController):
    
    def index(self, site_id, **kw):
        
        site = Site().get(int(site_id))
        
        return self.render_to_template("site.html", site=site)