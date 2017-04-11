#!/home/phnxrc/anaconda2/bin/python

import sys
import telnetlib
import sqlite3
import datetime

HOST = "192.168.100.120"
PORT = "9760"

try:
    tn = telnetlib.Telnet(HOST,PORT)
except Exception as ex:
    print ex
    print "cannot connect to controller... give up"
    sys.exit()

tn.write( "\n\r")
tn.write( "\n\r")

print "Inner HCAL"

prefix = "$GS0"
#2016a
#vi = [-60,-40,-30,-20,0,10,20,30,100,120,140,160,240,720,640,650]
#2017a
vi = [-58,-20,-6,40,-41,3,10,19,32,66,88,107,114,47,158,76]

i = 0
for v in vi:
    s = '%s%02d%d\n\r' % (prefix,i,v)
    print s
    tn.write(s)
    print "reading..."
    g = tn.read_until(">")
    print g
    i+=1 

print "Outer HCAL"

prefix = "$GS1"
#vo = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#2017a
vo = [187,166,99,137,90,82,129,198,81,-180,178,225,57,124,214,148]

i = 0
for v in vo:
    s = '%s%02d%d\n\r' % (prefix,i,v)
    print s
    tn.write(s)
    print "reading..."
    g = tn.read_until(">")
    print g
    i+=1 

tn.write( "\n\r")

print "Loaded default voltage offsets for Inner and Outer HCAL for T1044-2017a"
