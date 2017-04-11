#!/home/phnxrc/anaconda2/bin/python

import sys
import telnetlib
import sqlite3
import datetime
import time

# Turn on or off LED's in Inner and Outer HCAL, mask all on or off

# John Haggerty, BNL, 2016.03.18

HOST = "192.168.100.120"
PORT = "9760"

try:
    tn = telnetlib.Telnet(HOST,PORT)
except Exception as ex:
    print ex
    print "cannot connect to controller... give up"
    sys.exit()

if len(sys.argv) == 1:
    print "usage: hcalled.py [0|1|2|3|4]"
    sys.exit(0)

led = sys.argv[1]
if int(led) < 0 or int(led) > 4:
    print "usage: hcalled.py [0|1|2|3|4]"
    sys.exit(0)

tn.write( "\n\r")
tn.write( "\n\r")

dac = 1700

controllers = 2
for i in range(controllers): 
    setdac = "$LS"+str(i)+str(led)+str(dac)
    print "DAC: "+setdac
#    tn.write("$LS002000\n\r")
    tn.write(setdac+"\n\r")
    z = tn.read_until(">").split()
tn.write( "\n\r")

mask = [ "0100", "0200", "0400","0800", "1000"]

for i in range(controllers): 
    p = "$P"+str(i)+mask[int(led)]
    print "Mask: "+p
    tn.write(p+"\n\r")
    g = tn.read_until(">")
#    print g
tn.write( "\n\r")

