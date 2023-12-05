
'''

	for key in PowerSupplyDict:
	
		if PowerSupplyDict.get(key)[0] == 'visa':
			try:
				PowerSupplyDict.get(key)[3].write('*IDN?')
				if PowerSupplyDict.get(key)[3].read() != PowerSupplyDict.get(key)[1]: all_ps_idn = False
			except:
				all_ps_idn = False
				break

		elif PowerSupplyDict.get(key)[0] == 'serial':
			PowerSupplyDict.get(key)[3].write(b'*IDN?\n')


		if PowerSupplyDict.get(key)[0] == 'visa':
			try: 
				visa_resource = rm.open_resource(key)
			except: 
				all_ps_init = False
				break
			PowerSupplyDict.get(key).append(visa_resource)
		
		elif PowerSupplyDict.get(key)[0] == 'serial':
			serial_resource = serial.Serial()
			serial_resource.port = key
			serial_resource.baudrate = 9600
			serial_resource.stopbits = 2
			try:
				serial_resource.open()
			except: 
				all_ps_init = False
				break
			PowerSupplyDict.get(key).append(serial_resource)
'''
'''

#### Visa and serial communication intialization ##### 

psr_1 = rm.open_resource('USB0::0x2A8D::0x3302::MY59002179::0::INSTR')
psr_1.write('*IDN?')
if psr_1.read() in dict.get(key): index_psr_1 = psnamelist[psnamelist.index(psr_1.read())]




psr_2 = rm.open_resource('USB0::0x2A8D::0x3302::MY59002179::0::INSTR')
psr_2.write('*IDN?')
psr_2.read()



psr_3 = serial.Serial()
psr_3.port = '/dev/ttyUSB0'
psr_3.baudrate = 9600
psr_3.stopbits = 2
psr_3.open()

psr = serial.Serial()
psr_4.port = '/dev/ttyUSB1'
psr_4.baudrate = 9600
psr_4.stopbits = 2
psr_4.open()



ser.write(b'*IDN?\n')
ser.readline().decode()




'''
#### Initializing power supplies and checking if they are connected properly ####
for ps in psr: 
	ps.write('*IDN?')
	if ps.read() == psnamelist[psr.index(ps)]:
		### Give feedback to logbook, if you can identify all the power supplies
	else:
		### abort mission and tell the logbook to connect power supplies properly and then retry
		stopMon = True
		break
	ps.write('SYST:REM')

#### Database
dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  database = "power_supply_mon"
)
# preparing a cursor object
cursorObject = dataBase.cursor()


#### Monitoring the power supplies ####

while not stopMon:
	
	MeasVoltList = []
	MeasCurrList = []
	
	for ps in psr: 
		ps.write('MEAS:VOLT? (@1)')
		MeasVoltList.append(float(ps.read()))
		ps.write('MEAS:CURR? (@1)')
		MeasCurrList.append(float(ps.read()))
	
	local_time_now = datetime.datetime.now()

	### Make a database entry
	sql = "INSERT INTO power_supply_data (timestamp_loc, board_id, vme_e3633a_1_volt, vme_e3633a_1_curr, vme_e3633a_2_volt, vme_e3633a_2_curr,\
	 		dcfeb_e36233a_1_volt, dcfeb_e36233a_1_curr, dcfeb_e36233a_2_volt, dcfeb_e36233a_2_curr)\
	 		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	val = (local_time_now.strftime('%Y-%m-%d %H:%M:%S'), args.id, str(MeasVoltList[0]), str(MeasCurrList[0]),\
	 		str(MeasVoltList[1]), str(MeasCurrList[1]), str(MeasVoltList[2]), str(MeasCurrList[2]), str(MeasVoltList[3]), str(MeasCurrList[3]))
	cursorObject.execute(sql, val)
	dataBase.commit()

	time.sleep(MeasureInterval)

	### Check if stopMon is true using socket comm




#### Power supplies on local control and stop the communication ####
for ps in psr:
	ps.write('SYST:LOC')
	ps.close()

# disconnecting from server
dataBase.close()
'''

