#!/usr/bin/env python
import getch
import roslib; roslib.load_manifest('p3dx_mover')
import rospy
#import math
from geometry_msgs.msg import Twist

#receive file
import time
from Tkinter import *
from time import sleep

import socket

TCP_IP = '192.168.1.99'
TCP_PORT = 9005

BUFFER_SIZE = 20  # Normally 1024, but we want fast $
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

#---------------------------------------------------

USER_QUIT = 100

desiredAngle = 41.0 #modified 3-26-16
#desiredDistance = 27.0
desiredDistance = 40.0
#kp = 0.013 #modified 3-27-16
kp = 0.009 #modified 3-30-16
#kp = 0.0000500
kp_angle = 0.007

kd= 0.000

distance=0
startTime = time.time()
now = time.time()
prevDistError = 0

forward = 0.0
left = 0.0
keyPress = 0

conn, addr = s.accept()
#print 'Connection address:', addr

while(keyPress != USER_QUIT):


        pub = rospy.Publisher('/RosAria/cmd_vel', Twist)
        rospy.init_node('userToRosAria')

        twist = Twist()

        #keyPress = getch.getArrow()

        conn, addr = s.accept()
        data = conn.recv(BUFFER_SIZE)
        arr = data.split(" ")


        try: distance = float(arr[0])
        except (ValueError, IndexError): pass
        try: angle = float(arr[1])
        except (ValueError, IndexError): pass
        print "distance: ", distance

        prev = now
        now = time.time()
        #print now

        #UPDATE PLOT
        timePassed = now - startTime
        timePassed = round(timePassed,1)
        #print timePassed
        distance = round(distance,1)
        angle =round(angle,1)

        distanceError = distance - desiredDistance

        if angle>125:
                desiredAngle= 125
                angleError = angle - desiredAngle
        elif angle<100:
                desiredAngle=100
                angleError = angle - desiredAngle
        else:
                angleError=0


        '''
        if distance<40:
                forward= -0.05
        elif distance>40:
                forward =0.05
        '''
	
	#angleError = angle - desiredAngle
        derivative = (distanceError - prevDistError)/(now - prev)
        #print (now-prev)
        #if(abs(angleError)<15):
        forward = (distanceError *kp) + (kd * derivative)
        #forward+= distanceError*kp
        print "forward: ", forward
        prevDistError = distanceError
        #else:
                #forward =0

        left = angleError*kp_angle
        #left=0

        twist.linear.x = forward
        twist.angular.z = left
        pub.publish(twist)

pub = rospy.Publisher('/RosAria/cmd_vel', Twist)
rospy.init_node('userToRosAria')
twist = Twist()
pub.publish(twist)
exit()

