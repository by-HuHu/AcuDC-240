#!/usr/bin/env python
#Python 2.7
#Watchdog for Power and Energy file from AcuDC Power and Energy Meter

import os
import csv
import time
import datetime
import subprocess
import re

i = 1
minutes = [1, 60, 1440, 2880, 4320]

while True:
	try:
		t1 =time.time()
		dt = datetime.datetime.now()
		dt1= dt.strftime('%Y-%m-%d %H:%M')
		delta = datetime.timedelta(minutes = 1)
		dt2 = (dt - delta)
		dt2= dt2.strftime('%Y-%m-%d %H:%M')
		ls = [dt1, dt2]
		lastline = os.popen('tail -n 1 /home/pi/Documents/AcuDC/acuDC.csv').read()
		record = re.findall('(.* [0-9]*:[0-9]*)', lastline)[0]
		if record in ls:   
	    	#if lastline.startswith(dt):
			#msg = 'DAQ system is working properly ' + lastline
			alert = 0
			i = 1	
		else:
			#msg = 'No data since ' + record
			alert = i
			i = alert + 1
		tt = time.time() - t1
		#print('Process lasts ', tt)
		if alert in minutes:
			subprocess.call('echo "Production Energy DAQ system. The systems did not aquired data for the last minute. You may want to check what was the cause." | mail -s "DAQ Acu Vesterinen" hugo.huerta@turkuamk.fi hehuertam@gmail.com ', shell=True)
		time.sleep(60)
	except:
		pass

