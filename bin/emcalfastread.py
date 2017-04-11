#!/home/phnxrc/anaconda2/bin/python

import time
import datetime
import telnetlib
import sys

# Read emcal Keithley as fast as you can and report the results
# now with means and sigma

# John Haggerty, BNL 2016.03.05

K = 0
n = 0
Ex = 0
Ex2 = 0

def add_variable(x):
    global n,Ex,Ex2,K
    if (n == 0):
        K = x
    n = n + 1
    Ex += x - K
    Ex2 += (x - K) * (x - K)

def remove_variable(x):
    n = n - 1
    Ex -= (x - K)
    Ex2 -= (x - K) * (x - K)
    
def get_meanvalue():
    return K + Ex / n

def get_variance():
    return (Ex2 - (Ex*Ex)/n) / (n-1)

def main():
    print("starting...")

    terminal_server = 'serial1'
    serk1_port = 2
    serk1 = telnetlib.Telnet(terminal_server,4000+serk1_port)
    print("opening...")
    
    serk1.write(':outp:stat?\r')
    time.sleep(0.01)
    line = serk1.read_until('\r')
    print "output status: "+line

    if int(line)==0:
        print "Keithley is off... nothing to read"
        sys.exit(0)

    serk1.write(':FORM:ELEM VOLT,CURR\r')
    
    for xxx in range (0, 100):
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
        add_variable(1e6*i)
            
    mean_i = get_meanvalue()
    sigma_i = get_variance()

    print("mean current: "+str(mean_i)+" +/- "+str(sigma_i)+" uA from "+str(n)+" measurements")
            
main()

