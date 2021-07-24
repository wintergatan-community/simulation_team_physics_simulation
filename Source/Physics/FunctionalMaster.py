# -*- coding: utf-8 -*-
"""
Functionally-Programmed physics master file. Do not use this one.

Author: Locket Rauncher
Created: 7-17-2021

"""
import numpy as np

#Format: [Density, Elastic Modulus, Poisson Ratio]
#Units:  [g/mm^3 , MPa            , mm/mm        ]
#Materials: Stainless, Testing material (soft/elastic)
materialInfo = np.asarray([[7.81,205000,0.30],\
                           [7.81,2050,0.30]])


agrav=np.asarray([0,-9.81*1000,0]) #NOTE: LENGTH UNIT IS MM!!!!

# 0 is forward finite difference for velocity, central finite difference for position
# 1 is explicit central finite difference via newmark-beta
updateScheme=2
epsilon=0.000001   #The error for radius-normalized position change in predictor-corrector
maxIters=100


#A function to perform marble-to-marble collision detection
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
    np.fill_diagonal(cDist,1) #Note the diagonals are zeros, we have to fix this
    xDir=dx/cDist
    yDir=dy/cDist 
    zDir=dz/cDist 
    
    fx=np.sum(xDir*fMag,axis=1)
    fy=np.sum(yDir*fMag,axis=1)
    fz=np.sum(zDir*fMag,axis=1)
    forceArray=np.stack((fx,fy,fz))
    return forceArray
#A function to update marble positions using physics calculations.
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
    aInitial=fMarbleMarble/marbleMass + np.tile(agrav,(marbleInputSM.shape[1],1)).T
    
    #Recalculate velocity and position. Note the referencing notation to modify the original values.
    if (updateScheme==0):
        vOutput[:,:]=vInput+aInitial*dT
        xOutput[:,:]=xInput+(vInput+vOutput)/2*dT
    elif (updateScheme==1):
        xOutput[:,:]=xInput+vInput*dT+(dT*dT)/2*aInitial
        aFinal=(MarbleCollision(marbleOutputSM))/marbleMass + np.tile(agrav,(marbleInputSM.shape[1],1)).T
        vOutput[:,:]=vInput+(aInitial+aFinal)/2*dT
    elif (updateScheme==2):
        xOutput[:,:]=xInput+vInput*dT+(dT*dT)/2*aInitial
        aFinal=(MarbleCollision(marbleOutputSM))/marbleMass + np.tile(agrav,(marbleInputSM.shape[1],1)).T
        vOutput[:,:]=vInput+(aInitial+aFinal)/2*dT
        xTest=xInput+vInput*dT+(dT*dT)/2*(aInitial+aFinal)/2
        iters=0
        while(np.max((xTest-xOutput)/marbleInputSM[6,:])>epsilon and iters<=maxIters):
            xOutput[:,:]=xTest
            aResid=((MarbleCollision(marbleOutputSM))/marbleMass + np.tile(agrav,(marbleInputSM.shape[1],1)).T)-aFinal
            vOutput[:,:] = vOutput+aResid/2*dT
            xTest=xOutput+(dT*dT)/2*aResid/2
            iters+=1
            if(iters>maxIters):
                print("Warning! Predictor-corrector unable to converge! Select another integration method.")
                
    else:
        raise ValueError("Incorrect numerical integration scheme selected!")
    
    return marbleOutputSM
