import os, sys, atexit, getopt
import re
import sys
import time
import urllib

def usage():
    print "\nNginx Stats Monitor:"
    print "usage: nginxstats.py [--servers=HOST1,HOST2] [--time=TIME_SLEEP] [--help] COMMAND"
    print "\nOs comandos podem ser:"
    print "     help        mostra esse help\n"

def main():

    try:
        optlists, command = getopt.getopt(sys.argv[1:], "hst", ["help", "servers=", "time="])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    servers = []
    time = 5
    
    for opt, value in optlists:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-s", "--servers"):
            servers = [s.strip() for s in value.split(",")]
        elif opt in ("-t", "--time"):
            time = int(value)

    from nginxstats import NginxStats
    nStats = NginxStats(servers, time)
    nStats.loop()

if __name__ == "__main__":
    main()
