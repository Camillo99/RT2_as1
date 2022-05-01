#! /usr/bin/env python


"""
.. module:: keyboard_controller
    :platform: Unix
    :synopsis: Python module for handling the different guidance modality
    
.. moduleauthor:: Camillo Murgia

This node allows the UI for controlling the robot motion, to efficently comunicate with the robot enviroment

Service:
    /keyboard_type
    
"""


import rospy
from a3_code.srv import Keyboard_type	#service server
import os   #call in terminal


def handler(req):
    """
    Read the request parameter and choose whether it is case 2 or case 3 of the 
    user option menu, then call the dedicated launch file
    
    Args:
        req: value of the request (case 2 or case 3)
        
    Returns:
        always returns 0
    
    """
    if req.keyboard_case == 1:
       #call keyboard teleop w/o obstacle avoidance
       print("calling teleop twist keyboard")
       os.system("roslaunch a3_code case2.launch") 
       
    elif req.keyboard_case == 2:
        #call keyboard teleop and the osbstacle avoidance
        print("calling teleop twist keyboard with obstacle avoidance control")
        #call the launcher for case 3
        os.system("roslaunch a3_code case3.launch")
    else:
        print("incorrect parameter")
    return 0         
   
def my_keyboard_server():
    """
    Initialize the ROS node and call the service handler
    
    
    """
    #print general information about the node
    print("handler for keyboard controlling of the robot")
    print("please do not close this shell")
    #initialize the node
    rospy.init_node('keyboard_controller')
    #call the service handler
    s = rospy.Service('keyboard_type' ,Keyboard_type ,handler)
    print("service ready")
    rospy.spin()

#main
if __name__=="__main__":
    my_keyboard_server()
