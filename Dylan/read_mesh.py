import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix


################### Reading ###################

input_path = '../meshes/'
fname = 'voronoi' #'squares', 'triangles', 'voronoi', 'smoothed-voronoi', 'non-convex', 'urban'

#Read meshes
def read_meshes(fname) :

    #Read data from file
    file = np.load( fname+".npz" )
        
    #Assign points
    points = np.array(file["points"])
    npoints = len(points)

    #Setup element-to-points CSR adjacency matrix
    indices  = file["elements_indices"]
    indptr   = file["elements_indptr"]
    data     = np.ones(len(indices), dtype = int)
    elements = csr_matrix( (data, indices, indptr) )
    nelements = elements.shape[0]
    
    return points, nelements, elements

#Print point indices for every element
def print_points(nelements,elements) :
    for i in range(nelements):
        print( "element", i, "points", elements.getrow(i).indices )



# Affichage des points
def plot_points(points, fname):
    plt.figure()
    plt.scatter(points[:, 0], points[:, 1], c='blue', marker='o')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Points du maillage " + fname)
    plt.show()


# Affichag mesh
def plot_mesh(points, elements, fname):
    plt.figure()
    plt.scatter(points[:, 0], points[:, 1], color='blue', s=10, label="Points")
    
    for i in range(elements.shape[0]):
        element_indices = elements.getrow(i).indices
        element_points = points[element_indices]
        
        # Fermer le polygone en ajoutant le premier point à la fin
        polygon = np.vstack([element_points, element_points[0]])
        
        # Tracer le polygone
        plt.plot(polygon[:, 0], polygon[:, 1], 'k-', linewidth=0.5)
    
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Maillage " + fname)
    plt.show()

points, nelements, elements = read_meshes(fname)
#print_points(nelements,elements)
plot_points(points, fname)
plot_mesh(points, elements, fname)