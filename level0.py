import numpy as np
from thread import allocate_lock

dimensions  = [1000,1000]     #dimentions for box
door = dimensions[0]/10.  #dimentions for door
gridResol   = 1.           #grid resolution
Nx      = int((dimensions[0])/gridResol) #number of grid points
Ny      = int((dimensions[1])/gridResol) #number of grid points
Npoints     = Nx*Ny
grid    = np.zeros(Npoints, dtype=np.float64 ).reshape(Nx, Ny)
newGrid = np.zeros(Npoints, dtype=np.float64 ).reshape(Nx, Ny)
locked  = np.zeros(Npoints, dtype=np.bool ).reshape(Nx, Ny)
gradx   = np.zeros(Npoints, dtype=np.float64 ).reshape(Nx, Ny)
grady   = np.zeros(Npoints, dtype=np.float64 ).reshape(Nx, Ny)
time=0

#THREADING
activeThreads=0
lockCounter = allocate_lock()
lockGrid = allocate_lock()
