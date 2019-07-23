#!/usr/bin/env python
#Python 2.7
#Data Aquisition from a AcuDC 240 Power and Energy Meter

import os
import serial
import time
import datetime
import numpy as np
import minimalmodbus
import csv

minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL = True
minimalmodbus.HANDLE_LOCAL_ECHO = False

labels = 'datetime, voltage, current, power, totalEnergy'
filename = 'acuDC.csv'

def init_modbus(usb, addr):
	""" Function for the Modubus RTU driver via serial port.\n
		Args: USB name (For Windows: COM8, Linux: ttyUSB0),\n
		    add Instument adress (1-247)
	"""
	instr = minimalmodbus.Instrument(usb, addr, mode = 'rtu')
	instr.serial.baudrate = 9600
	instr.serial.bytesize = 8
	instr.serial.stopbits = 1
	instr.serial.parity = serial.PARITY_NONE
	instr.serial.timeout  = 0.2
	instr.debug = False
	return instr

def file_creation():
    """ Checks if the file to save the data exists or not. If not,
    it will be created """
    if not os.path.exists('/home/pi/Documents/AcuDC/%s'%filename):
        file = open('/home/pi/Documents/AcuDC/%s'%filename, 'w')
        file.write(labels + '\n')
        file.close()

def get_data(addr):
	try:
		instr = init_modbus('/dev/ttyUSB0', addr)
		voltage = instr.read_float(512, 3, 2)
		current = instr.read_float(514, 3, 2)
		power = instr.read_float(516, 3, 2)
		totalEnergy = instr.read_long(772, 3, False)  #Unsigned Integer variable
	except:
		pass

	if current == 0 or power == 0:
		voltage = 0
		current = 0
		power = 0
	return(voltage, current, power, totalEnergy)

def data_average(dt, average, energy):
	average = average / 10
	average = np.around(average, decimals = 2)
	average = np.hstack([dt, average, energy])
	average = ",".join(average)
	return average

starttime = time.time()
file_creation()

with open('/home/pi/Documents/AcuDC/acuDC.csv','a', buffering = 0) as f:
	while True:
		average = np.hstack([0])
		for i in range(10):
			#Data from acuDC
			data = get_data(1)   #data type: tuple
			dt = datetime.datetime.now()
			dt = dt.strftime('%Y-%m-%d %H:%M:%S')
			#stacked numpy array
			data1 = np.hstack([data[0], data[1], data[2]])
			average = average + data1
			stoptime = time.time()
			sleeptime = 6 - (stoptime-starttime) - 0.00556 -0.000042408
			if sleeptime > 0:
				time.sleep(sleeptime)
			starttime = time.time()
		#Average data & string type
		average1 = data_average(dt, average, data[3])
		f.write(average1 + '\n')
		#print(average1, type(average1))

