#!/usr/bin/env python
# TD Learning for implementing GVF.
# Basically the signal we need to predict becomes the reward signal (i.e., cumulant/signal of interest)
# GVF which works!

import rospy
from std_msgs.msg import String
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
import matplotlib.pyplot as plt

from Tilecoder3D import numTilings, tilecode, numTiles
from Tilecoder3D import numTiles as n
from pylab import *
import numpy as np
import random
import math
import pickle
numPast = 5
time_limit = 900
import argparse
from std_msgs.msg import *
from bento_controller.srv import *
from bento_controller.msg import *
'''
def td_lambda(data):    
    #print rospy.get_name(), "I heard %s"%str(data.data[0])
    #print "It works!"
    global state
    state = data.data
    return state
'''
class GVF:
	
	def __init__(self):
		self.alpha = 0.01/numTilings
		self.gamma = 0.97   #Since update frequency is ~27Hz (i.e., avg cycle update ~370ms
		self.lmbda = 0.999
		self.numPast = 2 # No. of Past actions ,i.e, history till the previous n timesteps
		self.w = np.zeros(n*numPast)
		self.e = np.zeros(n*numPast)
		self.delta = 0
		self.R = 0     #Cumulant Signal
		self.value = 0
		self.F = np.zeros(numTilings)
		self.nextValue = 0
		
	def Value(self,Features):
		Val = 0.0
		for index in Features:
			Val += self.w[index]
		self.value = Val
			
	def Next_Value(self,Features):
		Val = 0.0
		for index in Features:
			Val += self.w[index]
		self.nextValue = Val	
		    
	def Replacing_Traces(self,features):
		self.e = self.gamma * self.lmbda * self.e
		for index in features:
			self.e[index] = min(self.e[index]+1,1)
			
	def Delta(self):
		self.delta = self.R - self.value
		
	def Delta_Update(self):
		self.delta += self.gamma*self.nextValue
				
	def Weights_Update(self):
		self.w += self.alpha * self.delta * self.e
		#self.Trace_Update()
	
	def Trace_Update(self):
		self.e = self.lmbda*self.e
	
	def master_func(self,R,prev_features,next_features):
	    self.Value(prev_features)
	    self.R = R
	    self.Delta()
	    self.Next_Value(next_features)
	    self.Delta_Update()
	    self.Replacing_Traces(prev_features)
	    self.Weights_Update()
	    pass
		

def find_features(Pos,Z,Vel):
    F = [0] * numTilings	
    for i in range(0,numPast):
	tilecode(Pos[i],Z[i],Vel[i],F)
	F = [x+(i*numTiles) for x in F]
	if i == 0:
	    features = F
	else:
	    features = features + F
    return features
	 
def state_callback(data):    
    global state
    global now
    state = data.data[0:4]
    with open('twitchy_states.pkl', 'wb') as output:
        pickle.dump(state, output, pickle.HIGHEST_PROTOCOL)
    if now.secs < time_limit:
        #print(rospy.get_name(), "I heard %s"%str(state))
        pass
    else:
        print("It's done")
        
  
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    global state
    global now
    rospy.init_node('listener', anonymous=True)
    count = flag = flag2 = steps = 0
   
    rospy.Subscriber("/twitchy/state", numpy_msg(Floats), state_callback)
    #rospy.Subscriber("/twitchy/state", numpy_msg(Floats), td_lambda)
    pub = rospy.Publisher('/bento/command', BentoCommand, queue_size=10)
    tic = rospy.get_rostime()
    toc = rospy.get_rostime()
    now = toc - tic
    rospy.loginfo("Current time %i %i", now.secs, now.nsecs)
    
    F = np.zeros(numTilings)
    features = np.empty(0)
    
    prevState = np.empty(0)
    Pos = []
    Pos_next = []
    Z = []
    Vel = []
    Vel_next = []  
    Znext = []
    rospy.sleep(2)
    timeSteps = 200000
    # GVF Object definition/Initialization
    steps = 0
    
    elbow = GVF()
    wrist = GVF()
    elbow_vel = GVF()
    G = ind = 0
    r = rospy.Rate(1)
    
    returns_elbow = np.zeros(timeSteps)
    returns_wrist = np.zeros(timeSteps)
    returns_elbow_vel = np.zeros(timeSteps)
    
    t1 = [2.7, 2.0, 2.7, 3.3]
    t2 = [3.0, 2.1, 3.0, 3.9]
    x = y = 0
    for i in range(0,numPast):
	Pos.append(state[0])
	Vel.append(state[1])
	Z.append(state[2])
    while (now.secs <  time_limit):
        tiki = rospy.get_rostime()
        #temp = state
        prev_features = find_features(Pos,Z,Vel)
	Pos_next = Pos[:]
	Vel_next = Vel[:]
	Znext = Z[:]
	Pos_next.remove(Pos_next[0])
	Vel_next.remove(Vel_next[0])
	Pos_next.append(state[0])
	Vel_next.append(state[1])
	Znext.remove(Z[0])
	Znext.append(state[2])      
        
        next_features = find_features(Pos_next,Znext,Vel_next)	
	
	elbow.master_func(state[0],prev_features,next_features)
	wrist.master_func(state[2],prev_features,next_features)
	#elbow_vel.master_func(state[1],prev_features,next_features)
	
	Pos = Pos_next[:]
	Vel = Vel_next[:]
	Z = Znext[:]
	returns_elbow[steps] = elbow.value
	returns_wrist[steps] = wrist.value
	returns_elbow_vel[steps] = elbow_vel.value
	steps += 1			
	prevState = np.concatenate((prevState,np.asarray(state)))
	if steps >=timeSteps:
	    break		        
        toc = rospy.get_rostime()
        now = toc - tic
        
        count+=1
        taka = rospy.get_rostime()
        updateTime = taka - tiki
	
        if now.secs % 20 < 1:
	    print ("Update time = %f",now.secs)
	    pub.publish(header=Header(stamp=rospy.Time().now()), 
			joint_commands=[JointCommand(id=2, type="position_and_velocity", position=t2[ind], velocity=0.5)])
	    flag = 1
	    x = t1[ind]
	    y = t2[ind]
	    r.sleep()
	    
	if abs(state[2] - t2[ind]) < 0.05 and flag:	    
		pub.publish(header=Header(stamp=rospy.Time().now()), 
			joint_commands=[JointCommand(id=1, type="position_and_velocity", position=t1[ind], velocity=0.5)])
		flag = 0
		ind += 1
		if ind ==4:
		    ind = 0
        print x,y,state[0],state[2],steps, now.secs, elbow.value, wrist.value, elbow.delta, wrist.delta, state[1]
    np.savetxt('Elbow_weights_v3.out', elbow.w, fmt='%1.4e')   # use exponential notation
    np.savetxt('Elbow_vel_weights.out', elbow_vel.w, fmt='%1.4e')   # use exponential notation
    np.savetxt('Wrist_weights_v2.out', wrist.w, fmt='%1.4e')   # use exponential notation
    
    np.savetxt('prev_state_v2.out', prevState, fmt='%1.4e')   # use exponential notation		   				   
    np.savetxt('elbow_value_v2.out', returns_elbow, fmt='%1.4e')   # use exponential notation		   				   
    np.savetxt('wrist_value_v2.out', returns_wrist, fmt='%1.4e')   # use exponential notation		   				   
    np.savetxt('elbow_vel_value_v2.out', returns_elbow_vel, fmt='%1.4e')   # use exponential notation	
    plt.plot(returns_elbow)	   				   
    print (count)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
    
