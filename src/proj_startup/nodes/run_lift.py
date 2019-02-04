#!/usr/bin/env python

import rospy

from ar_track_alvar_msgs.msg import AlvarMarkers
from trajectory_msgs.msg import JointTrajectoryPoint
from geometry_msgs.msg import PoseStamped, Pose, PointStamped, Point
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64, UInt64, String
from tf.transformations import quaternion_from_euler
from scipy.spatial.distance import euclidean
import shlex, subprocess
import os, thread
from math import sqrt, acos, radians, atan2, degrees
import rospy
from rosserial_python import SerialClient, RosSerialServer
from serial import SerialException
from time import sleep
import multiprocessing

import sys

#Initializing node
rospy.init_node("run_lift")

class runLift:
	
	def __init__(self):
		#Intialize variables
		self.Height = 0.0
		self.max_height = rospy.get_param('max_height',25.0)
		self.min_height = rospy.get_param('min_height',15.0)
		
		self.target_visible = False
		self.target_id = rospy.get_param('tag_ids')
		self.found_id = 0
		
		self.z = 0.0
		self.y = 0.0
		self.x = 0.0
		self.z_thresh = rospy.get_param('z_threshold',0.05)
		
		self.control = 0
		r = rospy.get_param('rate',10)
		self.rate = rospy.Rate(r)
		
		#Create publisher
		pub = rospy.Publisher('/act_control',UInt16, queue_size=10)
		
		#Create subscribers
		rospy.Subscriber('ar_pose_marker',AlvarMarkers,self.marker_pose)
		rospy.Subscriber('/arduino_serial',String,self.message,queue_size=1)
		
		#rospy.wait_for_message('/arduino_serial',String)
		

		rospy.loginfo("Waiting for ar_pose_marker topic")
		rospy.wait_for_message('ar_pose_marker',AlvarMarkers)
		
		while not self.target_visible:
			rospy.loginfo('Searching for target...')
			self.search_for_target()
		
		#By this point, the target has been found, adjusting lift to optimal height
		while abs(self.z)>self.z_thresh:
			while self.Height > self.min_height and self.Height < self.max_height:
				#If the marker is below the camera, decrease lift height
				if self.z < 0:
					self.control = 2
					self.lift_control(2)
					rospy.sleep(1)
					self.control = 0
					self.lift_control(0)
					self.control = 3
					self.lift_control(3)
				elif self.z > 0:
					self.control = 1
					self.lift_control(1)
					rospy.sleep(1)
					self.control = 0
					self.lift_control(0)
					self.control = 3
					self.lift_control(3)
					
			#If the height exceeds max height or goes below min height, reset lift and terminate node
			if self.Height < self.min_height or self.Height > self.max_height:
				self.control = 0
				self.lift_control(0)
				rospy.loginfo('Exceeded height restrictions, beginning shutdown process...')
				self.terminate()
			
			#Wait for new ar_pose_marker message to check z value
			rospy.wait_for_message('ar_pose_marker',AlvarMarkers)
				
	
	def search_for_target(self):
		#While the target is not visible
		while not self.target_visible:
		
			#While height is not at max
			while self.Height < self.max_height:
				#Check id of ar_pose_marker topic
				if self.found_id == self.target_id[0]:
					self.target_visible = True
					return
				#Start and stop lift incrementally to look for id
				self.control = 1
				self.lift_control(1)
				rospy.sleep(2)
				self.control = 0
				self.lift_control(0)
				rospy.sleep(2)
				#Getting height of the lift
				self.control = 3
				self.lift_control(3)
				rospy.wait_for_message('ar_pose_marker',AlvarMarkers)
				
			#If the target is not found and the lift has reached max height, reset lift, terminate node
			if not self.target_visible:	
				self.control = 0
				self.lift_control(0)
				rospy.loginfo('No target found, beginning shutdown process...')
				self.terminate()	
				
	
	def marker_pose(self,msg):
		marker = msg.markers
		
		#If marker is empty, return
		if marker==[]:
			return
		self.found_id = marker[0].id
		
		self.z = marker[0].pose.pose.position.z
		self.y = marker[0].pose.pose.position.y
		self.x = marker[0].pose.pose.position.x
		
		rospy.loginfo("x: {}, y: {}, z: {}".format(x_offset,y_offset,z_offset))
		#rospy.loginfo(marker)
		
	def message(self,data):
		rospy.loginfo(data.data)
		if self.control == 3:
			self.Height=float(data.data)
			
	def lift_control(self,val):
		pub.publish(val)
		rospy.sleep(1)
	
	def hook()
		rospy.loginfo('Successfully reset, terminating node...')
		
	def terminate(self):
		#Reset the lift
		self.control = 0
		self.lift_control(0)
		self.control = 3
		self.lift_control(3)
		
		rospy.loginfo('Resetting lift...')
		
		while self.Height > self.min_height:
			self.control = 2
			self.lift_control(2)
			rospy.sleep(1)
			self.control = 0
			self.lift_control(0)
			self.control = 3
			self.lift_control(3)
		
		rospy.on_shutdown(self.hook)
		
		
if __name__ == "__main__":
	runLift()
	rospy.spin()
