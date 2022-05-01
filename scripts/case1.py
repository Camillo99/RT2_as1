#! /usr/bin/env python

"""
.. module:: autonomous_point_reaching
    :platform: Unix
    :synopsis: Python module for handling the first option selected by the user
    
.. moduleauthor:: Camillo Murgia

This node implements the first option seleceted by the user

Service:
    /coordinate_xy
    
Action:
    /move_base
    
"""





import rospy
from a3_code.srv import Coordinate_xy	#service server
# 3 imports for handling the action
import actionlib
from move_base_msgs.msg import *
from actionlib_msgs.msg import *
 


def handler(req):
    """
    Read the request provided by the user
    
    Create a goal (using user's data)
    
    Send the goal and wait for a result
    
    A timeout is set to prevent infinite waiting in case the target is out of the range
    of the robot
    
    If the target is reached or if the timeout is over the service return to user_controller 
    
    If the target is not reached call cancel_goal for the action
    """
    
    
    #copy data provided by the user
    x = req.x
    y = req.y
    
    print("calling the action x: ",x," y: ",y)
    #starting the action and wait for responce by the server
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    
    #create the goal
    goal = MoveBaseGoal()
    #set the goal parameter
    goal.target_pose.header.frame_id = 'map'
    goal.target_pose.pose.orientation.w = 1
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    #send the goal
    client.send_goal(goal)
    #wait for result
    wait = client.wait_for_result(timeout=rospy.Duration(50.0))
    if not wait:
        #target not reached
        #call cancel goal and return
    	print("abort the mission!!")
    	client.cancel_goal()
    	return -1
    #in case of target reached
    return 1

def my_coordinate_server():
    """
    Print general information about the node
    
    Initialize the node
    
    Call the service handler
    
    """
    #print general information about the node
    print("autonomous moving handler node")
    print("please do not close this shell")
    #initialize the node
    rospy.init_node('coordinate_controller')
    #call the service handler
    s = rospy.Service('coordinate_xy' ,Coordinate_xy ,handler)
    print("service ready")
    rospy.spin()

#main
if __name__=="__main__":
    my_coordinate_server() 
