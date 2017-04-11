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

tn.write( "\n\r")
tn.write( "\n\r")

nleds = 5
dac = 2000
print "Setting DAC to "+str(dac)
for i in range(nleds):
    setdac = "$LS1"+str(i)+str(dac)
    print setdac
#    tn.write("$LS002000\n\r")
    tn.write(setdac+"\n\r")
    z = tn.read_until(">").split()
tn.write( "\n\r")

mask = ["04"]
for m in mask:
    p = "$P1"+m+"00"
    print "Mask: "+p
    tn.write(p+"\n\r")
    g = tn.read_until(">")
#    print g
    tn.write( "\n\r")
    time.sleep(1.0)

