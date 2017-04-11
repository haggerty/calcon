#!/home/phnxrc/anaconda2/bin/python

import sys
import time
import telnetlib
import datetime
# Note that in general, commands to do things do not respond in any way,
# but commands to query (?) do

terminal_server = 'serial1'
serk1_port = 2
serk1 = telnetlib.Telnet(terminal_server,4000+serk1_port)
   
serk1.write('*idn?\r')
time.sleep(0.05)
line = serk1.read_until('\r')
print line

print "on or off?"
serk1.write(':outp:stat?\r')
time.sleep(0.01)
line = serk1.read_until('\r')
print line

if int(line)==0:
 print "turning on the keithley.."
 serk1.write(':outp on\r')
 time.sleep(0.05)
else:
 print "Keithley is already ON"
 print "To reset new values, turn it OFF first"
 sys.exit()

print "setting compliance"
serk1.write(':SENS:CURR:PROT 1.25E-4\r')
time.sleep(0.05)
#does not respond

print "reading compliance"
serk1.write(':SENS:CURR:PROT?\r')
time.sleep(1.05)
line = serk1.read_until('\r')
print line

print "rear panel output"
serk1.write(':ROUT:TERM REAR\r')
time.sleep(0.05)
#does not respond

print "voltage source"
serk1.write(':SOUR:FUNC VOLT\r')
time.sleep(0.05)
#does not respond

print "set voltage range"
serk1.write(':SOUR:VOLT:RANG 210\r')
time.sleep(0.01)
#does not respond

print "voltage range?"
serk1.write(':SOUR:VOLT:RANG?\r')
time.sleep(0.01)
line = serk1.read_until('\r')
print line

print "setting nominal output voltage in steps.."
serk1.write(':SOUR:VOLT:LEV -20.0\r')
time.sleep(1.05)

serk1.write(':SOUR:VOLT?\r')
time.sleep(0.05)
line = serk1.read_until('\r')
print line

serk1.write(':SOUR:VOLT:LEV -40.0\r')
time.sleep(1.05)

serk1.write(':SOUR:VOLT?\r')
time.sleep(0.05)
line = serk1.read_until('\r')
print line

serk1.write(':SOUR:VOLT:LEV -50.0\r')
time.sleep(1.05)

serk1.write(':SOUR:VOLT?\r')
time.sleep(0.05)
line = serk1.read_until('\r')
print line

serk1.write(':SOUR:VOLT:LEV -67.0\r')
time.sleep(1.05)
#does not respond

serk1.write(':SOUR:VOLT?\r')
time.sleep(0.05)
line = serk1.read_until('\r')
print line

print "Final output voltage"
serk1.write(':SOUR:VOLT?\r')
time.sleep(0.05)
line = serk1.read_until('\r')
print line

print "on or off?"
serk1.write(':outp:stat?\r')
time.sleep(0.01)
line = serk1.read_until('\r')
print line

if int(line)==1:
 print "Reading few current values.."
 serk1.write(':FORM:ELEM VOLT,CURR\r')
 for x in range (0, 10):
    serk1.write(':READ?\r')
    time.sleep(0.05)
    line = serk1.read_until('\r')
#    print line
    sline = line.rstrip()
    line = sline.lstrip()
    linestr = str(line)
    readback = linestr.split(',')
    try:
        v = float(readback[0])
        i = float(readback[1])
    except ValueError:
        print('error: readback[0]: '+str(readback[0])+'\n')
        print('error: readback[1]: '+str(readback[1])+'\n')
        v = 100.0
        i = 100.0
    now = str(datetime.datetime.now())
    print(now+" voltage: "+str(v)+" current: "+str(i))
else:
  print "Keithley is OFF.. exiting."

#Put it to local
serk1.write(':SYST:KEY 23\r')
#Does not respond
