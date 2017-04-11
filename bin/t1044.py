#!/home/phnxrc/anaconda2/bin/python

# This is a little menu to run shell commands from a gui

# John Haggerty, BNL
# Originally appearing in phenix now for t1044
# 2016.03.20

from Tkinter import *
import os
import sys

# list of button names and their associated shell commands

emcalcommands = [
    ["EMCAL Keithley ON","~/calcon/bin/emcal_keithley_start.py &"],
    ["EMCAL Keithley OFF","~/calcon/bin/emcal_keithley_off.py &"],
    ["EMCAL Read Keithley","~/calcon/bin/keithleyfastread.py 2 &"],
    ["EMCAL Default Bias (2.3E5)","~/calcon/bin/emcalbias.py &"],
    ["EMCAL Bias for 1.15E5","~/calcon/bin/emcalhalf.py &"],
    ["EMCAL LED ON","~/calcon/bin/emcalled.py on &"],
    ["EMCAL LED OFF","~/calcon/bin/emcalled.py off &"],
    ["EMCAL TP ON","~/calcon/bin/emcaltp.py on &"],
    ["EMCAL TP OFF","~/calcon/bin/emcaltp.py off &"],
    ["EMCAL gain stabilizer ON","~/calcon/bin/emcalstabilizer.py on &"],
    ["EMCAL gain stabilizer OFF","~/calcon/bin/emcalstabilizer.py off &"],
    ["EMCAL high gain","~/calcon/bin/emcalgain.py high &"],
    ["EMCAL normal gain","~/calcon/bin/emcalgain.py normal &"]
     ]

emcal3commands = [
    ["EMCAL3 Keithley ON","~/calcon/bin/emcal3_keithley_start.py &"],
    ["EMCAL3 Keithley OFF","~/calcon/bin/emcal_keithley_off.py &"],
    ["EMCAL3 Read Keithley","~/calcon/bin/keithleyfastread.py 2 &"],
    ["EMCAL3 Default Bias (2.3E5)","~/calcon/bin/emcal3bias.py &"],
    ["EMCAL3 Bias for 1.15E5","~/calcon/bin/emcal3half.py &"],
    ["EMCAL3 LED ON","~/calcon/bin/emcal3led.py on &"],
    ["EMCAL3 LED OFF","~/calcon/bin/emcal3led.py off &"],
    ["EMCAL3 TP ON","~/calcon/bin/emcal3tp.py on &"],
    ["EMCAL3 TP OFF","~/calcon/bin/emcal3tp.py off &"],
    ["EMCAL3 gain stabilizer ON","~/calcon/bin/emcal3stabilizer.py on &"],
    ["EMCAL3 gain stabilizer OFF","~/calcon/bin/emcal3stabilizer.py off &"],
    ["EMCAL3 high gain","~/calcon/bin/emcal3gain.py high &"],
    ["EMCAL3 normal gain","~/calcon/bin/emcal3gain.py normal &"],
    ["EMCAL3 temperature","~/calcon/bin/emcaltemp.py 1 1&"]
     ]

hcalcommands = [
    ["HCAL Keithley ON","~/calcon/bin/hcal_keithley_start.py &"],
    ["HCAL Keithley OFF","~/calcon/bin/hcal_keithley_off.py &"],
    ["HCAL Read Keithley","~/calcon/bin/keithleyfastread.py 1 &"],
    ["HCAL Default Bias (2.3E5)","~/calcon/bin/hcalbias.py &"],
    ["HCAL Bias for 1.15E5","~/calcon/bin/hcalhalf.py &"],
    ["HCAL LED ON","~/calcon/bin/hcalled.py on &"],
    ["HCAL LED OFF","~/calcon/bin/hcalled.py off &"],
    ["HCAL TP ON","~/calcon/bin/hcaltp.py on &"],
    ["HCAL TP OFF","~/calcon/bin/hcaltp.py off &"],
    ["HCAL gain stabilizer ON","~/calcon/bin/hcalstabilizer.py on &"],
    ["HCAL gain stabilizer OFF","~/calcon/bin/hcalstabilizer.py off &"],
    ["HCAL temperatures","~/calcon/bin/hcaltemp.py 1 &"],
    ["Possibly reboot DCM","rsh iocondev1e reboot &"],
    ["Toggle CM power", "python ~/calcon/bin/cmtoggle.py &"]
     ]

class App:

    def __init__(self, master):
        
        frame = Frame(master)
        frame.pack()
        
        homedir = os.getenv('HOME','/')
        logo_image = homedir + "/calcon/sPHENIX.gif"
        print logo_image
        
        try:
            f = open( logo_image )
            f.close()
            logo = PhotoImage(file=logo_image)
            self.lbl = Label( frame, image=logo, text="sPHENIX"  ) 
            self.lbl.logo = logo
        except IOError:
            print 'error opening ',logo_image,', ignoring'
            self.lbl = Label( frame, text="sPHENIX"  )
            
        self.lbl.configure(background='white')
        self.lbl.pack(side=TOP,fill=X)

        button_frame = Frame(frame)
        exit_frame = Frame(frame)

        button_frame.pack(side=TOP,fill=X)
        exit_frame.pack(side=TOP,fill=X)

        left_frame = Frame(button_frame)
        middle_frame = Frame(button_frame)
        right_frame = Frame(button_frame)

        left_frame.pack(side=LEFT,fill=BOTH)
        middle_frame.pack(side=LEFT,fill=BOTH)
        right_frame.pack(side=RIGHT,fill=BOTH)

        for c in emcalcommands:
          self.sh = Button( left_frame, text=c[0],
                            command=lambda arg1=c[1]: self.shell(arg1),
                            anchor=W ) 
          self.sh.pack(side=TOP,fill=X)

        for c in emcal3commands:
          self.sh = Button( middle_frame, text=c[0],
                            command=lambda arg1=c[1]: self.shell(arg1),
                            anchor=W ) 
          self.sh.pack(side=TOP,fill=X)

        for c in hcalcommands:
          self.sh = Button( right_frame, text=c[0],
                            command=lambda arg1=c[1]: self.shell(arg1),
                            anchor=W ) 
          self.sh.pack(side=TOP,fill=X)

        self.quit = Button(exit_frame, text="Exit", command=frame.quit, anchor=CENTER)
        self.quit.pack(side=TOP,fill=X)
        
# this executes the shell command "x" and prints the result
    def shell(self,x):
        result = os.system( x )
            
# down here is the main program

root = Tk()
root.title("T1044-2017a")            
app = App(root)
            
root.mainloop()
