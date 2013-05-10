#!/usr/bin/python

# need to import sys, os, and time to get some typical features
import sys, os, time

# we'll also import the datetime class from the datetime library
from datetime import datetime

# need to import the matplotlib, and set it as a TkAgg update type
import matplotlib
matplotlib.use('TkAgg')

# need to import some functions from the numpy library
from numpy import arange, sin, pi

# we'll also import an array variable also
import numpy.numarray as na

# need to set up some matplotlib figure imports
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

# since we are using the TkAgg type, we can import everything from the Tkinter library
from Tkinter import *

# import glob so that we can get a list of files in a directory
import glob

# import TkInter again, but this time as a variable...needs cleanup
import Tkinter as tk

# this is a callback function to update the plot or whatever
def update_clock():
    global root, t, a, f, canvas
    now = datetime.now()
    s_now = time.strftime("%Y-%m-%d %H:%M:%S")
    print "Updated at: " + s_now 

    # initialize lists
    labels=[]
    data=[]
         
    # look for all files
    files=glob.glob('../TestDumpingGround/*.dbd')
    for file in files:
        then = datetime.fromtimestamp(os.path.getmtime(file))
        td = (now - then)
        secSinceModTime = td.days*86400+td.seconds 
        # only update if file is less than 90000 seconds old
        if secSinceModTime <= 90000:
            rVal=float(open(file).readline())
            labels.append(file.split(".")[0])
            data.append(rVal) 

    # plot!
    a.clear()

    # get an array for the entire length of data
    xlocs = na.array(range(len(data))) 
    
    # set the width to a full 1.0 length?
    width = 1.0
    
    # set up the plot a bit
    a.set_title("Updated at: " + s_now)
    a.set_xticks(xlocs+width/2)
    a.set_xticklabels(labels)
    a.set_ylabel("Memory Usage [MiB]")
    
    # actually create a bar chart
    a.bar(range(len(data)), data, width=width)
    
    # and finally re-draw it
    canvas.draw()
    
    # call this to initiate another update in 1000ms
    root.after(1000, update_clock)

# create a Tk window instance
root = tk.Tk()
root.title("Lab 303 Dashboard")
root.geometry("700x500")

# create a matplotlib Figure -- note capital F
f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)

# create a dataplot canvas, show it, and pack it in the window
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

# setup the time range to plot
t = arange(0.0,3.0,0.01)

# call the callback once to get the party started...it will continue to call 'after' on itself
update_clock()

# run the main message loop and go!
root.mainloop()
