from pyrrd.rrd import RRD, RRA, DS
from pyrrd.graph import DEF, CDEF, VDEF
from pyrrd.graph import LINE, AREA, GPRINT
from pyrrd.graph import ColorAttributes, Graph
import os, logging, time

class RRDController(object):

    def __init__(self, rrdfile, static_path):
        
        self.rrdfile = rrdfile
        self.static_path = static_path
        
    def delete(self):
        os.unlink(self.rrdfile)
           
    def create(self):

        if os.path.exists(self.rrdfile):
            self.rrd = RRD(self.rrdfile)
            return
        
        dss = []
        
        ds1 = DS(dsName="requests", dsType="COUNTER",  heartbeat=120, minval=0, maxval=100000000)
        ds2 = DS(dsName="connections", dsType="ABSOLUTE",  heartbeat=120, minval=0, maxval=60000)
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
        time.sleep(2)
        
    def update(self, connections, requests, reading, writing, waiting):
        self.rrd.bufferValue("%d:%d:%d:%d:%d:%d" % (time.time(),connections, requests, reading, writing, waiting))
        self.rrd.update(template="connections:requests:reading:writing:waiting", debug=True)
    
    def graph_request(self, period='day'):
        def1 = DEF(rrdfile=self.rrdfile, vname='request', dsName="requests", cdef="AVERAGE")
        
        vdef1 = VDEF(vname='max', rpn='request,MAXIMUM')
        vdef2 = VDEF(vname='avg', rpn='request,AVERAGE')
        vdef3 = VDEF(vname='last', rpn='request,LAST')
        
        area1 = AREA(defObj=def1, color='#336600', legend='Requests')
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
        
        img = "request-%s.png" % period
        imgname = self.static_path +"/"+ img
        start = '-1'+period
        
        g = Graph(imgname, imgformat='PNG', step=start, vertical_label='request/sec', color=ca, width=700, height=150)
        g.data.extend([def1, vdef1, vdef2, vdef3, area1, gprint1, gprint2, gprint3])
        g.write()

    def graph_connection(self, period='day'):
        def1 = DEF(rrdfile=self.rrdfile, vname='connections', dsName="connections", cdef="AVERAGE")
        def2 = DEF(rrdfile=self.rrdfile, vname='reading', dsName="reading", cdef="AVERAGE")
        def3 = DEF(rrdfile=self.rrdfile, vname='writing', dsName="writing", cdef="AVERAGE")
        def4 = DEF(rrdfile=self.rrdfile, vname='waiting', dsName="waiting", cdef="AVERAGE")

        # TOTAL
        vdef1 = VDEF(vname='max', rpn='connections,MAXIMUM')
        vdef2 = VDEF(vname='avg', rpn='connections,AVERAGE')
        vdef3 = VDEF(vname='last', rpn='connections,LAST')
        vdef4 = VDEF(vname='min', rpn='connections,MINIMUM')

        line1 = LINE(1, defObj=def1, color='#22FF22', legend='Total')
        gprint1 = GPRINT(vdef1, "Max\\: %5.1lf %S")
        gprint2 = GPRINT(vdef2, "Avg\\: %5.1lf %S")
        gprint3 = GPRINT(vdef3, "Current\\: %5.1lf %S")
        gprint4 = GPRINT(vdef4, "Min\\: %5.1lf %S\\n")

        # READING
        reading_vdef1 = VDEF(vname='rmax', rpn='reading,MAXIMUM')
        reading_vdef2 = VDEF(vname='ravg', rpn='reading,AVERAGE')
        reading_vdef3 = VDEF(vname='rlast', rpn='reading,LAST')
        reading_vdef4 = VDEF(vname='rmin', rpn='reading,MINIMUM')

        line2 = LINE(1, defObj=def2, color='#0022FF', legend='Reading')
        reading_gprint1 = GPRINT(reading_vdef1, "Max\\: %5.1lf %S")
        reading_gprint2 = GPRINT(reading_vdef2, "Avg\\: %5.1lf %S")
        reading_gprint3 = GPRINT(reading_vdef3, "Current\\: %5.1lf %S")
        reading_gprint4 = GPRINT(reading_vdef4, "Min\\: %5.1lf %S\\n")

        # writing
        writing_vdef1 = VDEF(vname='wmax', rpn='writing,MAXIMUM')
        writing_vdef2 = VDEF(vname='wavg', rpn='writing,AVERAGE')
        writing_vdef3 = VDEF(vname='wlast', rpn='writing,LAST')
        writing_vdef4 = VDEF(vname='wmin', rpn='writing,MINIMUM')

        line3 = LINE(1, defObj=def3, color='#FF0000', legend='Writing')
        writing_gprint1 = GPRINT(writing_vdef1, "Max\\: %5.1lf %S")
        writing_gprint2 = GPRINT(writing_vdef2, "Avg\\: %5.1lf %S")
        writing_gprint3 = GPRINT(writing_vdef3, "Current\\: %5.1lf %S")
        writing_gprint4 = GPRINT(writing_vdef4, "Min\\: %5.1lf %S\\n")

        # WAITING
        waiting_vdef1 = VDEF(vname='wamax', rpn='waiting,MAXIMUM')
        waiting_vdef2 = VDEF(vname='waavg', rpn='waiting,AVERAGE')
        waiting_vdef3 = VDEF(vname='walast', rpn='waiting,LAST')
        waiting_vdef4 = VDEF(vname='wamin', rpn='waiting,MINIMUM')

        line4 = LINE(1, defObj=def4, color='#00AAAA', legend='Waiting')
        waiting_gprint1 = GPRINT(waiting_vdef1, "Max\\: %5.1lf %S")
        waiting_gprint2 = GPRINT(waiting_vdef2, "Avg\\: %5.1lf %S")
        waiting_gprint3 = GPRINT(waiting_vdef3, "Current\\: %5.1lf %S")
        waiting_gprint4 = GPRINT(waiting_vdef4, "Min\\: %5.1lf %S\\n")

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

        img = "connection-%s.png" % period
        imgname = self.static_path +"/"+ img
        start = '-1'+period

        g = Graph(imgname, imgformat='PNG', step=start, vertical_label='connections', color=ca, width=700, height=150)
        g.data.extend([def1, vdef1, vdef2, vdef3, vdef4, line1, gprint1, gprint2, gprint3, gprint4])
        g.data.extend([def2, reading_vdef1, reading_vdef2, reading_vdef3, reading_vdef4, line2, reading_gprint1, reading_gprint2, reading_gprint3, reading_gprint4])
        g.data.extend([def3, writing_vdef1, writing_vdef2, writing_vdef3, writing_vdef4, line3, writing_gprint1, writing_gprint2, writing_gprint3, writing_gprint4])
        g.data.extend([def4, waiting_vdef1, waiting_vdef2, waiting_vdef3, waiting_vdef4, line4, waiting_gprint1, waiting_gprint2, waiting_gprint3, waiting_gprint4])
        g.write()
		
    def graph(self, period='day'):
        
        self.graph_request(period)
        self.graph_connection(period)