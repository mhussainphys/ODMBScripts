import numpy as np
import sys
import matplotlib
import matplotlib.pyplot as plt
plt.style.use('ggplot')
matplotlib.use( 'tkagg' )


BaseFileDirectory = '/homes/mhussain/ODMBScripts/PCTest/PCTestData/'
PCTDataFile = BaseFileDirectory + 'PCTestData_Run_%s.txt' % sys.argv[1] 


DataArray = np.array(np.loadtxt(PCTDataFile, delimiter='\t', unpack=False, skiprows=5))
CurrentArray = DataArray[:,[2]]
TimeArray = DataArray[:,[0]]
VoltageArray = DataArray[:,[1]]

#print(DataArray[:,[2]])
fig, axs = plt.subplots(1,2, figsize=(12,9), sharey='row')
ax1,ax2 = axs

plt.title("Current vs Time graph")
plt.xlabel("Time (s)")
plt.ylabel("Current (A)")
ax1.plot(TimeArray - TimeArray[0], CurrentArray, color ="green")
ax2.plot(TimeArray - TimeArray[0], VoltageArray, color ="green")
plt.show()






'''
#plt.ion()   
fig, axs = plt.subplots(1,2, figsize=(12,9), sharey='row')
ax1,ax2 = axs
ax1.set_ylim([0,20])
ax2.set_ylim([0,1])
#ax1.scatter(time.time() - Timestamp, MeasVolt, color = 'black')
#ax2.scatter(time.time() - Timestamp, MeasCurr, color = 'black')
plt.pause(0.0005)'''