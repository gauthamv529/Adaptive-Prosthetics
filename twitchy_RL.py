#!/usr/bin/env python

import argparse
import rospy
from std_msgs.msg import *
from bento_controller.srv import *
from bento_controller.msg import *
from burlap_msgs.msg import *

def publishState(data):
	# Get the current time
    now = rospy.get_rostime()

    # Test output of the current state of the motor 
    # rospy.loginfo(str(int(round(data.joint_states[0].current_pos))))

    # Start a list of values
    agent0values = []

    # Append a value 
    agent0values.append(burlap_value())

    # Give the attribute name and value
    agent0values[0].attribute = "x"
    agent0values[0].value = str(int(round(data.joint_states[0].current_pos-2))) #"1"
    agent0values.append(burlap_value())
    agent0values[1].attribute = "y"
    agent0values[1].value = str(int(round(data.joint_states[1].current_pos-2))) #"4"

    # Start a list of state information details
    stateDetails = []

    # Append a BURLAP object
    stateDetails.append(burlap_object())

    # Define the name, object class and value set
    stateDetails[0].name = "agent0"
    stateDetails[0].object_class = "agent"
    stateDetails[0].values = agent0values

    # Wrap the state information object in BURLAP state message package
    state = burlap_state(objects=stateDetails)

    # Output the state information to the log
    # rospy.loginfo(state)

    # Publish the state information to the publisher
    pubState.publish(state)


def callback(data):
    if data.data == 'north':
        rospy.loginfo("Going north.")
        pubCommand.publish(header=Header(stamp=rospy.Time().now()), 
                    joint_commands=[JointCommand(id=1, type="velocity", velocity=10.0)])
    elif data.data == 'south':
        rospy.loginfo("Going south.")
        pubCommand.publish(header=Header(stamp=rospy.Time().now()), 
                    joint_commands=[JointCommand(id=1, type="velocity", velocity=-10.0)])
    elif data.data == 'west': 
        rospy.loginfo("Going west.")
        pubCommand.publish(header=Header(stamp=rospy.Time().now()), 
                    joint_commands=[JointCommand(id=2, type="velocity", velocity=10.0)])
    elif data.data == 'east':
        rospy.loginfo("Going east.")
        pubCommand.publish(header=Header(stamp=rospy.Time().now()), 
                    joint_commands=[JointCommand(id=2, type="velocity", velocity=-10.0)])
    else:
        rospy.loginfo("Unexpected direction. I'm not moving.")

if __name__=="__main__":
    rospy.loginfo("BURLAP Interaction")

    rospy.init_node("bento_test")
    
    pause_srv = rospy.ServiceProxy("/bento/pause", Pause)
    pause_srv.call(False)

    # Define the publisher with the BURLAP state message type
    pubState = rospy.Publisher('burlap_state', burlap_state, queue_size=10)

    # Define the publisher which will publish Bento commands
    pubCommand = rospy.Publisher('/bento/command', BentoCommand, queue_size=10)

    # Define the subscriber which will listen for BURLAP actions
    subAction = rospy.Subscriber('/burlap_action', String, callback)

    # Define the subscriber which will listen for Bento states
    subState = rospy.Subscriber('/bento/state', BentoState, publishState)

    rospy.sleep(2)

    # Tell burlap what the starting state is
    # publishState()

    rospy.spin()

    rospy.loginfo("Twitchy GridWorld Complete")