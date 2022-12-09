import numpy as np
import text_image_edited as text_image

class geometry:
    
    def __init__(self, Lx=1, Ly=1, Lz=.05):
        
        self.Lx, self.Ly, self.Lz = Lx, Ly, Lz

class stamping:
    
    def __init__(self, Tstamp=800, Tinitial=100, text='', fontsize=4, nx1=303, ny1=303, forma='', nx2=101, ny2=101, dx=0.01, dy=0.01, T0=np.zeros([101, 101])):
        
        self.Tstamp = Tstamp
        self.Ti = Tinitial
        
        self.T0  = np.ones([nx2,ny2]) * self.Ti
        self.T0 += text_image.InitialCondition.gera_forma(self, forma, nx2, ny2, dx, dy, Tstamp, T0) * self.Tstamp
        #self.T0  = np.ones([nx1,ny1]) * self.Ti
        #self.T0 += text_image.InitialCondition.gera_caracteres(self, text, nx1, ny1, fontsize) * self.Tstamp

class convection:
    
    def __init__(self, Trefr=0):
        
        self.Trefr = Trefr
        
class mesh:
    
    def __init__(self, nx=101, ny=101):
        
        self.nx, self.ny = nx, ny

class DiffFin:
    
    def __init__(self, geometry, material, fluid, stamping, convection, mesh=mesh(), dt=.01):
        
        self.geometry  = geometry
        self.material  = material
        self.fluid = fluid
        self.stamping  = stamping
        self.convection = convection
        self.mesh       = mesh

        dx = geometry.Lx / (mesh.nx - 1)
        dy = geometry.Ly / (mesh.ny - 1)
        dx2 = dx ** 2
        dy2 = dy ** 2
        self.dt = dt
        
        self.Fo = material.a * dt / geometry.Lz ** 2
        self.Bi = fluid.h * geometry.Lz / material.k
        
        self.Fox = material.a * dt / dx2
        self.Foy = material.a * dt / dy2
                
        self.T = np.copy(stamping.T0)
        
        # variável auxiliar para CC periódicas
        shx, shy = self.T.shape
        self.v = np.zeros((shx+2, shy+2))

    def evolve(self):
        
        ### condições de contorno periódicas
        self.v[1:-1, 1:-1] = self.T[:, :]
        self.v[0, 1:-1] = self.T[-1, :]
        self.v[-1, 1:-1] = self.T[0, :]
        self.v[1:-1, 0] = self.T[:, -1]
        self.v[1:-1, -1] = self.T[:, 0]
        
        # diferenças finitas
        self.v[1:-1, 1:-1] += \
            + self.Fox * (self.v[2:, 1:-1] - 2 * self.v[1:-1, 1:-1] + self.v[:-2, 1:-1]) \
            + self.Foy * (self.v[1:-1, 2:] - 2 * self.v[1:-1, 1:-1] + self.v[1:-1, :-2]) \
            - self.Bi * self.Fo * (self.v[1:-1, 1:-1] - self.convection.Trefr)

        self.T = self.v[1:-1, 1:-1]
