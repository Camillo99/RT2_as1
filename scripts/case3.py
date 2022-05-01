#! /usr/bin/env python



"""
.. module:: case_3
    :platform: Unix
    :synopsis: Python module for handling the third option selected by the user
    
.. moduleauthor:: Camillo Murgia

This node implements the third option seleceted by the user, and prevent the robot to collide with the wall of the enviroment

Subscribes to:
    /scan data measured by a laser scan sensor
    /remap_cmd_vel data from the teleop_twist_keyboard node for controlling the robot movement
    
Publishes to:
    /cmd_vel send the Twist to the robot simulator 

    
"""





import rospy
import numpy
from geometry_msgs.msg import Twist, Vector3    #for cmd_vel topic
from sensor_msgs.msg import LaserScan           #for scan topic

#linit distance to an ovstacle for avoiding collision
min_star = 0.5

#initialize a Twist object for the publisher
init = Vector3(0, 0, 0)
repost = Twist( init, init)


def compute_min_dist(ranges):
    """
    function for computing the minimal measured distance on the right, front and left of the robot
    
    Args:
        ranges: array from the LaserScan, containing all the distances measured by the laser sensor
        
    Returns:
        double[]: a 3 dimensional array containing the right, front, and left minimal distance measured by the laser sensor
    
    """
    #first block -> right side
    #second block -> front side
    #third block -> left side
    #init
    distance = [0,0,0]
    #divide the ranges array in 3 parts
    #right part
    #middle part
    #left part
    sub_right = ranges[0:240]
    sub_mid = ranges[240:480]
    sub_left = ranges[480:721]
    #compute and store the min distance
    distance[0] = min(sub_right)
    distance[1] = min(sub_mid)
    distance[2] = min(sub_left)
    return distance
        
  

def callback_scan(data):
    """
    this function takes both the twist from remap_cmd_vel and the distances from laser scan
    and in case of illegal motion (colliding the wall) prevents this action zeroing the twist published to the robot
    
    Args:
        data: data from /scan topic
    
    """
    
    #use a global variable 
    global repost
    #initialize the publisher
    pub = rospy.Publisher('cmd_vel',Twist, queue_size=10)
    #compute the minimun obsable distance to the right, left and in front of the robot
    distances = compute_min_dist(data.ranges)

    if distances[0] < min_star :
        if repost.angular.z < 0 :
            #avoid turning right -> w = -1   
            repost.angular.z = 0    
    if distances[1] < min_star:
        if repost.linear.x > 0 :
            #deny moving toward an obstacle
            repost.linear.x = 0
    if distances[2] < min_star :
        if repost.angular.z > 0 :
            #avoid turning left -> w = 1
            repost.angular.z = 0
    #pubblic on topic cmd_vel to the robot
    pub.publish(repost)




#copy remap_cmd_vel on repost -> ready to be:
#modified by the controller or
#reposted as it was
def callback_remap(data):
    """
    this function copies remap_cmd_vel in a global variable -> ready to be:
    modified by the controller or
    reposted as it was
    
    Args:
        data: twist from the remap_cmd_vel topic
    
    
    """
    #use a global variable
    global repost
    repost = data
  
def keyboard_remap():
    """
    Initialize the ROS node and subscribe to topics:
    /remap_cmd_vel 
    /scan
    
    """
    #initialize the node
    rospy.init_node('keyboard_remap_node')
    #subscriber to topic remap_cmd_vel    
    rospy.Subscriber("/remap_cmd_vel", Twist, callback_remap)
    #subscriber to topic scan
    rospy.Subscriber("/scan", LaserScan, callback_scan)
    rospy.spin()
    
#main 
if __name__=="__main__":
    keyboard_remap()
