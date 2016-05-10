import time
from Tkinter import *
from time import sleep
import getch
import socket
import time



root =Tk()	
root.geometry("2000x1000")
var = StringVar()
var2 = StringVar()
var.set(str(0))
var2.set(str(0))

angleLabel = Label(root, text = "Angle: ", font=("Arial",200))
#angleLabel = Label(root, text = "Desired Distance: 27 ", font=("Arial",120))
angleLabel.place(x=10, y=10)

aLabel = Label(root, textvariable =var,font=("Arial",200))
aLabel.place(x=1000, y=10)

distanceLabel = Label(root, text = "Distance: ", font=("Arial",200))
distanceLabel.place(x=10, y=500)

dLabel = Label(root, textvariable =var2,font=("Arial",200))
dLabel.place(x=1150, y=500)

TCP_IP = '192.168.1.185'
TCP_PORT = 9085
#TCP_PORT = 9005
BUFFER_SIZE = 20  # Normally 1024, but we want fast $
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
USER_QUIT = 100



'''
#import graphing stuff
import matplotlib.pyplot as plt

xar=[]
yar=[]

plt.ion()
#plt.figure(0)
plt.figure(0,figsize=(15,15))
#plt.subplot(2,1,1)
plt.plot(xar,yar,'bo')
#plt.axis([25,63, 0,63])
plt.xlim(25,63)
plt.ylim(0,63)
plt.title('Measured Distance vs. Actual Distance)')
plt.ylabel('Measured Distance (inches)')
plt.xlabel('Actual Distance (inches)')
plt.show()
'''
distance=0
angle=0


startTime = time.time()
timePassed = 0

f = open("measuredsquare4.csv","w")
f.write("time"+","+"DistanceMeasured"+',' +'Orientation'+'\n')
while (True):
	
	#t = time.time()
	#print t

	conn, addr = s.accept()
	data = conn.recv(BUFFER_SIZE)
	arr = data.split()
	var.set(arr[1])
	var2.set(arr[0])
	root.update_idletasks()
	#timePassed = time.time() - startTime
	distance = float(arr[0])
	angle = float(arr[1])
	f.write(str(time.time())+","+str(distance)+','+str(angle) +'\n')
	#print "distance: ", distance

'''
	#UPDATE PLOT
	timePassed = time.time() - startTime
	timePassed = round(timePassed,1)
	#print timePassed
	distance = round(distance,1)
	angle =round(angle,1)
	xar.append(timePassed)
	yar.append(distance)
	#yangle.append(angle)
	#plt.figure(0)
	plt.subplot(2,1,1)
	plt.plot(xar,yar, 'bo' )	
	#plt.plot(xar,yar, 'bo', xar, yar, 'k')	
	plt.plot([0,timePassed],[40,40], 'r')	
	plt.axis([0, timePassed, 0, 63])
	plt.draw()

#plt.savefig('measuredDistance_vs_time.png')
'''

'''
f = open("measuredvsactual.csv","w")
while True:
	actualDistance = raw_input("input>> ")
	if (actualDistance != "q"):
		for i in range(10):
			#actualDistance = int(actualDistance)		
		
			conn, addr = s.accept()
			data = conn.recv(BUFFER_SIZE)
			arr = data.split()
			distance=arr[0]
			var.set(arr[1])
			var2.set(arr[0])
			root.update_idletasks()
			distance = float(arr[0])
			angle = float(arr[1])
			#print "distance: ", distance
	
	
			#UPDATE PLOT
			#timePassed = time.time() - startTime
			#timePassed = round(timePassed,1)
			#print timePassed
			if (i>5):
				distance = round(distance,1)
				angle =round(angle,1)
				f.write(actualDistance + ','+str(distance)+'\n')

				#xar.append(actualDistance)
				#yar.append(distance)
				#yangle.append(angle)
				#plt.figure(0)
				#plt.subplot(2,1,1)
				

	
	else:	
		
		f.close()
		break
#plt.savefig('ramp_measuredvsactual3.png')
'''
'''
f = open("xydata_2nd_2.csv","w")
while True:
	input = raw_input("input>> ")
	if (input != "q"):
		for i in range(50):
			conn, addr = s.accept()
			data = conn.recv(BUFFER_SIZE)
			arr = data.split()
			distance=arr[0]
			var.set(arr[1])
			var2.set(arr[0])
			root.update_idletasks()
			f.write(input + ','+str(distance)+'\n')
	else:
		f.close()
		break
'''
