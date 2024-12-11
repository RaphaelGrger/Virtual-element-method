import os
import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix

import functions as fct
import read_mesh as rm
import vem

################### Variables ###################

fname = 'triangles'  # 'squares', 'triangles', 'voronoi', 'smoothed-voronoi', 'non-convex', 'urban'
input_path = './meshes/'
output_dir = './python/res'

def test(x, y):
    return x**2 + y**2

def boundary_test(coord):
    return coord[:, 0] + coord[:, 1] 

if __name__ == '__main__':
    
    Nelements, elements, vertices = rm.read_meshes(fname)
    u, verts = vem.vem(fname, vem.rhs, vem.square_boundary_condition)
    
    V = rm.extract_meshes(elements, verts)

    # Création du plot avec un seul axe pour superposer les deux graphiques
    fig, ax = plt.subplots(figsize=(10, 5))  # Un seul axe

    # Dessin du maillage sur l'axe
    rm.draw_meshes(V, ax)

    # Superposition de la solution sur le même axe
    vem.plot_solution(vertices, u, ax)

    # Sauvegarde du plot combiné
    solution_plot_path = os.path.join(output_dir, f'{fname}.png')
    plt.savefig(solution_plot_path)
    plt.show()

    # Vérification des conditions aux frontières
    bords = [i for i in range(len(vertices)) if fct.is_on_boundary(vertices[i])]
    print(np.max(np.abs(vem.square_boundary_condition(vertices[bords]) - u[bords])))
