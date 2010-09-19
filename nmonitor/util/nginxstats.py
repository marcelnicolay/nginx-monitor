from rrdcontroller import RRDController
import re
import sys
import time
import urllib

class NginxStats():
        
    def __init__(self):
        #self.servers = servers
        self.prev = {'accepted':0, 'requests':0}
        self.total = {'connections':0, 'accepted':0, 'requests':0, 'reading':0, 'writing':0, 'waiting':0}
        self.count = 0
        
        self.TIME_SLEEP = time
        
        self.rrd = RRDController()
        #self.rrd.delete()
        self.rrd.create()
    
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
        
    def update(self):

        stats = {'connections':0, 'accepted':0, 'requests':0, 'reading':0, 'writing':0, 'waiting':0}
        for server in self.servers:
            data = urllib.urlopen(server)
            content = data.read()
            result = self.parse(content)
            for k,v in result.iteritems(): stats[k] += v
        
        self.rrd.update(connections=stats['connections'], 
                        requests=stats['requests'], 
                        reading=stats['reading'],
                        writing=stats['writing'],
                        waiting=stats['waiting'])
    
    def graph(self):
        self.rrd.graph()
