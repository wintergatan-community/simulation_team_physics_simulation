# -*- coding: utf-8 -*-
"""
Object Oriented-Programmed Marbles class.

@author: Vsk
Created: August 4 2021

"""
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

# TODO #10 
# TODO #11