import serial
import time
import numpy as np
import pyvisa as visa
#import argparse
import mysql
import mysql.connector
import datetime
import sys

#### Argument parser #####
#parser = argparse.ArgumentParser()
#parser.add_argument('id', type = str,
#                    help='Board ID needed for the database')
#args = parser.parse_args()

board_id = 2
rm = visa.ResourceManager('/lib64/libiovisa.so')
MeasureInterval = 10

### Format for dictionary is -- {key is address of the resource : list of values[type of commmunication, name of the power supply, voltages]}							   
PowerSupplyDict = {
				   'USB0::0x2A8D::0x3302::MY59001082::0::INSTR' : ['visa', 'Keysight Technologies,E36233A,MY59001082,1.0.0-1.0.2-1.00\n', 2],
				   'USB0::0x2A8D::0x3302::MY59002179::0::INSTR' : ['visa', 'Keysight Technologies,E36233A,MY59002179,1.0.0-1.0.2-1.00\n', 3], 
				   '/dev/ttyUSB2'								: ['serial', 'HEWLETT-PACKARD,E3633A,0,1.7-5.0-1.0\r\n', 4],
				   '/dev/ttyUSB0'								: ['serial', 'HEWLETT-PACKARD,E3633A,0,1.7-5.0-1.0\r\n', 5]
				   }

def pscom_start_fail():

	print('Unable to establish connections, things to check:\n \
		Script should be running on WIMP machine\n \
		Check if the power supplies are ON\n \
		Check if both the serial ports (key in the dictionary) still exists (do ls /dev/*USB*), change the dictionary key if the serial port is changed\n \
		Communication protocol is set to RS232 in power supplies\n \
 		Resource addresses are correct in the dictionary defined in the script')

def pscom_idn_fail():

	print('The mapping of power supply addresses and names in the dictionary dont match, things to check:\n \
		Check if the power supplies are ON\n \
		Check if the power supplies addresses have changed \n \
 		Resource addresses are correct in the dictionary defined in the script')

### Open all the visa or serial resources for the power supplies

def pscom_start():
	
	print("Opening all resources (establish connection with the power supplies)")

	all_ps_init = True
	for key in PowerSupplyDict:		
		try:
			if PowerSupplyDict.get(key)[0] == 'visa':
				resource = rm.open_resource(key)
			elif PowerSupplyDict.get(key)[0] == 'serial':
				resource = serial.Serial(timeout=3)
				resource.port = key
				resource.baudrate = 9600
				resource.stopbits = 2
				resource.open()
		except: 
			all_ps_init = False
			break
		PowerSupplyDict.get(key).append(resource)

	return all_ps_init


### Identify all power supplies and check if they match the values given in dictionary

def pscom_idn():

	print("Checking the mapping of power supply names with their addresses")

	all_ps_idn = True
	for key in PowerSupplyDict:		
		resource = PowerSupplyDict.get(key)[3]
		try:
			if PowerSupplyDict.get(key)[0] == 'visa':
				resource.write('*IDN?')
				if resource.read() != PowerSupplyDict.get(key)[1]: 
					all_ps_idn = False
			elif PowerSupplyDict.get(key)[0] == 'serial':
				resource.write(b'*IDN?\n')
				if resource.readline().decode() != PowerSupplyDict.get(key)[1]: 
					all_ps_idn = False
		except: 
			all_ps_idn = False
			break

	return all_ps_idn	

### Monitors currents and voltages

def pscom_mon():

	ps_mon = True
	MeasVoltList = []
	MeasCurrList = []
	for key in PowerSupplyDict:		
		resource = PowerSupplyDict.get(key)[3]
		try:
			if PowerSupplyDict.get(key)[0] == 'visa':
				PowerSupplyDict.get(key)[3].write('MEAS:VOLT? (@1)')
				MeasVoltList.append('%.3f' % float(resource.read()))
				resource.write('MEAS:CURR? (@1)')
				MeasCurrList.append('%.3f' % float(resource.read()))			
			elif PowerSupplyDict.get(key)[0] == 'serial':
				resource.write(b'MEAS:VOLT?\n')
				MeasVoltList.append('%.3f' % float(resource.readline().decode()))
				resource.write(b'MEAS:CURR?\n')
				MeasCurrList.append('%.3f' % float(resource.readline().decode()))
		except: 
			ps_mon = False
			break

	return ps_mon, MeasVoltList, MeasCurrList	


### Connect to sql server

def sql_database():

	database = mysql.connector.connect(
	  host ="localhost",
	  user ="mhussain",
	  passwd="password",
	  database = "power_supply_mon"
	)
	cursor = database.cursor()

	return database, cursor


### Add database entries

def update_database(board_id, MeasVoltList, MeasCurrList, database, cursor):

	local_time_now = datetime.datetime.now()

	sql = "INSERT INTO power_supply_data (timestamp_loc, board_id, dcfeb_e36233a_1_volt, dcfeb_e36233a_1_curr, dcfeb_e36233a_2_volt, dcfeb_e36233a_2_curr,\
	 		vme_e3633a_1_volt, vme_e3633a_1_curr, vme_e3633a_2_volt, vme_e3633a_2_curr)\
	 		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	val = (local_time_now.strftime('%Y-%m-%d %H:%M:%S'), board_id, str(MeasVoltList[0]), str(MeasCurrList[0]),\
	 		str(MeasVoltList[1]), str(MeasCurrList[1]), str(MeasVoltList[2]), str(MeasCurrList[2]), str(MeasVoltList[3]), str(MeasCurrList[3]))
	cursor.execute(sql, val)
	database.commit()


def exit_program():
    print("Exiting the program...")
    sys.exit(0)


def main(board_id, MeasureInterval):

	MeasureInterval = MeasureInterval - 3 ## 2-3 seconds it takes between the measurements without any sleep  

	if pscom_start() is False: 
		pscom_start_fail()
		exit_program()

	if pscom_idn() is False:
		pscom_idn_fail()
		exit_program()

	try:
		database, cursor = sql_database()
	except:
		print("Unable to connect to database")
		exit_program()

	while True:
			
		ps_mon, MeasVoltList, MeasCurrList = pscom_mon()
		if ps_mon:
			try:
				update_database(board_id, MeasVoltList, MeasCurrList, database, cursor)
			except:
				print("Unable to update database")
				break
		else:
			print("Monitoring power supplies failed. Or One of the power supplies turned off.")
			break

		time.sleep(MeasureInterval)



if __name__ == '__main__':
	main(board_id, MeasureInterval)




