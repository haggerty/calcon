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
    ["EMCAL Keithley ON","~/t1044-2016a/bin/emcal_keithley_start.py &"],
    ["EMCAL Keithley OFF","~/t1044-2016a/bin/emcal_keithley_off.py &"],
    ["EMCAL Read Keithley","~/t1044-2016a/bin/keithleyfastread.py 2 &"],
    ["EMCAL Default Gain","~/t1044-2016a/bin/emcalbias.py &"],
    ["EMCAL LED ON","~/t1044-2016a/bin/emcalled.py on &"],
    ["EMCAL LED OFF","~/t1044-2016a/bin/emcalled.py off &"],
    ["EMCAL TP ON","~/t1044-2016a/bin/emcaltp.py on &"],
    ["EMCAL TP OFF","~/t1044-2016a/bin/emcaltp.py off &"],
    ["EMCAL high gain","~/t1044-2016a/bin/emcalgain.py high &"],
    ["EMCAL normal gain","~/t1044-2016a/bin/emcalgain.py normal &"]
     ]

hcalcommands = [
    ["HCAL Keithley ON","~/t1044-2016a/bin/hcal_keithley_start.py &"],
    ["HCAL Keithley OFF","~/t1044-2016a/bin/hcal_keithley_off.py &"],
    ["HCAL Read Keithley","~/t1044-2016a/bin/keithleyfastread.py 1 &"],
    ["HCAL Default Gain","~/t1044-2016a/bin/hcalbias.py &"],
    ["HCAL LED ON","~/t1044-2016a/bin/hcalled.py on &"],
    ["HCAL LED OFF","~/t1044-2016a/bin/hcalled.py off &"],
    ["HCAL TP ON","~/t1044-2016a/bin/hcaltp.py on &"],
    ["HCAL TP OFF","~/t1044-2016a/bin/hcaltp.py off &"]
     ]

class App:

    def __init__(self, master):
        
        frame = Frame(master)
        frame.pack()
        
        homedir = os.getenv('HOME','/')
        logo_image = homedir + "/t1044-2016a/sPHENIX.gif"
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
        right_frame = Frame(button_frame)

        left_frame.pack(side=LEFT,fill=BOTH)
        right_frame.pack(side=RIGHT,fill=BOTH)

        for c in emcalcommands:
          self.sh = Button( left_frame, text=c[0],
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
            
app = App(root)
            
root.mainloop()
