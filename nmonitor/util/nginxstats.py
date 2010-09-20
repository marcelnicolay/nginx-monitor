from rrdcontroller import RRDController
from nmonitor.models.server import Server
from nmonitor.models.site import Site

import re
import sys
import time
import urllib
import os
import logging

class NginxStats():
    
    RRD_PATH = "%s/../../data" % os.path.abspath(os.path.dirname(__file__))
    STATIC_PATH = "%s/../media/image" % os.path.abspath(os.path.dirname(__file__))
    
    def __init__(self):
        self.TIME_SLEEP = time

    def get_rrd(self, server=None, site=None):
        
        if server:
            rrdfile = self.RRD_PATH + "/server_" + str(server.id) + ".rrd"
            imgdir = self.STATIC_PATH + "/server_" + str(server.id)
        elif site:
            rrdfile = self.RRD_PATH + "/site_" + str(site.id) + ".rrd"
            imgdir = self.STATIC_PATH + "/site" + str(site.id)
            
        if not (os.path.isdir(imgdir)):
            os.makedirs(imgdir)
                        
        rrd = RRDController(rrdfile=rrdfile, static_path = imgdir)
        rrd.create()
        return rrd
    
    def parse(self, content):
        result = {}

        match1 = re.search(r'Active connections:\s+(\d+)', content)
        match2 = re.search(r'\s*(\d+)\s+(\d+)\s+(\d+)', content)
        match3 = re.search(r'Reading:\s*(\d+)\s*Writing:\s*(\d+)\s*'
            'Waiting:\s*(\d+)', content)
        if not match1 or not match2 or not match3:
            raise Exception('Unable to parse %s' % content)

        result['connections'] = int(match1.group(1))

        result['accepted'] = int(match2.group(1))
        result['requests'] = int(match2.group(3))

        result['reading'] = int(match3.group(1))
        result['writing'] = int(match3.group(2))
        result['waiting'] = int(match3.group(3))

        return result
                
    def update_rrd(self, rrd, stats):
        rrd.update(connections=stats['connections'], 
                   requests=stats['requests'], 
                   reading=stats['reading'],
                   writing=stats['writing'],
                   waiting=stats['waiting'])
        
        
    def update(self):
        sites = Site().all()
        
        for site in sites:
            
            logging.info("site: " + site.name)
            stats = {'connections':0, 'accepted':0, 'requests':0, 'reading':0, 'writing':0, 'waiting':0}
            
            for server in site.servers:
                logging.info("server: %s,%s"  % (server.name, server.url))
                data = urllib.urlopen(server.url)
                content = data.read()
                result = self.parse(content)
                
                rrd = self.get_rrd(server=server)
                self.update_rrd(rrd, result)
                
                for k,v in result.iteritems(): stats[k] += v
        
            rrd = self.get_rrd(site=site)
            self.update_rrd(rrd, stats)
        
    
    def graph(self):
        
        sites = Site().all()
        for site in sites:
            rrd = self.get_rrd(site=site)
            rrd.graph(period='day')
            rrd.graph(period='week')
            rrd.graph(period='month')
            rrd.graph(period='year')

            for server in site.servers:
                rrd = self.get_rrd(server=server)
                rrd.graph(period='day')
                rrd.graph(period='week')
                rrd.graph(period='month')
                rrd.graph(period='year')
