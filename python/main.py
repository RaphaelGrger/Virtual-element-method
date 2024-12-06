import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix

import functions as fct
import read_mesh as rm
import vem

################### Variables ###################

fname = 'voronoi'
input_path = '../meshes/'
    
def test(x,y) :
    return x**2+y**2

def boundary_test(coord):
    return coord[:,0] + coord[:,1] 

if __name__ == '__main__':
    
    Nelements, elements, vertices = rm.read_meshes(fname)
    u,verts = vem.vem(fname,vem.rhs,vem.square_boundary_condition)
    
    V = rm.extract_meshes(elements,verts)

    #middles,normals = read_mesh.mid_and_normals(meshes)
    #print("Somme des aires : {}".format(np.sum([fct.area(poly) for poly in V])))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    rm.draw_meshes(V,ax1)

    #vem.plot_solution(vertices,test(vertices[:,0],vertices[:,1]),ax2)
    
    vem.plot_solution(vertices,u,ax2)
    plt.show()

    bords = [i for i in range(len(vertices)) if fct.is_on_boundary(vertices[i])]
    print(np.max(np.abs(vem.square_boundary_condition(vertices[bords]) - u[bords])))
