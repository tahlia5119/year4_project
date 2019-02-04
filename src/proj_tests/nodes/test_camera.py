#!/usr/bin/env python

import rospy

from ar_track_alvar_msgs.msg import AlvarMarkers
from trajectory_msgs.msg import JointTrajectoryPoint
from geometry_msgs.msg import PoseStamped, Pose, PointStamped, Point
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64, UInt64, String
import tf
from tf.transformations import quaternion_from_euler
from scipy.spatial.distance import euclidean
import shlex, subprocess
import os, thread
from math import sqrt, acos, radians, atan2, degrees

#Initializing node
rospy.init_node("test_camera")

class markerTracker:
	
	def __init__(self):
		#Get camera link name
		#self.camera_link = 'camera_link'
	
	
		#Initialize tf listener
		#self.tf = tf.TransformListener()
		#rospy.sleep(2)
	
		rospy.loginfo("Waiting for ar_pose_marker topic")
		rospy.wait_for_message('ar_pose_marker',AlvarMarkers)
		rospy.Subscriber('ar_pose_marker',AlvarMarkers,self.position)
	
	
	def position(self,msg):
		marker = msg.markers
		
		#If marker is empty, return
		if marker==[]:
			return
		z_offset = marker[0].pose.pose.position.z
		y_offset = marker[0].pose.pose.position.y
		x_offset = marker[0].pose.pose.position.x
		
		rospy.loginfo("x: {}, y: {}, z: {}".format(x_offset,y_offset,z_offset))
		rospy.loginfo(marker)
		

if __name__ == "__main__":
	markerTracker()
	rospy.spin()
