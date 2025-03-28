import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from scipy.sparse import lil_matrix, csr_matrix
from scipy.sparse.linalg import eigsh


import functions as fct
import read_mesh as rm

def exact_solution(coord):
    return 15*np.sin(np.pi * coord[0]) * np.sin(np.pi * coord[1])/(2*np.pi**2)

def square_boundary_condition(coord):
    return coord[:,0]*coord[:,1]*np.sin(np.pi*coord[:,0]) 

def rhs(coord):
    return 15*np.sin(np.pi*coord[0])*np.sin(np.pi*coord[1])

def pertubation(vertices) :
    for v in vertices :
        if not fct.is_on_boundary(v) :
            v[0] += 0.01*(np.random.rand(1)-0.5)
            v[1] += 0.01*(np.random.rand(1)-0.5)
    return vertices

def vem(fname, rhs, boundary_condition):
    _, elements, vertices = rm.read_meshes(fname)
    
    bords = [i for i in range(len(vertices)) if fct.is_on_boundary(vertices[i])]
    #vertices = pertubation(vertices)
    elements = rm.csr_to_list(elements)
    
    n_dofs = vertices.shape[0]
    n_polys = 3  # Degré des polynômes (linéaires : 1, x, y)
    
    K = lil_matrix((n_dofs, n_dofs))  # Matrice de rigidité
    F = np.zeros(n_dofs)  # Vecteur de force

    linear_polynomial = [[0,0],[1,0],[0,1]]
    
    maxdiam = 0

    for el in elements: # el est un polygone = liste de
        vert_ids = np.array(el)  # Indices des sommets du polygone el (index 0-based)
        verts = vertices[vert_ids,:]
        n_sides = len(vert_ids)
        
        # Géométrie
        area = fct.area(verts)
        centroid = fct.isobarycenter(verts)
        diameter = max(np.linalg.norm(verts[i] - verts[j]) for i in range(n_sides) for j in range(i + 1, n_sides))
        
        if maxdiam < diameter :
            maxdiam=diameter

        # Matrices locales D et B
        D = np.zeros((n_sides, n_polys))
        D[:, 0] = 1
        B = np.zeros((n_polys, n_sides))
        B[0, :] = 1 / n_sides
        
        for i in range(n_sides):
            vert = verts[i]
            prev = verts[(i - 1)% n_sides]
            next = verts[(i + 1) % n_sides]

            vertex_normal= np.array([next[1] - prev[1], prev[0] - next[0]])
            for p in range(1, n_polys):
                poly_degree = linear_polynomial[p]
                monom_grad = poly_degree / diameter
                
                D[i, p] = np.dot(vert - centroid, poly_degree) / diameter
                B[p,i] = 0.5 * np.dot(monom_grad,vertex_normal)
        projector = np.linalg.solve(np.dot(B,D), B) 
        temp = (np.eye(n_sides) - np.dot(D,projector))
        stabilization = np.dot(temp.T , temp)
        G = B @ D
        G[0,:] = 0
        
        local_stiffness =np.dot( np.dot(projector.T, G) , projector) + stabilization
        # Assemblage
        for i, vi in enumerate(vert_ids): #ligne
            for j, vj in enumerate(vert_ids): #colonne
                K[vi, vj] += local_stiffness[i, j]
            F[vi] += rhs(centroid) * area / n_sides

    # Conditions aux limites
    u = np.zeros(n_dofs)
    #print(bords)
    boundary = np.array(bords)
    boundary_vals = boundary_condition(vertices[boundary])   
    internal_dofs = np.setdiff1d(np.arange(n_dofs), boundary)
    
    F-= K[:,boundary]@boundary_vals
    u[internal_dofs] = spsolve(K[internal_dofs, :][:, internal_dofs], F[internal_dofs])
    u[boundary] = boundary_vals
    
    return u, vertices,maxdiam, K

def plot_solution(V,vertices, u, ax):
    #Tracer le contour avec l'axe spécifié
    contour = ax.tricontourf(vertices[:, 0], vertices[:, 1], u, levels=100)
    
    #Ajouter la barre de couleurs
    cbar = plt.colorbar(contour, ax=ax)
    cbar.set_label("Solution")
    
    #Ajouter les points sur le graphique
    rm.draw_meshes(V,ax)
    pass

def l2_error(elements, vertices, u, exact_solution):
    error = 0
    for el in elements:
        vert_ids = np.array(el)
        verts = vertices[vert_ids, :]
        centroid = fct.isobarycenter(verts)
        exact = exact_solution(centroid)
        approx = np.mean(u[vert_ids])
        error += fct.area(verts) * (exact - approx) ** 2
    return np.sqrt(error)

def H1_error(vertices,u,exact_solution,K) :
    u_exact = np.array([exact_solution(v) for v in vertices])
    e = u-u_exact
    error = np.sqrt(e.T @ (K @ e))
    return error
