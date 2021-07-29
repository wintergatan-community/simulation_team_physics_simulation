# -*- coding: utf-8 -*-
"""
Object Oriented-Programmed physics example file.

Author: Kyle Williams
Created: 7-24-2021

"""
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp


def pairwise_add(array1, array2):
    shape = (len(array1), 1)
    return np.tile(array1, shape) + np.tile(array2, shape).T


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


grav_accel = np.array([0, -9.81*1000, 0])  # NOTE: LENGTH UNIT IS MM!!!!


class MMXPhysics:
    def __init__(self, pos, vel, marble_info):
        self.pos = pos
        self.vel = vel
        self.marbles = marble_info

    def collision_force(self, positions):
        dx = pairwise_add(positions[0, :], -positions[0, :])
        dy = pairwise_add(positions[1, :], -positions[1, :])
        dz = pairwise_add(positions[2, :], -positions[2, :])

        disp_mag = np.linalg.norm([dx, dy, dz])
        sum_radii = pairwise_add(self.marbles.radii, self.marbles.radii)
        collision_depth = np.maximum(sum_radii-disp_mag, 0)  # Collision depth cannot be smaller than zero, hence "max"

        # Set up effective radius and elastic modulus for hertzian contact calc:
        radii_eff = 1/pairwise_add(1/self.marbles.radii, 1/self.marbles.radii)
        elasticity_eff = 1/pairwise_add(1/self.marbles.elasticity, 1/self.marbles.elasticity)

        # Use sphere-on-sphere contact equations to determine force at depth:
        force_mag = (4.0/3.0)*np.abs(elasticity_eff)*np.sqrt(np.power(collision_depth, 3)*radii_eff)
        np.fill_diagonal(force_mag, 0)  # Marbles don't exert force on themselves

        # Calculate XYZ direction and turn into forces:
        np.fill_diagonal(disp_mag, 1)   # Note the diagonals are zeros, we have to fix this

        fx = np.sum(force_mag*dx/disp_mag, axis=1)
        fy = np.sum(force_mag*dy/disp_mag, axis=1)
        fz = np.sum(force_mag*dz/disp_mag, axis=1)
        return np.stack((fx, fy, fz))

    # state = [x | y | z | vx | vy | vz ]
    def derivative(self, _, state):     # first argument should be time (not used)
        pos, vel = state.reshape(2, 3*len(self.marbles))

        dvdt = np.tile(grav_accel.T, len(self.marbles)).flatten()  # + self.collision_force(pos)/self.marbles.masses
        dxdt = vel.flatten()
        return np.concatenate((dxdt, dvdt))

    def solve(self, t_end):
        """Returns the times and positions of the ode solution
            use scipy ODE solver
        """
        y0 = np.concatenate((self.pos.flatten(), self.vel.flatten()))
        return solve_ivp(self.derivative, (0, t_end), y0)


if __name__ == "__main__":
    n_marbles = 20
    radius = 10
    material_info = MaterialInfo(density=7.81, elastic_modulus=2050, poisson_ratio=0.30)
    marbles = MarbleInfo(n_marbles=n_marbles, radius=radius, material_info=material_info)

    x = np.array([3*radius*n for n in range(4)])
    y = np.array([3*radius*n for n in range(5)])
    x, y = np.meshgrid(x, y)
    x = x.flatten()
    y = y.flatten()
    z = 10*np.ones(y.shape)
    positions = np.array([x, y, z])

    velocities = np.random.random((3, n_marbles))
    velocities[2, :] = np.zeros(n_marbles)

    simulation = MMXPhysics(positions, velocities, marbles)
    simulation.solve(1)


