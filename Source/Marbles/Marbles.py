# -*- coding: utf-8 -*-
"""
Object Oriented-Programmed Marbles class.

@author: Vsk
Created: August 4 2021

"""
# Objective
#1. creating/spawning marbles into blender
# TODO #10 
#bpy.ops.surface.primitive_nurbs_surface_sphere_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
#2. applying custom material properties
#3. creating them as part of one particle system.
#4. translating them to numpy and back for our physics
# TODO #11
#rng = np.random.default_rng(seed=42) # create repeatable random numbers to use in MarbleSpawner

try:
    from dataclasses import dataclass
    
    import numpy as np
    from scipy.integrate import solve_ivp
except ModuleNotFoundError:
    print("ERROR: Module not found. Please install the numpy and scipy package before running.")
#    raise SystemExit

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