# -*- coding: utf-8 -*-
"""
Physics master unit test

Author: Locket Rauncher
Created: 7-17-2021

"""
import os
path = os.getcwd()
os.chdir('../Physics')

import numpy as np
import matplotlib.pyplot as plt
import PhysicsMaster

##############
#Test Settings
##############
numParticles=50
radius=10
spawnRange=300
testTime=0.5
dT=0.00001
plotFreq=1000
v0=500                   # Initial velocity range, actual values are on [-v0,v0]

#generate some positions and velocities
pos=np.random.rand(3,numParticles)*spawnRange
vel=(np.random.rand(3,numParticles)-0.5)*2*v0

#Set the velocity, radius, and material
rad=np.ones((1,numParticles))*radius
mat=np.ones((1,numParticles))

#Assemble particle array
particleArray=np.concatenate((pos,vel,rad,mat),axis=0)

#Plotting things
fig = plt.figure()
ax = plt.axes(projection='3d')

curTime=0

while (curTime<testTime):
    #Update positions
    particleArray=PhysicsMaster.PhysicsCalc(particleArray,dT)
    #Plot update
    if (int(curTime/dT)%plotFreq==0):
        ax.scatter3D(particleArray[0,:], particleArray[2,:],particleArray[1,:], color='black')
    curTime+=dT
    
os.chdir(path)