
import rospy
from std_msgs.msg import String
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
import matplotlib.pyplot as plt

from Tilecoder3D import numTilings, tilecode_v2, numTilesv2
from Tilecoder3D import numTilesv2 as n
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
	
	def __init__(self, alpha = 0.01, gamma = 0.99, lmbda = 0.7):
		self.alpha = alpha
		self.gamma = gamma  #Since update frequency is ~27Hz (i.e., avg cycle update ~370ms
		self.lmbda = lmbda
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
			#self.e[index] = min(self.e[index]+1,1)
			self.e[index] = self.e[index]+1
			
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
