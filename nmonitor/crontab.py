#!/usr/bin/python
import os, sys, atexit, getopt
import logging

def usage():
    print "\nNginxStats crontab scri[t]:"
    print "usage: crontab.py COMMAND"
    print "\nOs comandos podem ser:"
    print "     update        atualiza os dados"
    print "     graph         gera os graficos"
    print "     help          mostra esse help\n"
    
def main():

    try:
        opts, command = getopt.getopt(sys.argv[1:], "", ["help", "update", "graph"])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    
    if not command or command[0] not in ("help","update","graph") or command[0] == "help":
        usage()
        return
        
    project_root = os.path.abspath(os.path.dirname(__file__))
    sys.path.insert(0, os.path.abspath("%s/.." % project_root))
    
    from nmonitor.util.nginxstats import NginxStats
    
    nstats = NginxStats()
    getattr(nstats, command[0])()

if __name__ == "__main__":
    main()
