#!/home/phnxrc/anaconda2/bin/python

import sys
import telnetlib
import sqlite3
import datetime
import time

# Turn on or off LED's in EMCAL, mask all on or off

# John Haggerty, BNL, 2016.03.18

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

if len(sys.argv) == 1:
    print "usage: hcalled.py [on|off]"
    sys.exit(0)

arg1 = str(sys.argv[1]).lower()

if arg1 =="on":

    tn.write("$P000FF")
    g = tn.read_until(">")
    print g
    tn.write( "\n\r")

    print "TP on"

else:
    
    tn.write("$P00000")
    g = tn.read_until(">")
    print g
    tn.write( "\n\r")

    print "TP off masks 0"
    
