import serial
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('ggplot')
matplotlib.use( 'tkagg' )

#Power cycle test settings
SetVoltage = 0
CurrentLimit = 0.25
NumTest = 10
#Serial communication parameters and intialization
ser = serial.Serial()
ser.port = '/dev/ttyUSB0'
ser.baudrate = 9600
ser.stopbits = 2
ser.open()

#Initializing power supply
ser.write(b'*IDN?\n')
print('#################################################################')
print('\nPower supply model: %s' % ser.readline().decode())
print('#################################################################')
ser.write(b'SYST:REM\n')
ser.write(b'CURR:PROT %.4f\n' % CurrentLimit)


ser.write(b'SOUR:VOLT 0\n') 
ser.write(b'OUTP:STAT ON\n')

iter = 0

while iter < NumTest:
	SetVoltage = SetVoltage + 1  
	ser.write(b'SOUR:VOLT %.4f\n' % SetVoltage)
	time.sleep(2)
	ser.write(b'MEAS:VOLT?\n')
	MeasVolt = float(ser.readline().decode())
	print('Measured voltage is %.3f V' % MeasVolt)
	ser.write(b'MEAS:CURR?\n')
	MeasCurr = float(ser.readline().decode())
	print('Measured current is %.3f A' % MeasCurr)
	
	iter += 1

ser.write(b'OUTP:STAT OFF\n')
ser.close()





