import serial
import time
import numpy as np
#import matplotlib.pyplot as plt

#Power cycle test settings
PowerCycleInterval = 10
MeasureInterval = 2
NumTest = 3

#Serial communication parameters and intialization
ser = serial.Serial()
ser.port = '/dev/ttyUSB0'
ser.baudrate = 9600
ser.stopbits = 2
ser.open()

plt.axis([0, 10, 0, 10])    

ser.write(b'*IDN?\n')
print(ser.readline())
ser.write(b'SYST:REM\n')
ser.write(b'SOUR:VOLT 5\n')
#Set current limit

iter = 0

while iter < NumTest:

	print('Starting power cycling test ' + str(iter + 1)) 
	start_time = time.time()
	ser.write(b'OUTP:STAT ON\n')  

	while True:
		
		time.sleep(MeasureInterval)
		TimeElapsed = time.time() - start_time
		print('Time elapsed: ' + str(TimeElapsed))
		if TimeElapsed < PowerCycleInterval:
			ser.write(b'MEAS:VOLT?\n')
			type(ser.readline())
			plt.scatter(TimeElapsed, )
			
			ser.write(b'MEAS:CURR?\n')
			print(ser.readline())
			plt.pause(0.00001)
		else:
			break

	ser.write(b'OUTP:STAT OFF\n')
	iter += 1

ser.close()
