# coding: utf-8
#!/usr/bin/env python

from torneira.controller import BaseController, render_to_extension
from tornado.web import HTTPError

import math
import settings

class HomeController(BaseController):
    
    def index(self, **kw):
        
        self.render_to_template("")