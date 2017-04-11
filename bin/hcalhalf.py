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
# Gain = 2.3E5
#vi = [-60,-40,-30,-20,0,10,20,30,100,120,140,160,240,720,640,650]
# Gain = 1.15E5
vi = [-1037,-1026,-1008,-996,-986,-969,-957,-940,-879,-864,-845,-817,-741,-364,-340,-324]

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
# Gain = 2.3E5
#vo = [-242,-174,-100,-84,-72,66,88,678,692,702,712,720,726,730,730,740]
# Gain = 1.15E5
vo = [-1226,-1157,-1086,-1066,-1052,-916,-897,-305,-290,-277,-272,-263,-260,-253,-246,-235]

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

print "loaded bias values for *half* gain for Inner and Outer HCAL"
