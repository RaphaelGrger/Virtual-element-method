import skfem as fem
from skfem.helpers import dot, grad 
import numpy as np
import matplotlib.pyplot as plt


@fem.Functional
def erreurL2(w):   # erreur L2
    x, y = w.x
    uh = w['uh']
    u = 15*np.sin(np.pi * x) * np.sin(np.pi * y) / (2. * np.pi ** 2)
    return np.sqrt(np.sum((uh - u) ** 2))

def f(x,y) : #Second membre
    return 15 * np.sin(np.pi * x) * np.sin(np.pi * y)

@fem.BilinearForm
def a(u, v,_): # forme bilinéaire
    return dot(grad(u), grad(v))

@fem.LinearForm
def l(v, w): # forme linéaire
    x, y = w.x  # coordonnées globales
    return v *f(x,y)

# condition aux bords
def boundary_condition(x):
    X, Y = x 
    return X * Y * np.sin(np.pi * X) * 0

N = 3 # Niveau de raffinage
mesh = fem.MeshTri().refined(N) # maillage
Vh = fem.Basis(mesh, fem.ElementTriP1()) # espace des fonctions


# Assemblage des matrices et du vecteur
A = a.assemble(Vh)
b = l.assemble(Vh)

# Application des conditions aux bords
D = Vh.get_dofs()
boundary_values = boundary_condition(Vh.doflocs)  # g(x, y) sur les bords
x = fem.solve(*fem.condense(A, b, D=D, x=boundary_values))

X, Y = mesh.p  # coordonnées des points (nodes)
triangles = mesh.t.T  # triangles du maillage
solution = x  # solution approchée

errL2 = round(erreurL2.assemble(Vh, uh=Vh.interpolate(x)), 4)

plt.figure(figsize=(8, 6))

plt.tricontourf(X, Y, triangles, solution, levels=50, cmap="viridis")
plt.colorbar(label="Solution $u(x, y)$")

plt.triplot(X, Y, triangles, color="black", linewidth=0.5, alpha=0.5)
plt.title("Solution avec éléments finis")
plt.xlabel("$x$")
plt.ylabel("$y$")
plt.gca().set_aspect('equal')
plt.show()

print(f'Erreur L² : {errL2}')