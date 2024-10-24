import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix


################### Reading data ###################

input_path = '../meshes/'
fname = 'voronoi' #'squares', 'triangles', 'voronoi', 'smoothed-voronoi', 'non-convex', 'urban'

#Read meshes
def read_meshes(fname) :

    #Read data from file
    file = np.load( input_path+fname+".npz" )
        
    #Assign points
    points = np.array(file["points"])
    npoints = len(points)

    #Setup element-to-points CSR adjacency matrix
    indices  = file["elements_indices"]
    indptr   = file["elements_indptr"]
    data     = np.ones(len(indices), dtype = int)
    elements = csr_matrix( (data, indices, indptr) )
    nelements = elements.shape[0]
    
    return nelements, elements, points

#Print point indices for every element
def print_points(nelements,elements) :

    for i in range(nelements):
        print( "element", i, "points", elements.getrow(i).indices )


################### Mesh drawing ###################

def draw_figure(V) :

    X = [v[0] for v in V] + [V[0][0]]
    Y = [v[1] for v in V] + [V[0][1]]
    plt.plot(X,Y,'-',color='k',linewidth=0.5)
    pass

def draw_meshes(elements, points):
    
    indptr = elements.indptr  
    indices = elements.indices  

    for i in range(len(indptr) - 1):  
        first_idx = indptr[i]
        last_idx = indptr[i + 1]

        element_points_indices = indices[first_idx:last_idx]
        V = [points[j] for j in element_points_indices]
        
        draw_figure(V)
    pass


#### Operations ####

#Calcul area 1/2(u ∧ v)
def area(x,y) :
    
    return (1/2)* np.cross(x,y)

def middles_segments(elements,points) : #return every middles of segments
    
    indptr = elements.indptr  
    indices = elements.indices  
    middles = []

    for i in range(len(indptr) - 1):  
        first_idx = indptr[i]
        last_idx = indptr[i + 1]

        element_points_indices = indices[first_idx:last_idx]
        V = [points[j] for j in element_points_indices]
        middles.append([(V[i]+ V[i+1])/2 for i in range(len(V)-1)])
        
    return middles

def normal_vect(a,b) : #Unit normal vector of [AB]

    return np.array( [b[1] - a[1], a[0] - b[0] ])/np.linalg.norm(b-a)

def normal_vector(elements, points) : #Return all normals vectors 
    
    indptr = elements.indptr  
    indices = elements.indices  
    normals = []

    for i in range(len(indptr) - 1):  
        first_idx = indptr[i]
        last_idx = indptr[i + 1]

        element_points_indices = indices[first_idx:last_idx]
        V = [points[j] for j in element_points_indices]
        normals.append([normal_vect(V[i],V[i+1]) for i in range(len(V)-1)])
        
    return normals