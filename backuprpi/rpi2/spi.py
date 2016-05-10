#Work Cite----------------------------------------------------------
#https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/script 
#-------------------------------------------------------------------------------
import time
import os
import RPi.GPIO as GPIO
import socket
#import math
#from math import log, cos, tan
from math import *
#chainLength = 44.0 #date modified: 3-24-16
chainLength = 63.0 #date modified: 4-7-16
GPIO.setmode(GPIO.BCM)
DEBUG = 1
TCP_IP='192.168.1.123'
TCP_IP2='192.168.1.185' #updated 4-9-16
#TCP_IP='192.168.1.185'
#TCP_IP='192.168.1.30'
TCP_PORT = 9005
TCP_PORT2 = 8008 #updated 4-9-16
BUFFER_SIZE = 1024

#heightL = 43.8 # inches. added 4-10-16
#heightR = 28.5 # inches. added 4-10-16
 
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)
 
        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low
 
        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1
 
        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout


# SPI port on the ADC to the Cobbler
SPICLK =11
SPIMISO =9
SPIMOSI = 10
SPICS = 8

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

potentiometer_adc = 0;
potentiometer_adc_1 = 1;
potentiometer_adc_2 = 2;
	
while True:
        # we'll assume that the pot didn't move
        #trim_pot_changed = False
 
        # read the analog pin
	dist_pot = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
	#print "digital voltage: ", dist_pot
        #time.sleep(0.1)
	angle_pot= readadc(potentiometer_adc_1, SPICLK, SPIMOSI, SPIMISO, SPICS)
	orientation= angle_pot/5.1
	digital3 = readadc(potentiometer_adc_2, SPICLK, SPIMOSI, SPIMISO, SPICS)
	print "digital3: ", digital3 
	#final=trim_pot*(3.3/1024)*(90/3.3)
	#final = trim_pot/4.45
	#final = final*(90.00/116.00)+41-58
	#final = trim_pot/5
	#final = trim_pot
	#final=(dist_pot*90.0/430.0)-2
	final = dist_pot/4.5
	theta2 = digital3/4.5
	if theta2>=90:
		 theta2=89.99
	elif theta2<=0: 
		theta2 = 0.01
	theta2 = round(theta2, 2)
	angle2 = theta2
	print "theta2: ", theta2
	#final=dist_pot*0.21739
	#final =dist_pot/4
	final1=(225.0/1024.0)*dist_pot
	##print "final1: ", final1
	#final=dist_pot/5.0
	#final_deg = final - 20.0 #date modified: 3-24-16
	#print final
	if final>=90:
		final=89.99
	elif final<=0:
		final=0.01
	#final = 90.0-final  #-15.0
	final_deg=final1
	final = round(final,2)
	print "theta1: ",  final
	orientation = round(orientation,2)
	#angle_pot = str(angle_pot)	
	#print angle_pot
	final = radians(final)

	a = cos(final)
	b = tan(final)
	c = log(b+(1.0/a))
	d = (1.0/b)*c*chainLength
	err = -0.0985*d +5.6
	d= d + err
	d= round(d,2)
	err2= -0.0697*d +8.62585
        d=d+err2
        d=round(d,2)	

	'''
	#Different Heights Formula added 4-10-16
	theta1 = final
	theta2 = radians(theta2)
	length1 = chainLength/((tan(theta2)/tan(theta1))+1)
	length2 = chainLength/((tan(theta1)/tan(theta2))+1)
	x1 = (length1/tan(theta1))*log(tan(theta1)+(1.0/cos(theta1)))
	x2 = (length2/tan(theta2))*log(tan(theta2)+(1.0/cos(theta2)))
	d = x1 + x2
	d = round(d, 2)
	'''
	#print "distance:", d
	#print "orientation: ", orientation
	combine = str(d) + " \n" + str(orientation)
	#combine = str(d) + " " +str(orientation)
	#combine = d + " \n" + str(final_deg)
#	print combine
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#s.sendto(combine,(UDP_IP,UDP_PORT))
	s.connect((TCP_IP, TCP_PORT))
	s2.connect((TCP_IP2, TCP_PORT2))
	s.send(combine)
	s2.send(combine)

#	time.sleep(0.5)
	#data = s.recv(BUFFER_SIZE)
#	s.close()
#	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#	s.connect((TCP_IP, TCP_PORT2))
#	s.send(str(trim_pot2))
#	print trim_pot2
#	s.close()
	#print "sent  data:", final
	time.sleep(0.1)

