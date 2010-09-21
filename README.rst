Nginx Monitor
======================

Nginx-monitor is a network graphing solution designed to harness the power of RRDTool_ data storage and the flexibility of Nginx status module. It's a easily and practice solution, written in python, to monitoring Nginx servers in production enviroments.

Quick start
==========

 1. Install the dependencies
 2. make a clone of this repository
 3. make db 'create mysql database'
 4. make start 'run server in port 8888'
 5. add update script in crontab
	
	>>> crontab -e
	* * * * * python /nginx-monitor/nmonitor/crontab.py update >> /nginx-monitor/nmonitor/crontab.out.txt 2>&1
	0-59/5 * * * * python /nginx-monitor/nmonitor/crontab.py graph >> /nginx-monitor/nmonitor/crontab.out.txt 2>&1
	30 * * * * cp /nginx-monitor/data/* /rrd.backup/


Dependencies
============

 * Tornado_ >= 0.2
 * Mako_ >= 0.3.2
 * SqlAlchemy_ >= 0.5.6
 * nose_ >= 0.11.0
 * mox_ >= 0.5.1
 * simplejson_
 * simplexml_
 * Torneira_
 * PyRRD_
 * simple-db-migrate_
 * MySQL_

Contributing
============

With new features
^^^^^^^^^^^^^^^^^

 1. Create both unit and functional tests for your new feature
 2. Do not let the coverage go down, 100% is the minimum.
 3. Write properly documentation
 4. Send-me a patch with: ``git format-patch``

.. _Tornado: http://www.tornadoweb.org/
.. _Mako: http://www.makotemplates.org/
.. _SqlAlchemy: http://www.sqlalchemy.org/
.. _nose: http://code.google.com/p/python-nose/
.. _mox: http://code.google.com/p/pymox/test
.. _simplejson: http://code.google.com/p/simplejson/
.. _simplexml: http://github.com/marcelnicolay/simplexml
.. _Torneira: http://github.com/marcelnicolay/torneira
.. _RRDTool's: http://oss.oetiker.ch/rrdtool/
.. _PyRRd: http://code.google.com/p/pyrrd/
.. _simple-db-migrate: http://github.com/guilhermechapiewski/simple-db-migrate
.. _mysql: http://www.mysql.com

E-mail: marcel.nicolay at gmail com
