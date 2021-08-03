# -*- coding: utf-8 -*-
"""
Object Oriented-Programmed physics example file.

Author: Kyle Williams
Created: 7-24-2021

"""
try:
    from dataclasses import dataclass

    import numpy as np
    from scipy.integrate import solve_ivp
except ModuleNotFoundError:
    print("ERROR: Module not found. Please install the numpy and wave package before running.")
    raise SystemExit

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


grav_accel = np.array([0, 0, -9.81*1000])  # NOTE: LENGTH UNIT IS MM!!!!


class MMXPhysics:
    def __init__(self, pos, vel, marble_info):
        self.pos = pos
        self.vel = vel
        self.marbles = marble_info

        # Cache effective radius and elastic modulus for hertzian contact calc:
        self.sum_radii = pairwise_add(self.marbles.radii, self.marbles.radii)
        self.radii_eff = 1/pairwise_add(1/self.marbles.radii, 1/self.marbles.radii)
        self.elasticity_eff = 1/pairwise_add(1/self.marbles.elasticity, 1/self.marbles.elasticity)

    def collision_force(self, positions):
        dx = pairwise_add(positions[0, :], -positions[0, :])
        dy = pairwise_add(positions[1, :], -positions[1, :])
        dz = pairwise_add(positions[2, :], -positions[2, :])

        # Calculate XYZ direction and turn into forces:
        disp_mag = np.sqrt(dx*dx + dy*dy + dz*dz)
        np.fill_diagonal(disp_mag, 1)   # Note the diagonals are zeros, avoid division by zero

        # Use sphere-on-sphere contact equations to determine force at depth:
        collision_depth = np.maximum(self.sum_radii-disp_mag, 0)  # Collision depth cannot be smaller than zero
        force_mag = (4.0/3.0)*np.abs(self.elasticity_eff)*np.sqrt(np.power(collision_depth, 3)*self.radii_eff)
        np.fill_diagonal(force_mag, 0)  # Marbles don't exert force on themselves

        fx = np.sum(force_mag*dx/disp_mag, axis=1)
        fy = np.sum(force_mag*dy/disp_mag, axis=1)
        fz = np.sum(force_mag*dz/disp_mag, axis=1)
        return np.stack((fx, fy, fz))

    def derivative(self, _, state):
        """
            compute rhs for d/dt = F(t, X),
            first argument would be time (not used)
            state = [x | y | z | vx | vy | vz ]
            return value is same shape as state 1 x 6*N
        """

        # Unpack shape, pos and vel are 3 x N arrays
        pos, vel = np.reshape(state, (2, 3, -1))

        # Compute accelerations
        accel_g = np.tile(grav_accel, (len(self.marbles), 1)).transpose()
        accel_mm = self.collision_force(pos)/self.marbles.masses

        # ODE System
        dxdt = vel
        dvdt = accel_g + accel_mm

        # pack/flatten to proper shape
        return np.stack((dxdt, dvdt)).flatten()

    def solve(self, t_end):
        """Returns the times and positions of the ode solution
            use scipy ODE solver
        """
        y0 = np.concatenate((self.pos.flatten(), self.vel.flatten()))
        t_vals = np.arange(0, t_end, 1e-2)
        return solve_ivp(self.derivative, (0, t_end), y0, t_eval=t_vals,
                         method='Radau', max_step=1e-4)


if __name__ == "__main__":
    n_marbles = 49
    radius = 10
    height = 100
    material_info = MaterialInfo(density=7.81, elastic_modulus=2050, poisson_ratio=0.30)
    marbles = MarbleInfo(n_marbles=n_marbles, radius=radius, material_info=material_info)

    # Create 5 x 4 grid of marbles, spaced to they don't initially collide
    x = np.arange(0, 0.5*radius*7, 0.5*radius)
    y = np.arange(0, 0.5*radius*7, 0.5*radius)
    x, y = np.meshgrid(x, y)
    x = x.flatten()
    y = y.flatten()
    z = height*np.ones(y.shape)
    positions = np.array([x, y, z])

    # give random horizontal velocity with 0 vertical component
    velocities = 300*(np.random.random((3, n_marbles)) - 0.5)
    velocities[2, :] = np.zeros(n_marbles)

    # Initialize Simulation
    simulation = MMXPhysics(positions, velocities, marbles)

    # Solve
    solution = simulation.solve(0.3)

    # Visualise the results.
    result = np.reshape(solution.y, (6, n_marbles, -1))
    x, y, z = result[0:3, :, :]
    
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        print("ERROR: Module not found. Please install the numpy and wave package before running.")
        raise SystemExit
    
    ax = plt.figure().add_subplot(projection='3d')
    for i in range(n_marbles):
        ax.plot(x[i], y[i], z[i])
    plt.show()
