import numpy as np
from Tilecoder import numTilings, tilecode, numTiles
import math 
n = numTiles
numPast = 5
class GVF:
	
	def __init__(self):
		self.alpha = 0.033 #/numTilings
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
		#self.e = self.lmbda*self.e
		for index in features:
			self.e[index] = 1
			
	def Delta(self):
		self.delta = self.R - self.value
		
	def Delta_Update(self):
		self.delta += self.gamma*self.nextValue
				
	def Weights_Update(self):
		self.w += self.alpha * self.delta * self.e
		self.Trace_Update()
	
	def Trace_Update(self):
		self.e = self.lmbda*self.e

def find_features(F,State):
	features = np.empty(0)
	numPast = 5
	for i in range(0,numPast):
			tilecode(State[0],State[1],State[2],F)
			F = i*numTiles + F
			features = np.concatenate((features,F),axis=0)
	return features
	 

  
def listener():
    numPast = 5
    Position = np.loadtxt('state.out')
    Velocity = np.loadtxt('velocity.out')
    Axis = np.loadtxt('joy_axis.out')
    State = np.empty(0)
    F = np.zeros(numTilings)
    pos = GVF()
    for index in range(0,5):
        state = np.array([Position[index],Velocity[index],Axis[index]])
        State = np.concatenate((State,state),axis=0)
		
    for i in range(100,np.size(Position)-100):
		features = find_features(F,State)
		State = np.empty(0) 
		pos.Value(features)			
		pos.R = Position[i] 				#GVF for state[index]
		pos.Delta()			
		pos.Replacing_Traces(features)
		
		for index in range(3,8):
			state = np.array([Position[i+index],Velocity[i+index],Axis[i+index]])
			State = np.concatenate((State,state),axis=0)
			
		features = find_features(F,State)
		pos.Next_Value(features)
		pos.Delta_Update()						
		pos.Weights_Update()
		if i%100 == 0:
			print("We just finished %d steps",i)
		
        
    np.savetxt('Position_Stored.out', pos.w, fmt='%1.4e')   # use exponential notation

if __name__ == '__main__':
    listener()
    
