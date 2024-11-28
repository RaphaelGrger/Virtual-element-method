import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix


################### Reading data ###################

input_path = '../meshes/'
#Read meshes
def read_meshes(fname) :

    #Read data from file
    file = np.load( input_path+fname+".npz" )
        
    #Assign points
    points = np.array(file["points"])
    #Setup element-to-points CSR adjacency matrix
    indices  = file["elements_indices"]
    indptr   = file["elements_indptr"]
    data     = np.ones(len(indices), dtype = int)
    elements = csr_matrix( (data, indices, indptr) )
    Nelements = np.shape(elements[0])

    return Nelements, elements, points


def extract_meshes(elements,points) :
    indptr = elements.indptr
    indices = elements.indices
    
    L = [] #list of polygons

    for i in range(len(indptr) - 1):  
        first_idx = indptr[i]
        last_idx = indptr[i + 1]

        element_points_indices = indices[first_idx:last_idx]
        V = [points[j] for j in element_points_indices]
        

        L.append(np.array(V))
        
    return L

def csr_to_list(elements) :
    indptr = elements.indptr
    indices = elements.indices
    
    L = [] #list of polygons

    for i in range(len(indptr) - 1):  
        first_idx = indptr[i]
        last_idx = indptr[i + 1]

        element_points_indices = indices[first_idx:last_idx]
        V = [j for j in element_points_indices]
        
        L.append(np.array(V))
    return L

################### Mesh drawing ###################

def draw_figure(V,axis) :
    X = [v[0] for v in V] + [V[0][0]]
    Y = [v[1] for v in V] + [V[0][1]]
    axis.plot(X,Y,'-',color='k',linewidth=0.5)
    pass

def draw_meshes(V,axis):
    for v in V :    
        draw_figure(v,axis)
    pass

def draw_normals(midpoints,normals,axis=plt) :
    for mid,normal in zip(midpoints,normals):
        axis.quiver(mid[0], mid[1], normal[0], normal[1], color='0.2', scale=20)
    pass
