#!/home/phnxrc/anaconda2/bin/python

# Clock Master LV Control

# John Haggerty, BNL, 2016.03.17

import sys
import telnetlib
import time

terminal_server = 'serial2'
ser1_port = 3
ser1 = telnetlib.Telnet(terminal_server,4000+ser1_port)
 
ser1.write('#01S11301\r')
time.sleep(0.05)
line = ser1.read_until('>')
print line
print ("Clockmaster 4V OFF")

ser1.write('#01S11401\r')
time.sleep(0.05)
line = ser1.read_until('>')
print line
print ("Clockmaster 3.3V OFF")
time.sleep(1.0)

# turn back on

ser1.write('#01S11400\r')
time.sleep(0.05)
line = ser1.read_until('>')
print line
print ("Clockmaster 3.3V ON\n")

ser1.write('#01S11300\r')
time.sleep(0.05)
line = ser1.read_until('>')
print line
print ("Clockmaster 4V ON\n")
            
