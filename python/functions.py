import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from matplotlib.tri import Triangulation
import matplotlib.pyplot as plt
import read_mesh as rm


def is_on_boundary(coord,eps=10**-3) : 
    if (np.abs(coord[0]) <= eps) or (np.abs(coord[1])  <= eps) or (np.abs(coord[0]-1) <= eps) or (np.abs(coord[1]-1) <= eps) :
        return True
    return False 

##### Propreties #####

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
