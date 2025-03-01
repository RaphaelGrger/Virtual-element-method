import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix


import functions as fct
import read_mesh as rm
import vem


input_path = '../meshes/generated_meshes/'
    
def test(x,y) :
    return x**2+y**2

def boundary_test(coord):
    return coord[:,0] + coord[:,1] 

if __name__ == '__main__':

    errL2 = []
    errH1 = []
    max_diam = []
    times = []
    N = 7
    for k in range(1,N) :
        fname = 'mesh'+str(k)

    
        Nelements, elements, vertices = rm.read_meshes(fname)
        u,verts, diam,K = vem.vem(fname,vem.rhs,vem.square_boundary_condition)

        V = rm.extract_meshes(elements,verts)

        
        errorL2 = vem.l2_error(rm.csr_to_list(elements), vertices, u, vem.exact_solution)
        errorH1 = vem.H1_error(vertices,u,vem.exact_solution,K)
        
        print(f"Erreur L² : {errorL2:.6e}")
        print(f"Erreur H^1 : {errorH1:.6e}")
        
        plt.close()
        max_diam.append(diam)
        errL2.append(errorL2)
        errH1.append(errorH1)


    plt.loglog(max_diam, errH1, label="Erreur H1",color= 'red', marker='o')
    plt.loglog(max_diam, errL2, label="Erreur L²", marker='o')
    
    plt.xlabel("Diamètre maximal")
    plt.ylabel("Erreur")
    plt.grid(True, which="both", ls="--", color='gray')
    plt.legend()
    plt.show()

    
    #Ordre de convergence
    ordreL2 = []
    ordreH1 = []
    for k in range(0,N-2):
        print(k)
        ordreL2.append( np.log(errL2[k+1]/errL2[k])/np.log(max_diam[k+1]/max_diam[k]))
        ordreH1.append( np.log(errH1[k+1]/errH1[k])/np.log(max_diam[k+1]/max_diam[k]))
    
    plt.close()
    print("Ordre de convergence L² : ", ordreL2)
    print("\nOrdre de convergence H1 : ", ordreH1)
    plt.semilogx(max_diam[1:], ordreL2, marker='o', linestyle='-', color='b', label="Ordre de Convergence L²")
    plt.semilogx(max_diam[1:], ordreH1, marker='o', linestyle='-', color='r', label="Ordre de convergence H1")
    plt.xlabel("Diamètre maximal")
    plt.ylabel("Ordre de convergence")
    plt.grid(True, which="both", ls="--", color='gray')
    plt.legend()
    plt.show()