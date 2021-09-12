# -*- coding: utf-8 -*-
"""
Object Oriented-Programmed physics example file.

Author: Kyle Williams
Created: 7-24-2021

"""
try:
    from dataclasses import dataclass
    import time
    import numpy as np
    from scipy.integrate import solve_ivp
except ModuleNotFoundError:
    print("ERROR: Module not found. Please install the numpy and scipy package before running.")
#    raise SystemExit

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
        self.sqrt_radii_eff = np.sqrt(1/pairwise_add(1/self.marbles.radii, 1/self.marbles.radii))
        self.elasticity_eff = 1/pairwise_add(1/self.marbles.elasticities, 1/self.marbles.elasticities)
        
        #Cache a masking array for not-self marbles
        self.n_marbles=pos.shape[1]
        self.not_self_marble = 1-np.eye(self.n_marbles)

    def collision_force(self, positions):
        dx = pairwise_add(positions[0, :], -positions[0, :])
        dy = pairwise_add(positions[1, :], -positions[1, :])
        dz = pairwise_add(positions[2, :], -positions[2, :])

        # Calculate XYZ direction and turn into forces:
        disp_mag = np.sqrt(dx*dx + dy*dy + dz*dz)
        np.fill_diagonal(disp_mag, 1)   # Note the diagonals are zeros, avoid division by zero

        # Use sphere-on-sphere contact equations to determine force at depth:
        collision_depth = np.maximum(self.sum_radii-disp_mag, 0)  # Collision depth cannot be smaller than zero
        force_mag = (4.0/3.0)*np.abs(self.elasticity_eff)*self.sqrt_radii_eff*collision_depth*np.sqrt(collision_depth)
        np.fill_diagonal(force_mag, 0)  # Marbles don't exert force on themselves

        fx = np.sum(-force_mag*dx/disp_mag, axis=1)
        fy = np.sum(-force_mag*dy/disp_mag, axis=1)
        fz = np.sum(-force_mag*dz/disp_mag, axis=1)
        return np.stack((fx, fy, fz))
    
    def masked_collision_force(self, positions):
        dx = pairwise_add(positions[0, :], -positions[0, :])
        dy = pairwise_add(positions[1, :], -positions[1, :])
        dz = pairwise_add(positions[2, :], -positions[2, :])
        
        # Use the maximum single-dimension distance as a lower bound for separation, make a mask for further operations:
        sumdim = np.abs(dx)+np.abs(dy)+np.abs(dz)
        dm= np.logical_and(sumdim<=self.sum_radii, self.not_self_marble)
        
        
        # Calculate XYZ direction, but only for relevant dims. For non-colliding dims, just default to 1 to avoid NaN:
        disp_mag = np.ones(dx.shape)
        disp_mag[dm] = np.sqrt(dx[dm]*dx[dm] + dy[dm]*dy[dm] + dz[dm]*dz[dm])
        #np.fill_diagonal(disp_mag, 1)   # Note the diagonals are zeros, avoid division by zero
        
        

        # Use sphere-on-sphere contact equations to determine force at depth:
        collision_depth = np.maximum(self.sum_radii[dm]-disp_mag[dm], 0)  # Collision depth cannot be smaller than zero
        force_mag=np.zeros(dx.shape)
        force_mag[dm] = (4.0/3.0)*np.abs(self.elasticity_eff[dm])*self.sqrt_radii_eff[dm]*collision_depth*np.sqrt(collision_depth)
        #np.fill_diagonal(force_mag, 0)  # Marbles don't exert force on themselves
        
        
        fx = np.sum(-force_mag*dx/disp_mag, axis=1)
        fy = np.sum(-force_mag*dy/disp_mag, axis=1)
        fz = np.sum(-force_mag*dz/disp_mag, axis=1)
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
        t_vals = np.arange(0, t_end, 4e-3)
        return solve_ivp(self.derivative, (0, t_end), y0, t_eval=t_vals,
                         method='Radau')


#Function to run a test problem. Returns a tuple of x, y, and z position arrays, as well as radius and number of timesteps.
def run_test_problem(t_end=0.4,marblelayout=[4,4,1]):
    n_marbles = np.prod(marblelayout)
    radius = 10
    height = 100
    material_info = MaterialInfo(density=.00781, elastic_modulus=205000, poisson_ratio=0.30)
    marbles = MarbleInfo(n_marbles=n_marbles, radius=radius, material_info=material_info)

    # Create X x Y grid of marbles, spaced so they don't initially collide
    x = np.arange(0, 2.5*radius*marblelayout[0], 2.5*radius)
    y = np.arange(0, 2.5*radius*marblelayout[1], 2.5*radius)
    x, y = np.meshgrid(x, y)
    x = x.flatten()
    y = y.flatten()
    z = height*np.ones(y.shape)
    positions = np.array([x, y, z])

    # give random horizontal velocity with 0 vertical component
    velocities = 600*(np.random.random((3, n_marbles)) - 0.5)
    velocities[2, :] = np.zeros(n_marbles)

    # Initialize Simulation
    tsolver=time.time()
    simulation = MMXPhysics(positions, velocities, marbles)
    
    # Solve
    solution = simulation.solve(t_end)
    print("Solver time: ",time.time()-tsolver)
    
    # Visualise the results.
    result = np.reshape(solution.y, (6, n_marbles, -1))
    x, y, z = result[0:3, :, :]
    
    nsteps=result.shape[2]
    
    return (x,y,z,radius,nsteps)

if __name__ == "__main__":
    animation=True
    tstart=time.time()
    marblelayout=[4,4,1]

    (x,y,z,radius,nsteps)=run_test_problem(t_end=0.4,marblelayout=marblelayout)
    n_marbles = np.prod(marblelayout)
    print("{",x,"}{",y,"}{",z,"}{",radius,"}{",nsteps,"}{",n_marbles,"}")
    
    if animation:
        try:
            import matplotlib.pyplot as plt
            import matplotlib.animation as animation
        except ModuleNotFoundError:
            print("ERROR: Module not found. Please install matplotlib.")
            raise SystemExit
        
        #Plotting things
        u = np.linspace(0, 2 * np.pi, 8)
        v = np.linspace(0, np.pi, 8)
        px = radius * np.outer(np.cos(u), np.sin(v))
        py = radius * np.outer(np.sin(u), np.sin(v))
        pz = radius * np.outer(np.ones(np.size(u)), np.cos(v))
        
        def update_spheres(num, data, surfs):
            for i in range(n_marbles):
                surfs[i].remove()
                surfs[i] = ax.plot_surface(px+x[i,num], py+y[i,num], pz+z[i,num], color='grey')
        
        # Attaching 3D axis to the figure
        fig = plt.figure()
        ax = fig.add_subplot(projection="3d")
        
        spheres=[]
        for i in range(n_marbles):
            spheres.append(ax.plot_surface(px+x[i,0], py+y[i,0], pz+z[i,0], color='grey'))

        # Setting the axes properties
        ax.set_xlim3d([-50, 150])
        ax.set_xlabel('X')
        
        ax.set_ylim3d([-50, 150])
        ax.set_ylabel('Y')
        
        ax.set_zlim3d([-100, 100])
        ax.set_zlabel('Z')
        
        ax.set_title('3D Test')
        
        # Creating the Animation object
        line_ani = animation.FuncAnimation(fig, update_spheres, nsteps, fargs=([x,y,z], spheres), interval=5)
        
        plt.show()
    else:
        try:
            import matplotlib.pyplot as plt
        except ModuleNotFoundError:
            print("ERROR: Module not found. Please install matplotlib.")
            raise SystemExit
        
        ax = plt.figure().add_subplot(projection='3d')
        for i in range(n_marbles):
            ax.plot(x[i], y[i], z[i])
        plt.show()
        print("Total runtime: ",time.time()-tstart)
