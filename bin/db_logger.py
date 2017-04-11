import logging
import sqlite3
import datetime
import telnetlib
import time
import sys
import os
import socket
import pandas as pd

class SQLiteHandler():
   init_sql_hcal = """CREATE TABLE IF NOT EXISTS HCAL(
		 	   CREATED TEXT,
			   UTIME REAL,
			   RUNNUMBER INT,
			   DETID INT,
		  	   T0 REAL,
	           	   T1 REAL,
		 	   D0 INT,
		  	   D1 INT,
		  	   I0 REAL,
		  	   I1 REAL,
			   GR0 REAL,
			   GR1 REAL
			)"""


   init_sql_emcal = """CREATE TABLE IF NOT EXISTS EMCAL(
                           CREATED TEXT,
                           UTIME REAL,
                           RUNNUMBER INT,
                           DETID INT,
                           T0 REAL,
                           T1 REAL,
                           D0 INT,
                           D1 INT,
                           I0 REAL,
                           I1 REAL,
                           GR0 REAL,
                           GR1 REAL
                        )"""

   init_sql_hcal_keithley = """CREATE TABLE IF NOT EXISTS HCAL_KEITHLEY(
                           CREATED TEXT,
                           UTIME REAL,
			   RUNNUMBER INT,
                           BIAS_VOLT REAL,
                           BIAS_CUR REAL
                        )"""

   init_sql_emcal_keithley = """CREATE TABLE IF NOT EXISTS EMCAL_KEITHLEY(
                           CREATED TEXT,
                           UTIME REAL,
			   RUNNUMBER INT,
                           BIAS_VOLT REAL,
                           BIAS_CUR REAL
                        )"""


   insert_hcal_sql = """INSERT INTO HCAL( CREATED, UTIME, RUNNUMBER, DETID, T0, T1, D0, D1, I0, I1, GR0, GR1) VALUES(  '%s', '%f', '%d', '%d', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f' );"""
   insert_emcal_sql = """INSERT INTO EMCAL( CREATED, UTIME, RUNNUMBER, DETID, T0, T1, D0, D1, I0, I1, GR0, GR1) VALUES(  '%s', '%f', '%d', '%d', '%f', '%f', '%f', '%f', '%f', '%f', '%f', '%f' );"""
   insert_hcal_keithley_sql = """INSERT INTO HCAL_KEITHLEY( CREATED, UTIME, RUNNUMBER, BIAS_VOLT, BIAS_CUR ) VALUES(  '%s', '%f', '%d', '%g', '%g' );"""
   insert_emcal_keithley_sql = """INSERT INTO EMCAL_KEITHLEY( CREATED, UTIME, RUNNUMBER, BIAS_VOLT, BIAS_CUR ) VALUES(  '%s', '%f', '%d', '%g', '%g' );"""
 
   #Initialization
   def __init__(self, db):
     self.db = db
     conn = sqlite3.connect(self.db)
     logging.info('Connected to database file %s',self.db)
     conn.execute(self.init_sql_hcal)
     conn.execute(self.init_sql_emcal)
     conn.execute(self.init_sql_hcal_keithley)
     conn.execute(self.init_sql_emcal_keithley)
     conn.commit()

   #Setting up a telnet connection
   def setup_telnet(self,host,port):
     self.host = host
     self.port = port
     try:
      tn = telnetlib.Telnet( host, port, 1 )
      logging.info('Telnet OK. host: %s port: %s', host, port)
      return tn
     except socket.timeout:
      logging.info('Cant Telnet. host: %s port: %s', host, port) 
      return 0
    
   #Check keithley is ON or OFF  
   def check_if_keithley_on(self,keithley):
    try:
     keithley.write(':outp:stat?\r')
     line = keithley.read_until('\r')
     if int(line)==0:
      logging.info('Keithley is OFF. Exiting..')
    except Exception as ex:
     print ex
     logging.info('Cant read Keithley')
     line = 0
    if int(line)==1: keithley.write(':SYST:KEY 23\r') #Put back to local
    return int(line)

   #Read calo
   def read_calo(self, calo, len, cmd=''):
     if calo==0: sys.exit()
     logging.info('Reading %d values from %s',len,cmd)
     data = pd.DataFrame()
     if calo!=0:
       data['T0'] = handler.read( calo, "$T0" )[:len]
       data['T1'] = handler.read( calo, "$T1" )[:len]
       data['D0'] = handler.read( calo, "$D0" )[:len]
       data['D1'] = handler.read( calo, "$D1" )[:len]
       data['I0'] = handler.read( calo, "$I0" )[:len]
       data['I1'] = handler.read( calo, "$I1" )[:len]
       data['GR0'] = handler.read( calo, "$GR0" )[:len]
       data['GR1'] = handler.read( calo, "$GR1" )[:len]
     else:
       pass
     #print(data)
     return data

   #Read controller values
   def read(self, instrument, cmd=''):
     if instrument==0: sys.exit()
     logging.info( 'Reading.. %s', cmd )
     cmd = cmd + "\n\r"
     instrument.write(cmd)
     try:
       r = instrument.read_until(">").split("\r")
     except Exception as ex:
       logging.info('Cant read cmd %s', cmd)   
       r = 0
     #print r
     val = []
     for value in r:
      try:
        val.append( float(value) )
      except ValueError:
        pass
     return val

   #Get Runnumber
   def get_runnumber(self):
    run = os.popen("rcdaq_client daq_status -s | awk \'{print $1}\'").read()
    #logging.info('Runnumber %s', run)
    try:
       runnumber = int(run)
    except ValueError:
       runnumber = -1
    return runnumber

   #Get datetime as string
   def get_datetime(self):
    return str(datetime.datetime.now())

   #Get unix time
   def get_utime(self):
    return time.time()

   #Get keithley Volt, Cur
   def read_keithley(self, keithley):
     on = self.check_if_keithley_on(keithley)
     self.kv = 0
     self.ki = 0
     if on==1:
      keithley.write(':FORM:ELEM VOLT,CURR\r')
      keithley.write(':READ?\r')
      line = keithley.read_until('\r')
      #print line
      readback = str(line).split(',')
      v = float( readback[0] )
      i = float( readback[1] )
      #print "voltage %2.2f, current %2.12f" % (v,i)
      self.kv = v
      self.ki = i
      keithley.write(':SYST:KEY 23\r') #Put back to local
     return on

   #Dump to file 
   def dump(self, data, calo=''):
     fT0=open('./DB_LOGGER_'+calo+'_T0.txt', 'w+')
     fT1=open('./DB_LOGGER_'+calo+'_T1.txt', 'w+')
     fT0_val=open('./DB_LOGGER_'+calo+'_T0_values.txt', 'w+')
     fT1_val=open('./DB_LOGGER_'+calo+'_T1_values.txt', 'w+')
     fD0=open('./DB_LOGGER_'+calo+'_D0.txt', 'w+')
     fD1=open('./DB_LOGGER_'+calo+'_D1.txt', 'w+')
     fI0=open('./DB_LOGGER_'+calo+'_I0.txt', 'w+')
     fI1=open('./DB_LOGGER_'+calo+'_I1.txt', 'w+')
     fI0_val=open('./DB_LOGGER_'+calo+'_I0_values.txt', 'w+')
     fI1_val=open('./DB_LOGGER_'+calo+'_I1_values.txt', 'w+')
     fGR0=open('./DB_LOGGER_'+calo+'_GR0.txt', 'w+')
     fGR1=open('./DB_LOGGER_'+calo+'_GR1.txt', 'w+')
     multiplier=1000
     for detid in range(0,len(data)):
       print >> fT0, '{0:.2f}'.format(data.T0[detid])
       print >> fT1, '{0:.2f}'.format(data.T1[detid])
       print >> fT0_val, '{0:.0f}'.format(multiplier*data.T0[detid])
       print >> fT1_val, '{0:.0f}'.format(multiplier*data.T1[detid])
       print >> fD0, '{0:.2f}'.format(data.D0[detid])
       print >> fD1, '{0:.2f}'.format(data.D1[detid])
       print >> fI0, '{0:.2f}'.format(data.I0[detid])
       print >> fI1, '{0:.2f}'.format(data.I1[detid])
       print >> fI0_val, '{0:.0f}'.format(multiplier*data.I0[detid])
       print >> fI1_val, '{0:.0f}'.format(multiplier*data.I1[detid])
       print >> fGR0, '{0:.2f}'.format(data.GR0[detid])
       print >> fGR1, '{0:.2f}'.format(data.GR1[detid])

   #DB comit
   def db_commit(self, data,calo=''):
    created = self.get_datetime()
    utime = self.get_utime()
    run = self.get_runnumber()
    conn = sqlite3.connect(self.db)
    if calo=='HCAL':
     cmd = self.insert_hcal_sql
    elif calo=='EMCAL':
     cmd = self.insert_emcal_sql
    else: 
      print('Not sure which db to commit')
      sys.exit()
    for detid in range(0,len(data)):
      sql = cmd % (created, utime, run, detid, data.T0[detid], data.T1[detid], data.D0[detid], data.D1[detid], data.I0[detid], data.I1[detid], data.GR0[detid], data.GR1[detid] )
      #print sql 
      conn.execute(sql)
    logging.info('Committed to database..')
    conn.commit()

   def dump_keithley(self, filename):
     #print self.kv, self.ki
     f=open(filename + "_VOLTAGE.txt", 'w+')
     print >> f, '{0:.2f}'.format(self.kv)
     
     multiplier=1000
     f=open(filename + "_VOLTAGE_values.txt", 'w+')
     print >> f, '{0:.0f}'.format(multiplier*self.kv)  
  
     f=open(filename + "_CURRENT.txt", 'w+')
     print >> f, '{0:.10f}'.format(self.ki)

     multiplier=1000000000
     f=open(filename + "_CURRENT_values.txt", 'w+')
     print >> f, '{0:.0f}'.format(multiplier*self.ki)   



   #DB for keithley
   def db_keithley_commit(self, keithley, cmd):
    created = self.get_datetime()
    utime = self.get_utime()
    run = self.get_runnumber()
    conn = sqlite3.connect(self.db)
    on = self.read_keithley( keithley )
    if on==1:
     #print self.kv, self.ki
     sql = cmd % ( created, utime, run, self.kv, self.ki )
     conn.execute(sql)
     conn.commit()
    

if __name__ == '__main__':
  logfile = "/data/data/phnxsa/testbeam.log"
  dbfile = "/data/data/phnxsa/testbeam.db"
  logging.basicConfig(filename=logfile,level=logging.DEBUG,format='%(asctime)s %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
  handler = SQLiteHandler(dbfile)

  #HCAL keithley
  host = "serial1"
  port = "4001"
  keithley = handler.setup_telnet(host, port)  
  if keithley!=0: handler.db_keithley_commit( keithley, handler.insert_hcal_keithley_sql)
  if keithley!=0: handler.dump_keithley("DB_LOGGER_HCAL_KEITHLEY")

  #EMCAL keithley
  host = "serial1"
  port = "4002"
  keithley = handler.setup_telnet(host, port)
  if keithley!=0: handler.db_keithley_commit( keithley, handler.insert_emcal_keithley_sql)
  if keithley!=0: handler.dump_keithley("DB_LOGGER_EMCAL_KEITHLEY") 

  #check HCAL controller
  host = "192.168.100.120"
  port = "9760"
  hcal = handler.setup_telnet(host, port)
  if(hcal): hcal_read = handler.read_calo(hcal,24,"HCAL")
  handler.db_commit(hcal_read,'HCAL')
  handler.dump(hcal_read,'HCAL')
  #print('hcal_data:')
  #print(hcal_read)

  #check EMCAL controller
  host = "192.168.100.110"
  port = "9760"
  emcal = handler.setup_telnet(host, port)
  if(emcal): emcal_read = handler.read_calo(emcal,64,"EMCAL")
  handler.db_commit(emcal_read,'EMCAL')
  handler.dump(emcal_read,'EMCAL')
  #print('emcal_data:')
  #print(emcal_read)

 
