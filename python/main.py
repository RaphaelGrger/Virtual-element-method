import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix

import functions as fct
import read_mesh as rm
import vem


fname =  'urban'
input_path = '../meshes/'
    
def test(x,y) :
    return x**2+y**2

def boundary_test(coord):
    return coord[:,0] + coord[:,1] 

if __name__ == '__main__':
    
    Nelements, elements, vertices = rm.read_meshes(fname)
    u,verts, diam,K = vem.vem(fname,vem.rhs,vem.square_boundary_condition)

    V = rm.extract_meshes(elements,verts)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))         
    rm.draw_meshes(V,ax1)
            
    vem.plot_solution(V,vertices,u,ax2)
    plt.show()
