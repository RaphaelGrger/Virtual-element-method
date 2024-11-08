import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from matplotlib.tri import Triangulation

import read_mesh
import vem

################### Variables ###################

fname = 'voronoi'

def plot_solution(vertices, elements, U, axis):
    # Crée une triangulation à partir des éléments
    x, y = vertices[:, 0], vertices[:, 1]
    triangulation = Triangulation(x, y, elements)
    
    # Tracé de la solution
    axis.figure(figsize=(8, 6))
    axis.tricontourf(triangulation, U, levels=100, cmap="viridis")
    axis.colorbar(label="Solution u(x, y)")
    axis.scatter(x, y, color='k', s=1)  # Ajouter les points des sommets pour référence
    axis.title("Solution de l'équation de Poisson")
    axis.xlabel("x")
    axis.ylabel("y")
    axis.show()


if __name__ == '__main__':
    
    Nelements, elements, points = read_mesh.read_meshes(fname)
    
    meshes = read_mesh.extract_meshes(elements,points)
    middles,normals = read_mesh.mid_and_normals(meshes)

    U, vertices, elements = vem.vem(fname, vem.rhs_function, vem.boundary_condition)

    print("Somme des aires : {}".format(np.sum([read_mesh.area(poly) for poly in meshes])))


    fig = plt.figure()

    ax1 = fig.add_subplot(221) #meshes
    read_mesh.draw_meshes(meshes,ax1)
    
    ax2 = fig.add_subplot(222) #normals
    read_mesh.draw_normals(middles,normals,ax2)
    
    ax3 = fig.add_subplot(223)
    plot_solution(vertices, elements, U,ax3)

    plt.show()