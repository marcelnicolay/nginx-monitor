from pyrrd.rrd import RRD, RRA, DS
from pyrrd.graph import DEF, CDEF, VDEF
from pyrrd.graph import LINE, AREA, GPRINT
from pyrrd.graph import ColorAttributes, Graph
import os, logging, time

class RRDController(object):
    
    def __init__(self, rrdfile="nginxmonitor.rrd"):
        self.rrdfile = rrdfile
        self.graph_request_name = "request.png"
    
    def delete(self):
        os.unlink(self.rrdfile)
           
    def create(self):

        if os.path.exists(self.rrdfile):
            self.rrd = RRD(self.rrdfile)
            return
        
        dss = []
        
        ds1 = DS(dsName="connections", dsType="ABSOLUTE",  heartbeat=120, minval=0, maxval=60000)
        ds2 = DS(dsName="requests", dsType="COUNTER",  heartbeat=120, minval=0, maxval=100000000)
        ds3 = DS(dsName="reading", dsType="ABSOLUTE",  heartbeat=120, minval=0, maxval=60000)
        ds4 = DS(dsName="writing", dsType="ABSOLUTE",  heartbeat=120, minval=0, maxval=60000)
        ds5 = DS(dsName="waiting", dsType="ABSOLUTE",  heartbeat=120, minval=0, maxval=60000)
        dss.extend([ds1,ds2,ds3,ds4,ds5])
        
        rras = []
        rra1 = RRA(cf="AVERAGE", xff=0.5, steps=1, rows=2880)    	
        rra2 = RRA(cf="AVERAGE", xff=0.5, steps=30, rows=672)
        rra3 = RRA(cf="AVERAGE", xff=0.5, steps=120, rows=732)
        rra4 = RRA(cf="AVERAGE", xff=0.5, steps=720, rows=1460)
        rras.extend([rra1, rra2, rra3, rra4])
        
        self.rrd = RRD(self.rrdfile, step=60, ds=dss, rra=rras)
        self.rrd.create(debug=False)
        
    def update(self, connections, requests, reading, writing, waiting):
        self.rrd.bufferValue("%d:%d:%d:%d:%d:%d" % (time.time(),connections, requests, reading, writing, waiting))
        self.rrd.update(template="connections:requests:reading:writing:waiting", debug=True)
     
    def graph(self):
        def1 = DEF(rrdfile=self.rrd.filename, vname='request', dsName="requests", cdef="AVERAGE")
        
        vdef1 = VDEF(vname='max', rpn='request,MAXIMUM')
        vdef2 = VDEF(vname='avg', rpn='request,AVERAGE')
        vdef3 = VDEF(vname='last', rpn='request,LAST')
        
        line1 = LINE(1, defObj=def1, color='#336600', legend='Requests')
        gprint1 = GPRINT(vdef1, "Max\\: %5.1lf %S")
        gprint2 = GPRINT(vdef2, "Avg\\: %5.1lf %S")
        gprint3 = GPRINT(vdef3, "Current\\: %5.1lf %Sreq/sec")
        
        ca = ColorAttributes()
        ca.back = '#333333'
        ca.canvas = '#333333'
        ca.shadea = '#000000'
        ca.shadeb = '#111111'
        ca.mgrid = '#CCCCCC'
        ca.axis = '#FFFFFF'
        ca.frame = '#AAAAAA'
        ca.font = '#FFFFFF'
        ca.arrow = '#FFFFFF'
        
        g = Graph(self.graph_request_name, step='-1day', vertical_label='request/sec', color=ca, width=700, height=150)
        g.data.extend([def1, vdef1, vdef2, vdef3, line1, gprint1, gprint2, gprint3])
        g.write()