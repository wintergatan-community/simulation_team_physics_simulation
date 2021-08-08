# -*- coding: utf-8 -*-
"""
Functionally-programmed physics master unit test

Author: Locket Rauncher
Created: 7-17-2021

"""

try:
    import os

    path = os.getcwd()
    os.chdir('../Physics')

    import numpy as np
    import matplotlib.pyplot as plt
    import MarblePhysics_FP
except ModuleNotFoundError:
    print("ERROR: Module not found. Please install the numpy package before running.")
#    raise SystemExit

##############
#Test Settings
##############
numParticles=20
radius=10
spawnRange=90
testTime=0.5
dT=0.000001
plotFreq=10000
v0=300                   # Initial velocity range, actual values are on [-v0,v0]

#quantize positions according to 3r
numPts=int(spawnRange/(3*radius)+1)
#draw positions linearly from the quantized points
linpos=np.random.choice(numPts**3,size=numParticles,replace=False)
#Convert this to x, y, and z coordinates
zpos=(linpos/numPts/numPts).astype(int)*3*radius
ypos=((linpos%(numPts*numPts))/numPts).astype(int)*3*radius
xpos=(linpos%numPts).astype(int)*3*radius
#Calcuate position
pos=np.stack((xpos,ypos,zpos))

#Randomly sample velocity
vel=(np.random.rand(3,numParticles)-0.5)*2*v0

#Set the radius and material
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
