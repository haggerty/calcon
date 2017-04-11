#!/home/phnxrc/anaconda2/bin/python

import sys
import telnetlib
import sqlite3
import datetime
import time

# Turn on or off real-time gain stabilization feature in HCAL

# John Haggerty, BNL, 2016.04.27

HOST = "192.168.100.120"
PORT = "9760"

if len(sys.argv) == 1:
    print "usage: emcalgain.py [off|on]"
    sys.exit(0)

arg1 = str(sys.argv[1]).lower()

try:
    tn = telnetlib.Telnet(HOST,PORT)
except Exception as ex:
    print ex
    print "cannot connect to controller... give up"
    sys.exit()

tn.write( "\n\r")
tn.write( "\n\r")

if arg1 =="on":

    tn.write("$SN")
    g = tn.read_until(">")
    print g
    tn.write( "\n\r")
    
    print "HCAL gain stabilization *ON*"

else:
    tn.write("$SF")
    g = tn.read_until(">")
    print g
    tn.write( "\n\r")
    
    print "HCAL gain stabilization off (the default)"
