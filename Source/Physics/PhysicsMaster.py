# -*- coding: utf-8 -*-
"""
Physics master file

Author: Locket Rauncher
Created: 7-17-2021

"""
import numpy as np

#Format: [Density, Elastic Modulus, Poisson Ratio]
#Units:  [g/mm^3 , MPa            , MPa          ]
#Materials: Stainless, Testing material (soft/elastic)
materialInfo = np.asarray([[7.81,205000,0.30],\
                           [7.81,20.5,0.30]])


agrav=np.asarray([0,-9.81*1000,0]) #NOTE: LENGTH UNIT IS MM!!!!

#A function to perform collision detection between marbles.
#Usually returns force vectors. Currently returns zeroes always.
def MarbleCollision (marbleSM):
    nMarbles=marbleSM.shape[1]
    forceArray=np.zeros((3,nMarbles))
    
    #Calculate dx, dy, and dz for each marble with each other marble:
    dx=np.tile(marbleSM[0,:],(nMarbles,1))-np.tile(marbleSM[0,:],(nMarbles,1)).T
    dy=np.tile(marbleSM[1,:],(nMarbles,1))-np.tile(marbleSM[1,:],(nMarbles,1)).T
    dz=np.tile(marbleSM[2,:],(nMarbles,1))-np.tile(marbleSM[2,:],(nMarbles,1)).T
       #Note that this tiling is just a clever way to compare each element to each other element
    
    #Calculate distances between centroids, use to find collision depth
    cDist=np.sqrt(dx*dx+dy*dy+dz*dz)
    addRad=np.tile(marbleSM[6,:],(nMarbles,1))+np.tile(marbleSM[6,:],(nMarbles,1)).T
    colDepth=np.maximum(addRad-cDist,0) #Collision depth cannot be smaller than zero, hence "max"
    np.fill_diagonal(colDepth,0)
    
    #Set up effective radius and elastic modulus for hertzian contact calc:
    rEff=1/(1/np.tile(marbleSM[6,:],(nMarbles,1))+1/np.tile(marbleSM[6,:],(nMarbles,1)).T)
    eVec=materialInfo[marbleSM[7,:].astype(int),1]
    eEff=rEff=1/(1/np.tile(eVec,(nMarbles,1))+1/np.tile(eVec,(nMarbles,1)).T)
    
    #Use sphere-on-sphere contact equations to determine force at depth:
    fMag=np.sqrt(np.power(colDepth,3)*(16.0/9.0)*rEff*eEff*eEff)
    
    #Calculate XYZ direction and turn into forces:
    xDir=dx/cDist
    np.fill_diagonal(xDir,0) #Note the diagonals are NaNs, we have to fix this
    yDir=dy/cDist 
    np.fill_diagonal(yDir,0) 
    zDir=dz/cDist 
    np.fill_diagonal(zDir,0) 
    
    fx=np.sum(xDir*fMag,axis=1)
    fy=np.sum(yDir*fMag,axis=1)
    fz=np.sum(zDir*fMag,axis=1)
    forceArray=np.stack((fx,fy,fz))
    return forceArray
#A function to update marble positions using physics calculations.
#Currently only does acceleration due to gravity
#
#marbleInputSM is [x,y,z,vx,vy,vz,radius,materialIndex]
def PhysicsCalc (marbleInputSM,dT):
    
    #Set up some references to input data:
    xInput=marbleInputSM[0:3,:]
    vInput=marbleInputSM[3:6,:]
    
    #Make a copy of the input array for output
    marbleOutputSM=np.copy(marbleInputSM)
    xOutput=marbleOutputSM[0:3,:]
    vOutput=marbleOutputSM[3:6,:]
    
    #Calculate mass:
    marbleDensity=materialInfo[marbleInputSM[7,:].astype(int),0]
    marbleVolume=np.power(marbleInputSM[6,:],3)*4/3*np.pi
    marbleMass=marbleDensity/marbleVolume
    
    #Calculate force on the marbles due to collisions:
    fMarbleMarble=MarbleCollision(marbleInputSM)
    
    #Calculate acceleration due to collisions and gravity:
    aTotal=fMarbleMarble/marbleMass + np.tile(agrav,(marbleInputSM.shape[1],1)).T
    
    #Recalculate velocity and position. Note the referencing notation to modify the original values.
    #TODO: Switch to Newmark Beta Method
    vOutput[:,:]=vInput+aTotal*dT
    xOutput[:,:]=xInput+(vInput+vOutput)/2*dT
    
    return marbleOutputSM