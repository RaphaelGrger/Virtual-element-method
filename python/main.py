import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix


import read_mesh


################### Variables ###################

fname = 'voronoi'


if __name__ == '__main__':
    
    Nelements, elements, points = read_mesh.read_meshes(fname)
    
    read_mesh.draw_meshes(elements,points)
    plt.show()

    pass