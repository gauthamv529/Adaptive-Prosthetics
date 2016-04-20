#!/usr/bin/env python
# TD Learning for implementing GVF.
# Basically the signal we need to predict becomes the reward signal (i.e., cumulant/signal of interest)
# GVF which works!
# Make GVF run in parallel, Offline Learning

from Tilecoder import numTilings, tilecode, numTiles
from Tilecoder import numTiles as n
from pylab import *
import numpy as np
import random
import math
import pickle
numPast = 5

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
		self.alpha = 0.03 #/numTilings
		self.gamma = 0.954   #Since update frequency is ~27Hz (i.e., avg cycle update ~370ms
		self.lmbda = 0.999
		self.numPast = 5 # No. of Past actions ,i.e, history till the previous n timesteps
		self.w = -0.01*np.random.rand(n*numPast)
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
		self.e = self.lmbda*self.e
		for index in features:
			self.e[index] = 1
			
	def Delta(self):
		self.delta = self.R - self.value
		
	def Delta_Update(self):
		self.delta += self.gamma*self.nextValue
				
	def Weights_Update(self):
		self.w += self.alpha * self.delta * self.e
		#self.Trace_Update()
	
	def Trace_Update(self):
		self.e = self.lmbda*self.e

def find_features(F,stateInfo):
	features = np.empty(0)
	numPast = 5
	for i in range(0,numPast):
			tilecode(stateInfo[0+3*i],stateInfo[1+3*i],stateInfo[2+3*i],F)
			F = i*numTiles + F
			features = np.concatenate((features,F),axis=0)
	#print features		
	return features

        
  
def listener():
    count = 0
    
    state = np.loadtxt('state.out')
    velocity = np.loadtxt('velocity.out')
    axes = np.loadtxt('joy_axis.out')
    
    state = np.concatenate((state,state),axis = 0)
    velocity = np.concatenate((velocity,velocity),axis = 0)
    axes = np.concatenate((axes,axes),axis = 0)
    '''
    with open('Twitchy_StateInfo10min.txt') as f:
        content = f.readlines()
    print ("I'm in")
    print np.size(content)
    #print content[300]
    #string = content[300]
    state = []
    velocity = []
    axes = []
    for i in range(10,np.size(content)):
	st = content[i].split(',')
	#print st[4]
	state.append(float(st[1]))
	velocity.append(float(st[2]))
	axes.append(float(st[4]))    
    state = state + state
    velocity = velocity + velocity
    axes = axes + axes 
    '''
    F = np.zeros(numTilings)
    features = np.empty(0)
    stateInfo = np.empty(0)
    saveValue = np.empty(0)

    # GVF Object definition/Initialization
    
    pos = GVF()
    # Initialize State History
    for index in range(0,numPast):
	st = np.array([state[499+index],velocity[499+index],axes[499+index]])
        stateInfo = np.concatenate((stateInfo,st),axis = 0)   
    #Obtain State approximataion - Feature space    
    prev_features = find_features(F,stateInfo)
    
    for i in range(500,np.size(state)-500): 	
	pos.Value(prev_features)			
        pos.R = stateInfo[0] 				#GVF for state[index]
        pos.Delta()
	
        stateInfo = np.empty(0)
        for index in range(0,numPast):
	    st = np.array([state[i+index],velocity[i+index],axes[i+index]])
	    stateInfo = np.concatenate((stateInfo,st),axis = 0)
	    
        new_features = find_features(F,stateInfo)
        pos.Next_Value(new_features)
        pos.Delta_Update()	
				
        pos.Replacing_Traces(prev_features)						
        pos.Weights_Update()
	prev_features = new_features
	
	# Save the Expected Value/Returns
        saveValue = np.concatenate((saveValue,np.array([pos.value])),axis=0)        
        count+=1
	
    np.savetxt('Pos_offline_weights.out', pos.w, fmt='%1.4e')   # use exponential notation
    #np.savetxt('Vel_weights.out', vel.w, fmt='%1.4e')   # use exponential notation
    #np.savetxt('pos2_10minv2.out', pos2.w, fmt='%1.4e')   # use exponential notation
    #np.savetxt('vel2_10minv2.out', vel2.w, fmt='%1.4e')   # use exponential notation    				   
    #np.savetxt('axis10minv2.out', axis.w, fmt='%1.4e')   # use exponential notation
    np.savetxt('save_offline_values.out', saveValue, fmt='%1.4e')   # use exponential notation				   				   
    print (count)
    # spin() simply keeps python from exiting until this node is stopped

if __name__ == '__main__':
    listener()
    
