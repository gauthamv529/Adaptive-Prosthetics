# Tilecoding for GVF - Twitchy
# State information consists of Position X, Velocity V and Action A
# Tilecoder uses Normalized Input signals
#from __future__ import division
import math 
npos = 8.0 # No. of divisions for position
nvel = 8.0# No. of divisions for velocity
njoy = 5.0 # No. of divisions for Joystick axis

numTilings = 10

numTiles = numTilings * (npos+1) * (nvel+1) * (njoy+1)  # Extra tile is necessary for offset
limitPos = 1.0       										# 0.5 -(-1.2), i.e, (max - min) of Position
limitVel = 1.0      										# 0.07 -(-0.07), i.e, (max - min) of Velocity
limitJoy = 1.0      										# 1 - (-1), i.e., (max - min) of Joystick axis reading     

def tilecode(in1,in2,in3,tileIndices):
    if in3 > 2: in3 = 2.0
    elif in3 < -2: in3 = -2.0
    in1 += 0.0
    in2 += 0.0
    in3 += 0.6
    in1 /= 8.0
    in2 /= 9.0
    in3 /= 1.2
    
    for i in range (0, numTilings):
        x_off = i * (limitPos/npos) / numTilings
        y_off = i * (limitVel/nvel) / numTilings
        z_off = i * (limitJoy/njoy) / numTilings        
        index1 = int(math.ceil (npos * (in1 + x_off)/limitPos))
        index2 = int(math.ceil (nvel * (in2 + y_off)/limitVel))
        index3 = int(math.ceil (njoy * (in3 + z_off)/limitJoy))
        #print(index1,index2,index3)
        tileIndices[i] = ((npos+1) * (nvel+1) * (njoy+1) * i) + ((npos+1) * (nvel+1) * (index3-1)) + ((npos+1) * (index2-1)) + index1 - 1
    
    
def printTileCoderIndices(in1,in2,in3):
    tileIndices = [-1.0]*numTilings
    tilecode(in1,in2,in3,tileIndices)
    print 'Tile indices for input (',in1,',',in2,',',in3,') are : ', tileIndices

printTileCoderIndices(0.01,0.01,0.01)
#printTileCoderIndices(0.09,0.19,0.15)

'''
printTileCoderIndices(-1.2,-0.07)
printTileCoderIndices(-1.12,-0.07)
printTileCoderIndices(-1.10,-0.07)
printTileCoderIndices(0.5,0.07)
printTileCoderIndices(-1.2,0.07)
printTileCoderIndices(0.5,-0.07)
'''


