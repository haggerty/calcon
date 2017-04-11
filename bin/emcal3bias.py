#!/home/phnxrc/anaconda2/bin/python

# Sets EMCAL DAC's to nominal values

# John Haggerty, BNL, 2016.03.17

import sys
import telnetlib
import sqlite3
import datetime

HOST = "192.168.100.110"
PORT = "9760"

try:
    tn = telnetlib.Telnet(HOST,PORT)
except Exception as ex:
    print ex
    print "cannot connect to controller... give up"
    sys.exit()

tn.write( "\n\r")
tn.write( "\n\r")

prefix = "$GS1"
vd = [line.rstrip('\n') for line in open('/home/phnxrc/calcon/config/emc3book.dat')]

i = 0
for v in vd:
    s = '%s%02d%s\n\r' % (prefix,i,v)
    print s
    tn.write(s)
    print "reading..."
    g = tn.read_until(">")
    print g
    i+=1 

tn.write( "\n\r")

print "loaded default bias values from /home/phnxrc/calcon/config/emc3book.dat"
