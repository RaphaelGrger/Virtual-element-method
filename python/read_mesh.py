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

def extract_meshes(elements,points) :
    indptr = elements.indptr
    indices = elements.indices
    
    L = [] #list of polygons

    for i in range(len(indptr) - 1):  
        first_idx = indptr[i]
        last_idx = indptr[i + 1]

        element_points_indices = indices[first_idx:last_idx]
        V = [points[j] for j in element_points_indices]
        
        L.append(V)
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

################### Properties ###################


###### Area
def isobarycenter(V) :
    n = len(V[0])
    bary = [0] * n
    for v in V :
        for i in range(n) :
            bary[i] += v[i]
    return np.array([x / len(V) for x in bary])

def area(poly) :
    isobary = isobarycenter(poly)
    area_poly = 0
    for i in range(len(poly)) :
        AG = isobary - poly[i]
        BG = isobary - poly[(i+1) % len(poly)]
        area_poly += 0.5 * np.abs(np.cross(AG,BG))
        
    return area_poly

###### Middles and normals

def normal_vect(a,b) : #Unit normal vector of [AB]
    return np.array( [b[1] - a[1], a[0] - b[0] ])/np.linalg.norm(b-a)

def mid_and_normals(L) : 
    middles = []
    normals = []
    for poly in L :
        middle_points = [(poly[i] + poly[(i + 1) % len(poly)]) / 2 for i in range(len(poly))]
        normal = [normal_vect(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))]
        for m,n in zip(middle_points,normal) :
            middles.append(m)
            normals.append(n)
        #middles.append(middle_points)
        #normals.append(normal)

    return middles , normals


def normal_vector(L) : #Return all normals vectors 
    normals = []
    for poly in L :  
        normals_vect = [normal_vect(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly))]
        for nv in normals_vect :
            normals.append(nv)    
    return normals