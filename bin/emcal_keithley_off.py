#!/home/phnxrc/anaconda2/bin/python

import time
import telnetlib

terminal_server = 'serial1'
serk1_port = 2
serk1 = telnetlib.Telnet(terminal_server,4000+serk1_port)
   
serk1.write('*idn?\r')
time.sleep(0.05)
line = serk1.read_until('\r')
print line

serk1.write(':outp off\r')
time.sleep(0.05)
# on or off does not respond with anything....

serk1.write(':outp:stat?\r')
time.sleep(0.01)
line = serk1.read_until('\r')
print line
                            


                            
