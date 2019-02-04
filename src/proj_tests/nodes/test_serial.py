#!/usr/bin/env python

import rospy
from rosserial_python import SerialClient, RosSerialServer
from serial import SerialException
from time import sleep
import multiprocessing
from std_msgs.msg import Float64, UInt16, String

import sys

#Initiating node
rospy.init_node('test_serial')

class TestArduinoConnection:
	
	def __init__(self):
		
		#Initializing variables
		self.choice = 0
		
		#Selecting the rate 10Hz
		rate = rospy.Rate(1) 
	
		#Creating publisher
		pub = rospy.Publisher('/act_control',UInt16, queue_size=10)
		
		#Subscribing to arduino_serial
		rospy.Subscriber('/arduino_serial',String,self.message,queue_size=1)
		#rospy.Subscriber('/arduino_serial',Float64,self.message,queue_size=1)
		#rospy.Subscriber('/arduino_height',Float64,self.position,queue_size=1)
		
		while not rospy.is_shutdown():
			rospy.loginfo("Enter 0 to close and 1 to open")
			self.choice = int(raw_input())
			rospy.loginfo("Publishing to act_control topic")
			pub.publish(self.choice)
			
			rospy.wait_for_message('/arduino_serial',String)
			#rospy.wait_for_message('/arduino_height',Float64)
				
			#rate.sleep()
			
	def message(self,data):
		rospy.loginfo(data.data)
		
if __name__=="__main__":

	TestArduinoConnection()
	rospy.spin()
	
	
