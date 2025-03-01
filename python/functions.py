import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from matplotlib.tri import Triangulation
import matplotlib.pyplot as plt
import read_mesh as rm

def is_inside_circle(coord,r=0.1,centroid=[0.5,0.5]) :
    if (coord[0]-centroid[0])**2 + (coord[1]-centroid[1])**2 <= r**2 :
        return True
    return False

# Definitions of buildings
square_points = [(0.5011, 0.4182), (0.6391, 0.4182), (0.6391, 0.5976), (0.5011, 0.5976)]
square1 = [(0.3113,0.4031),(0.4330,0.4031),(0.4330,0.4969),(0.3113,0.4969)]
square2 = [(0.3852,0.4914),(0.4187,0.4914),(0.4187,0.5054),(0.3852,0.5054)]
square3 = [(0.2549,0.3072),(0.3677,0.3072),(0.3677,0.3981),(0.2549,0.3981)]
square4 = [(0.2908,0.3919),(0.3954,0.3919),(0.3954,0.4070),(0.2908,0.4070)]

def is_inside_bat(point,square):
    x, y = point
    x1, y1 = square[0]
    x2, y2 = square[1]
    x3, y3 = square[2]
    x4, y4 = square[3]
    
    # min and max of coords
    min_x = min(x1, x2, x3, x4)
    max_x = max(x1, x2, x3, x4)
    min_y = min(y1, y2, y3, y4)
    max_y = max(y1, y2, y3, y4)
    
    return min_x <= x <= max_x and min_y <= y <= max_y


''' 
# Buildings are boundary conditions
def is_on_boundary(coord,square = square_points,square1=square1,square2=square2,square3=square3,square4=square4,eps=10**-3) : 
    if is_inside_bat(coord,square) or is_inside_bat(coord,square1) or is_inside_bat(coord,square2) or is_inside_bat(coord,square3) or is_inside_bat(coord,square4) or (np.abs(coord[0]) <= eps) or (np.abs(coord[1])  <= eps) or (np.abs(coord[0]-1) <= eps) or (np.abs(coord[1]-1) <= eps) :
            return True
    return False 
'''


def is_on_boundary(coord,eps=10**-3) : # boundary conditions on the boundaries of the domain
    if (np.abs(coord[0]) <= eps) or (np.abs(coord[1])  <= eps) or (np.abs(coord[0]-1) <= eps) or (np.abs(coord[1]-1) <= eps) :
            return True
    return False 

'''  if the mesh is exact
def is_on_boundary(coord) :
    if coord[0]==0 or coord[0] == 1 or coord[1] == 0 or coord[1] == 1 :
        return True
    return False
'''
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
        
    return middles , normals

def error_L2(u, u_exacte, mesh):
    u = np.array(u)
    mesh = np.array(mesh)
    
    x_values = mesh[:, 0]
    y_values = mesh[:, 1]
    
    u_exacte_values = np.array([u_exacte([x, y]) for x, y in zip(x_values, y_values)])
    
    delta_x = np.mean(np.diff(x_values))
    delta_y = np.mean(np.diff(y_values))
    
    error_L2 = np.sqrt(np.sum((u - u_exacte_values)**2) * delta_x * delta_y)
    return error_L2
