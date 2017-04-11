#!/home/phnxrc/anaconda2/bin/python

import sys
import telnetlib
import sqlite3
import datetime
import time

# Read temperatures

# John Haggerty, BNL, 2017.01.19

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

if len(sys.argv) == 1:
    print "usage: hcaltemp.py #reads"
    sys.exit(0)

nreads = int(sys.argv[1])


for channel in range(0, 2):

    command = '$T'
    command += str(channel)
    print command
    tn.write(command)
#    tn.write("$T1")
    line = tn.read_until(">")
#    print line
    tn.write( "\n\r")

    sline = line.rstrip()
    line = sline.lstrip()
    line = line.replace('\r', '')
    tstr = str(line)
    readback = tstr.split('\n')
    
    readback.remove('>')
#    print readback

    temps = [float(i) for i in readback]
    twodecimals = ["%.2f" % v for v in temps]
#    print temps

    row_of_temp = '|  '
    for j, t in enumerate(twodecimals):
#            print("T {}: {}".format(j, t))
            row_of_temp += str(t)
            row_of_temp += ' | '
            if j%4 == 3:
                print row_of_temp
                row_of_temp = '|  '
            if j>16:
                break

    
