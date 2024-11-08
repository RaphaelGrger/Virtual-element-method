import numpy as np

from read_mesh import isobarycenter
from read_mesh import area

def rhs_function(x, y):
    return 15 * np.sin(np.pi * x) * np.sin(np.pi * y)
def boundary_condition(x, y): 
    return x * y * np.sin(np.pi * x)

def polynomial_basis_matrix(vertices, isobarycenter, h):
    basis = np.zeros((3, vertices.shape[0]))
    for i, (x, y) in enumerate(vertices):
        basis[0, i] = 1
        basis[1, i] = (x - isobarycenter[0]) / h
        basis[2, i] = (y - isobarycenter[1]) / h
    return basis

def projection_ritz(vertices,basis) :
    G = np.dot(basis,basis.T)
    print(G)
    pass

def local_matrix(vertices,isobarycenter,area,h,rhs_funct) :
    
    pass