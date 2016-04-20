#!/usr/bin/env python

import argparse
import rospy
import random
import numpy as np
from std_msgs.msg import *
from bento_controller.srv import *
from bento_controller.msg import *

import time
import matplotlib.pyplot as plt

# def moveJointsWithVel(vel):
#     directions = [-1,1]
#     pub.publish(header=Header(stamp=rospy.Time().now()), 
#         joint_commands=[JointCommand(id=1, type="velocity", velocity=vel*random.choice(directions)),
#                         JointCommand(id=2, type="velocity", velocity=vel*random.choice(directions))])
#     demoStr = "Command: Move joints with velocity " + str(vel)
#     rospy.loginfo(demoStr)
#     rospy.sleep(1)

def moveJointsToPos(pos1,pos2):
    pub.publish(header=Header(stamp=rospy.Time().now()), 
        joint_commands=[JointCommand(id=1, type="position_and_velocity", position=pos1, velocity=10.0),
                        JointCommand(id=2, type="position_and_velocity", position=pos2, velocity=10.0)])
    demoStr = "Command: Move joints to pos " + str(pos1) + " and " + str(pos2)
    rospy.loginfo(demoStr)
    rospy.sleep(1)

# def moveJointWithVel(joint,vel):
#     pub.publish(header=Header(stamp=rospy.Time().now()), 
#         joint_commands=[JointCommand(id=joint, type="velocity", velocity=vel)])
#     demoStr = "Command: Move joint " + str(joint) + " with velocity " + str(vel)
#     rospy.loginfo(demoStr)
#     rospy.sleep(1)   

# def moveJointToPos(joint,pos):
#     pub.publish(header=Header(stamp=rospy.Time().now()), 
#         joint_commands=[JointCommand(id=joint, type="position_and_velocity", position=pos, velocity=10.0)])
#     demoStr = "Command: Move joint " + str(joint) + " to position " + str(pos)
#     rospy.loginfo(demoStr)
#     rospy.sleep(0.5) 

def callback(data):
    rospy.loginfo("%s",data.joint_states[0].current_pos)

if __name__=="__main__":
    
    # Start a bento_test node for communication
    rospy.init_node("bento_test")
    
    # Ensure that the motors are not paused
    pause_srv = rospy.ServiceProxy("/bento/pause", Pause)
    pause_srv.call(False)

    # Build the publisher and sleep to ensure it is configured
    pub = rospy.Publisher('/bento/command', BentoCommand, queue_size=0)
    # sub = rospy.Subscriber("/bento/state", BentoState, callback)
    rospy.sleep(1)

    # Start the velocity control demo
    rospy.loginfo("Velocity control demo start.")

    for i in range(1,21): 
        # moveJointsWithVel(8)
        positions = np.arange(1,4,0.1)
        moveJointsToPos(random.choice(positions),random.choice(positions))
        # moveJointToPos(2,random.choice(positions))

    rospy.loginfo("Velocity control demo complete.")