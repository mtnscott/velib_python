#!/usr/bin/env python
# -*- coding: utf-8 -*-

# takes data from the dbus, does calculations with it, and puts it back on
from dbus.mainloop.glib import DBusGMainLoop
import gobject
from gobject import idle_add
import dbus
import dbus.service
import inspect
import platform
import pprint

# our own packages
from vedbus import VeDbusItemExport

softwareVersion = '1.0'

# Dictionary containing all objects exported to dbus
dbusObjects = {}

def handleDbusNameOwnerChanged(name, oldOwner, newOwner):
		#print('handlerNameOwnerChanged name=%s oldOwner=%s newOwner=%s' % (name, oldOwner, newOwner))
		#decouple, and process in main loop
		#idle_add(processNameOwnerChanged, name, oldOwner, newOwner)
		pass

def processNameOwnerChanged(name, oldOwner, newOwner):
		#print 'processingNameOwnerChanged'
		pass

def addDbusOject(dictionary, dbusConn, path, value, isValid = True, description = '', callback = None):
		dbusObjects[path] = VeDbusItemExport(dbusConn, path, value, isValid, description, callback)

def main(argv):
		global dbusObjects

		print __file__ + " starting up"

		# Have a mainloop, so we can send/receive asynchronous calls to and from dbus
		DBusGMainLoop(set_as_default=True)

		# For a PC, connect to the SessionBus
		# For a CCGX, connect to the SystemBus
		# Todo: do this automatically?
		dbusConn = dbus.SessionBus()

		# Register ourserves on the dbus, fake that we are a Quattro
		name = dbus.service.BusName("com.victronenergy.dbusexample", dbusConn)

		# subscribe to NameOwnerChange for bus connect / disconnect events.
		dbusConn.add_signal_receiver(handleDbusNameOwnerChanged, signal_name='NameOwnerChanged')

		# Create the management objects, as specified in the ccgx dbus-api document
		addDbusOject(dbusObjects, dbusConn, '/String', 'this is a string')
		addDbusOject(dbusObjects, dbusConn, '/Int', 0)
		addDbusOject(dbusObjects, dbusConn, '/NegativeInt', -10)
		addDbusOject(dbusObjects, dbusConn, '/Float', 1.5)

		# Start and run the mainloop
		print 'To see the list of objects that I export, run dbus com.victronenergy.dbusexample'
		print 'And to see a value, run following examples:'
		print 'dbus com.victronenergy.dbusexample /string GetValue'
		print 'dbus com.victronenergy.dbusexample /string GetText'
		print ''
		print 'Connected to dbus, and switching over to gobject.MainLoop() (= event based)'

		mainloop = gobject.MainLoop()
		mainloop.run()

main("")




