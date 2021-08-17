# -*- coding: utf-8 -*-
"""
Functionally-programmed physics master unit test

Author: Locket Rauncher
Created: 7-17-2021

"""

try:
    import os

    #path = os.getcwd()
    #os.chdir('../Physics')

    import numpy as np
    import matplotlib.pyplot as plt
    import Wintergatan.Physics.MarblePhysics_OOP as MarblePhysics_OOP
    import matplotlib.animation as animation
except ModuleNotFoundError:
    print("ERROR: Module not found. Please install the numpy and matplotlib package before running.")
#    raise SystemExit

##############
#Test Settings
##############
numParticles=15
radius=10
spawnRange=90
testTime=0.3
dT=0.00001
plotFreq=400
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

curTime=0

data=[]

while (curTime<testTime):
    #Update positions
    particleArray=MarblePhysics_OOP.PhysicsCalc(particleArray,dT)
    #Plot update
    if (int(curTime/dT)%plotFreq==0):
        data.append(particleArray)
    curTime+=dT

#Plotting things
u = np.linspace(0, 2 * np.pi, 10)
v = np.linspace(0, np.pi, 10)
px = 10 * np.outer(np.cos(u), np.sin(v))
py = 10 * np.outer(np.sin(u), np.sin(v))
pz = 10 * np.outer(np.ones(np.size(u)), np.cos(v))

def update_spheres(num, data, surfs):
    for i in range(numParticles):
        surfs[i].remove()
        surfs[i] = ax.plot_surface(px+data[num][0,i], py+data[num][2,i], pz+data[num][1,i], color='b')

# Attaching 3D axis to the figure
fig = plt.figure()
ax = fig.add_subplot(projection="3d")

# Creating surface plots of spheres:
spheres=[]
for i in range(numParticles):
    spheres.append(ax.plot_surface(px+data[0][0,i], py+data[0][2,i], pz+data[0][1,i], color='b'))

# Setting the axes properties
ax.set_xlim3d([-100, 200])
ax.set_xlabel('X')

ax.set_ylim3d([-300, 100])
ax.set_ylabel('Y')

ax.set_zlim3d([-100, 200])
ax.set_zlabel('Z')

ax.set_title('3D Test')

# Creating the Animation object
line_ani = animation.FuncAnimation(fig, update_spheres, len(data), fargs=(data, spheres), interval=50)

plt.show()
    
#os.chdir(path)
