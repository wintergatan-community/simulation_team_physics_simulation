# -*- coding: utf-8 -*-
"""
Physics master file

Author: Locket Rauncher
Created: 7-17-2021

"""
import numpy as np

#Format: [Density, Elastic Modulus, Poisson Ratio]
#Units:  [g/mm^3 , MPa            , MPa          ]
materialInfo = np.asarray([[7.81,205000,0.30]]) 
agrav=np.asarray([0,-9.81*1000,0]) #NOTE: LENGTH UNIT IS MM!!!!

#A function to perform collision detection between marbles.
#Usually returns force vectors. Currently returns zeroes always.
def MarbleCollision (marbleSM):
    
    forceArray=np.zeros((3,marbleSM.shape[1]))
    
    #TODO: Calculate distances between centroids, use to find collision depth
    cDist=np.zeros((marbleSM.shape[1],marbleSM.shape[1]))
    #TODO: Using collision depth as a gating variable, calculate XYZ direction
    
    #TODO: Use collision depths to calculate force
    
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
    marbleDensity=materialInfo[marbleInputSM[7,:].astype(int),1]
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