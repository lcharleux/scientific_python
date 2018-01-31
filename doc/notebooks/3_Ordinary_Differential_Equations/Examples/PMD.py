################################################################################
# POINT MASS DYNAMICS
# Author: Ludovic Charleux, ludovic.charleux@univ-smb.fr, 01/2018 
################################################################################
import numpy as np
from scipy import integrate, optimize


def distances(P):
    """
    Return vectorials distance, scalar distance and normalized directions.
    """
    X, Y = P.T
    dX = X - X[:, np.newaxis]
    dY = Y - Y[:, np.newaxis]
    D = np.array([dX, dY]).swapaxes(0,2)
    R = np.sqrt(D[:,:,0]**2 + D[:,:,1]**2)
    U = np.divide(
            D, 
            R[:,:,np.newaxis], 
            out = np.zeros_like(D), 
            where = R[:,:,np.newaxis] != 0.)
    return D, R, U

class PMD(object):
    """
    Point Mass Dynamics.
    """
    def __init__(self, m, P0, V0, force, nk = 1000):
        n = len(m)
        self.X = np.zeros([nk, 4 * n])
        self.X.fill(np.NAN)
        self.X[-1,    :2*n] = np.array(P0).flatten()
        self.X[-1, 2*n:   ] = np.array(V0).flatten()
        self.m = m
        force.set_master(self)
        self.force = force
        self.nk = nk
 
    def derivative(self, X, t):
        """
        ODE 
        """      
        m = self.m
        n = len(m)
        V = self.velocities()
        A = (self.force.master_force().T / m).T
        X2 = X.copy()
        X2[:2*n ] = V.flatten()
        X2[ 2*n:] = A.flatten()
        return X2       
    
    def positions(self):
        """
        Returns the current positions.
        """
        n = len(self.m)
        return self.X[-1, :2 * n ].reshape(n ,2)
  
    def velocities(self):
        """
        Returns the current velocities.
        """
        n = len(self.m)
        return  self.X[-1, 2 * n:].reshape(n ,2)
    
    def solve(self, dt, nt, **kwargs):
        """
        Solves the ODE.
        """
        time = np.linspace(0., dt, nt + 1)
        Xs = integrate.odeint( self.derivative, self.X[-1], time, **kwargs)
        nk = self.nk
        X = self.X
        X[:nk - nt] = X[nt:]
        X[-nt-1:] = Xs 
        self.X    = X
  
    def xy(self):
        """
        Returns the position of each mass.
        """
        P = self.positions()
        return P[:,0], P[:,1]
    
    def trail(self, i):
        """
        Returns the trail of each mass.
        """
        X = self.X
        return X[:, 2*i], X[:, 2*i+1 ]


class MetaForce:
    """
    A force metaclass to rule them all
    """
    def set_master(self, master):
        """
        Sets the PMD instance to work with
        """
        self.master = master
        
    def master_force(self):
        return self.force(P = self.master.positions(), V = self.master.velocities())    
