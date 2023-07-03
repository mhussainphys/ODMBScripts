import serial
import time
import numpy as np

#Power cycle test settings
PowerCycleInterval = 5
MeasureInterval = 2
NumTest = 3
SetVoltage = 3.3
CurrentLimit = 0.05

#Serial communication parameters and intialization
ser = serial.Serial()
ser.port = '/dev/ttyUSB0'
ser.baudrate = 9600
ser.stopbits = 2
ser.open()

#Reading run number
BaseFileDirectory = '/homes/mhussain/ODMBScripts/PCTest/'
PCTRunNumberFile = BaseFileDirectory + 'PCTRunNum.txt' #Power cycle test serial number 
PCTRunNumberHandle = open(PCTRunNumberFile, "r")
PCTRunNumber = int(PCTRunNumberHandle.read().strip())
PCTRunNumberHandle.close()

#Creating and writing data file for the run number
DataFileHandle  = open(BaseFileDirectory + 'PCTestData/PCTestData_Run_' + str(PCTRunNumber) + '.txt', 'w')
DataFileHandle.write('PowerCycleInterval: %.2f \nMeasureInterval: %.2f \nNumber of tests: %d \nSetVoltage: %.3f \nCurrentLimit: %.3f \n' % (PowerCycleInterval, MeasureInterval, NumTest, SetVoltage, CurrentLimit))

#Initializing power supply
ser.write(b'*IDN?\n')
print('#################################################################')
print('\nPower supply model: %s' % ser.readline().decode())
print('#################################################################')
ser.write(b'SYST:REM\n')
ser.write(b'SOUR:VOLT %0.4f\n' % SetVoltage) 
ser.write(b'CURR:PROT %0.4f\n' % CurrentLimit)


iter = 0

print('\n############ Starting run number %d #################' % PCTRunNumber)

Timestamp = time.time()
while iter < NumTest:

	print('\n############### Starting power cycling test %d #################' % (iter + 1)) 
	start_time = time.time()
	ser.write(b'OUTP:STAT ON\n')  

	while True:
		
		time.sleep(MeasureInterval)
		TimeElapsed = time.time() - start_time
		print('Time elapsed: %.3f s' % TimeElapsed)
		if TimeElapsed < PowerCycleInterval:
			ser.write(b'MEAS:VOLT?\n')
			MeasVolt = float(ser.readline().decode())
			print('Measured voltage is %.3f V' % MeasVolt)
			ser.write(b'MEAS:CURR?\n')
			MeasCurr = float(ser.readline().decode())
			print('Measured current is %.3f A' % MeasCurr)
			DataFileHandle.write('%.3f\t%.3f\t%.3f\n' % (time.time(), MeasVolt, MeasCurr))
		else:
			break

	ser.write(b'OUTP:STAT OFF\n')
	iter += 1

ser.close()
DataFileHandle.close()

PCTRunNumberHandle = open(PCTRunNumberFile, "w")
PCTRunNumberHandle.write(str(PCTRunNumber + 1))
PCTRunNumberHandle.close()

print('\n############ Run number %d  completed #################' % PCTRunNumber)







