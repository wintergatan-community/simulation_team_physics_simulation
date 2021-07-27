# -*- coding: utf-8 -*-
"""
Object Oriented-Programmed physics example file.

Author: Kyle Williams
Created: 7-24-2021

"""
from dataclasses import dataclass

import numpy as np


@dataclass
class MaterialInfo:
    """This class holds all static data relating to a material being used"""
    density: float
    elastic_modulus: float
    poisson_ratio: float


class MarbleInfo:
    """This class holds all static data relating to the set of marbles"""
    def __init__(self, n_marbles: int, radius: float, material_info: MaterialInfo):
        self.radii = radius*np.ones(n_marbles)
        self.densities = material_info.density * np.ones(n_marbles)
        self.volumes = np.power(self.radii, 3)*4/3*np.pi
        self.masses = self.densities * self.volumes
        self.elasticities = material_info.elastic_modulus * np.ones(n_marbles)
        self.material_info = material_info
        self.size = n_marbles

    def __len__(self):
        return self.size


materialInfo = MaterialInfo(density=7.81, elastic_modulus=205000, poisson_ratio=0.30)

grav_accel = np.array([0, -9.81*1000, 0])  # NOTE: LENGTH UNIT IS MM!!!!


class MMXPhysics:
    def __init__(self, pos, vel, marble_info):
        self.pos = pos
        self.vel = vel
        self.marbles = marble_info

    def collision_force(self, positions):
        return np.zeros(positions.shape)

    # state = [x | y | z | vx | vy | vz ]
    def derivative(self, state):
        pos, vel = state.reshape(2, 3*len(self.marbles))

        dvdt = np.tile(grav_accel, (len(self.marbles), 1)) + self.collision_force(pos)/self.marbles.masses
        dxdt = vel

        return np.stack((dxdt, dvdt))


    def solve(self, dt):
        """Returns the times and positions of the ode solution
            use scipy ODE solver
        """
        pass

# def pairwise_add(array1, array2):
#     nMarbles = len(array1)
#     return np.tile(array1, (nMarbles, 1)) + np.tile(array2, (nMarbles, 1)).T
#
#
# #A function to perform marble-to-marble collision detection
# def force_collision(state, marbles):
#
#     dx = pairwise_add(state[0, :], -state[0, :])
#     dy = pairwise_add(state[1, :], -state[1, :])
#     dz = pairwise_add(state[2, :], -state[2, :])
#
#     disp_mag = np.linalg.norm([dx, dy, dz])
#     sum_radii = pairwise_add(marbles.radii, marbles.radii)
#     collision_depth = np.maximum(sum_radii-disp_mag, 0)  # Collision depth cannot be smaller than zero, hence "max"
#
#     # Set up effective radius and elastic modulus for hertzian contact calc:
#     radii_eff = 1/pairwise_add(1/marbles.radii, 1/marbles.radii)
#     elasticity_eff = 1/pairwise_add(1/marbles.elasticity, 1/marbles.elasticity)
#
#     #Use sphere-on-sphere contact equations to determine force at depth:
#     force_mag = (4.0/3.0)*np.abs(elasticity_eff)*np.sqrt(np.power(collision_depth, 3)*radii_eff)
#     np.fill_diagonal(force_mag, 0)  # Marbles don't exert force on themselves
#
#     #Calculate XYZ direction and turn into forces:
#     np.fill_diagonal(disp_mag, 1) #Note the diagonals are zeros, we have to fix this
#
#     fx = np.sum(force_mag*dx/disp_mag, axis=1)
#     fy = np.sum(force_mag*dy/disp_mag, axis=1)
#     fz = np.sum(force_mag*dz/disp_mag, axis=1)
#     return np.stack((fx, fy, fz))
#
# #A function to update marble positions using physics calculations.
# #
# # marbleInputSM is [x,y,z,vx,vy,vz,radius,materialIndex]
# def PhysicsCalc (marbleInputSM,dT):
#
#     #Set up some references to input data:
#     xInput=marbleInputSM[0:3,:]
#     vInput=marbleInputSM[3:6,:]
#
#     #Make a copy of the input array for output
#     marbleOutputSM=np.copy(marbleInputSM)
#     xOutput=marbleOutputSM[0:3,:]
#     vOutput=marbleOutputSM[3:6,:]
#
#     #Calculate mass:
#     marbleDensity=materialInfo[marbleInputSM[7,:].astype(int),0]
#     marbleVolume=np.power(marbleInputSM[6,:],3)*4/3*np.pi
#     marbleMass=marbleDensity/marbleVolume
#
#     #Calculate force on the marbles due to collisions:
#     fMarbleMarble=MarbleCollision(marbleInputSM)
#
#     #Calculate acceleration due to collisions and gravity:
#     aInitial=fMarbleMarble/marbleMass + np.tile(agrav,(marbleInputSM.shape[1],1)).T
#
#     #Recalculate velocity and position. Note the referencing notation to modify the original values.
#     if (updateScheme==0):
#         vOutput[:,:]=vInput+aInitial*dT
#         xOutput[:,:]=xInput+(vInput+vOutput)/2*dT
#     elif (updateScheme==1):
#         xOutput[:,:]=xInput+vInput*dT+(dT*dT)/2*aInitial
#         aFinal=(MarbleCollision(marbleOutputSM))/marbleMass + np.tile(agrav,(marbleInputSM.shape[1],1)).T
#         vOutput[:,:]=vInput+(aInitial+aFinal)/2*dT
#     elif (updateScheme==2):
#         xOutput[:,:]=xInput+vInput*dT+(dT*dT)/2*aInitial
#         aFinal=(MarbleCollision(marbleOutputSM))/marbleMass + np.tile(agrav,(marbleInputSM.shape[1],1)).T
#         vOutput[:,:]=vInput+(aInitial+aFinal)/2*dT
#         xTest=xInput+vInput*dT+(dT*dT)/2*(aInitial+aFinal)/2
#         iters=0
#         while(np.max((xTest-xOutput)/marbleInputSM[6,:])>epsilon and iters<=maxIters):
#             xOutput[:,:]=xTest
#             aResid=((MarbleCollision(marbleOutputSM))/marbleMass + np.tile(agrav,(marbleInputSM.shape[1],1)).T)-aFinal
#             vOutput[:,:] = vOutput+aResid/2*dT
#             xTest=xOutput+(dT*dT)/2*aResid/2
#             iters+=1
#             if(iters>maxIters):
#                 print("Warning! Predictor-corrector unable to converge! Select another integration method.")
#
#     else:
#         raise ValueError("Incorrect numerical integration scheme selected!")
#
#     return marbleOutputSM
