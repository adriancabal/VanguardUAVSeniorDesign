#Work Cite----------------------------------------------------------
#https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/script 
#-------------------------------------------------------------------------------
import time
import os
import RPi.GPIO as GPIO
import socket
import math
from math import log, cos, tan

#chainLength = 44.0 #date modified: 3-24-16
chainLength =61.0 #date-modified:4-13-16 
GPIO.setmode(GPIO.BCM)
DEBUG = 1

TCP_IP='192.168.1.99'
TCP_IP2='192.168.1.185'

#TCP_IP='192.168.1.30'
TCP_PORT = 9005
TCP_PORT2 = 8008

BUFFER_SIZE = 1024

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


while True:
        # we'll assume that the pot didn't move
        #trim_pot_changed = False

        # read the analog pin
        dist_pot = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #print "digital voltage: ",dist_pot
        #time.sleep(0.1)
        angle_pot= readadc(potentiometer_adc_1, SPICLK, SPIMOSI, SPIMISO, SPICS)
        #print "angle_pot: ", angle_pot
        orientation= angle_pot/4.6
        orientation=round(orientation, 2)
        print "orientation: ", orientation
        #final=trim_pot*(3.3/1024)*(90/3.3)
        #final = trim_pot/4.45
        #final = final*(90.00/116.00)+41-58
        #final = trim_pot/5
        #final = trim_pot
        #final=(dist_pot*90.0/430.0)-2
        #final=dist_pot* 0.21739
        final=dist_pot/4.5
        final = round(final, 2)
	 #print final
        #final=dist_pot/5.0
        #final_deg = final - 20.0 #date modified: 3-24-16
        #print final
        if final>=90:
                final=89.99
        elif final<=0:
                final=0.01
        final=round(final,2)
        #final = 90.0-final  #-15.0
        final_deg=final
        #print "angle: ",  final
        orientation = round(orientation,2)
        #angle_pot = str(angle_pot)     
        #print angle_pot
        final = math.radians(final)
        a = math.cos(final)
        b = math.tan(final)
        c = math.log(b+(1.0/a))
        d = (1.0/b)*c*chainLength
	d = round(d,2)
        #d= str(d)
        print "distance:", d
        combine = str(d) + " \n" + str(orientation)
        #combine = d + " \n" + str(final_deg)
#       print combine


        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(combine)

#       time.sleep(0.5)
        #data = s.recv(BUFFER_SIZE)
#       s.close()
        ##s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ##s2.connect((TCP_IP2, TCP_PORT2))
        #s2.send(str(trim_pot2))
        ##s2.send(combine)
#       print trim_pot2
d = round(d,2)
        #d= str(d)
        print "distance:", d
        combine = str(d) + " \n" + str(orientation)
        #combine = d + " \n" + str(final_deg)
#       print combine


        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(combine)

#       time.sleep(0.5)
        #data = s.recv(BUFFER_SIZE)
#       s.close()
        ##s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ##s2.connect((TCP_IP2, TCP_PORT2))
        #s2.send(str(trim_pot2))
        ##s2.send(combine)
#       print trim_pot2
d = round(d,2)
        #d= str(d)
        print "distance:", d
        combine = str(d) + " \n" + str(orientation)
        #combine = d + " \n" + str(final_deg)
#       print combine


        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(combine)

#       time.sleep(0.5)
        #data = s.recv(BUFFER_SIZE)
#       s.close()
        ##s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ##s2.connect((TCP_IP2, TCP_PORT2))
        #s2.send(str(trim_pot2))
        ##s2.send(combine)
#       print trim_pot2
d = round(d,2)
        #d= str(d)
        print "distance:", d
        combine = str(d) + " \n" + str(orientation)
        #combine = d + " \n" + str(final_deg)
#       print combine


        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(combine)

#       time.sleep(0.5)
        #data = s.recv(BUFFER_SIZE)
#       s.close()
        ##s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ##s2.connect((TCP_IP2, TCP_PORT2))
        #s2.send(str(trim_pot2))
        ##s2.send(combine)
#       print trim_pot2

#       s.close()
        #print "sent  data:", final
        time.sleep(.1)
        #print time.time()

