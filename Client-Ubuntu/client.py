#!/usr/bin/env python

import subprocess, os
from gi.repository import GObject, Gtk, GLib, AppIndicator3 as appindicator
import socket

username = os.getlogin()
outputFile = "%s/../TestDumpingGround/%s.dbd" % (os.getcwd(), socket.gethostname())

def writeUserProcessMemoryUsage():
    process = subprocess.Popen("ps -u %s -o rss | awk '{sum+=$1} END {print sum}'" % username,
                                    shell=True,
                                    stdout=subprocess.PIPE,
                                    )
    stdout_list = process.communicate()[0].split('\n')
    f = open(outputFile, 'w')
    f.write(stdout_list[0])
    f.close()
    print stdout_list[0]
    return True
        
# build the app indicator
ind = appindicator.Indicator.new("303dashboardClient", "303dashboardClient", appindicator.IndicatorCategory.APPLICATION_STATUS)
ind.set_status (appindicator.IndicatorStatus.ACTIVE)
ind.set_icon("%s/../Resources/chart.png" % os.getcwd())

# create a menu
menu = Gtk.Menu()
menu_item = Gtk.MenuItem("Quit")
menu.append(menu_item)
menu_item.connect("activate", Gtk.main_quit)
menu_item.show()
ind.set_menu(menu)
menu.show()
       
# then continue to call the memory updater
GLib.timeout_add(1000, writeUserProcessMemoryUsage)

# run the message loop! (pump/process messages)
GObject.MainLoop().run()
