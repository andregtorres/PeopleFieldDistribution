import numpy as np
from thread import allocate_lock
from multiprocessing import Lock

def cm(cm): #converts cm to pixels
    return int( cm /gridResol)

dimensions  = [500,350]     #dimentions for box in cm
gridResol   = 1.           #grid resolution in cm/pixel
Nx      = int((dimensions[0])/gridResol) #number of grid points
Ny      = int((dimensions[1])/gridResol) #number of grid points
Npoints     = Nx*Ny
door= (0,Ny/2., cm(72))
a=8000.

grid    = np.zeros(Npoints, dtype=np.float64 ).reshape(Nx, Ny)
doorField = np.zeros(Npoints, dtype=np.float64 ).reshape(Nx, Ny)
locked  = np.zeros(Npoints, dtype=np.bool ).reshape(Nx, Ny)
gradx   = np.zeros(Npoints, dtype=np.float64 ).reshape(Nx, Ny)
grady   = np.zeros(Npoints, dtype=np.float64 ).reshape(Nx, Ny)
time=0
exitAreaR   = 40 #cm
dt          = 1 #s
radius      = 18. #cm
JBuffer=[]
rhoBuffer=[]
velocityBuffer=[]

#THREADING
activeThreads=0
lockPrint = Lock()
lockGrid = Lock()
