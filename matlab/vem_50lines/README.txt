  ***************************************************************************
  * All the software  contained in this library  is protected by copyright. *
  * Permission  to use, copy, modify, and  distribute this software for any *
  * purpose without fee is hereby granted, provided that this entire notice *
  * is included  in all copies  of any software which is or includes a copy *
  * or modification  of this software  and in all copies  of the supporting *
  * documentation for such software.                                        *
  ***************************************************************************
  * THIS SOFTWARE IS BEING PROVIDED "AS IS", WITHOUT ANY EXPRESS OR IMPLIED *
  * WARRANTY. IN NO EVENT, NEITHER  THE AUTHORS, NOR THE PUBLISHER, NOR ANY *
  * MEMBER  OF THE EDITORIAL BOARD OF  THE JOURNAL  "NUMERICAL ALGORITHMS", *
  * NOR ITS EDITOR-IN-CHIEF, BE  LIABLE FOR ANY ERROR  IN THE SOFTWARE, ANY *
  * MISUSE  OF IT  OR ANY DAMAGE ARISING OUT OF ITS USE. THE ENTIRE RISK OF *
  * USING THE SOFTWARE LIES WITH THE PARTY DOING SO.                        *
  ***************************************************************************
  * ANY USE  OF THE SOFTWARE  CONSTITUTES  ACCEPTANCE  OF THE TERMS  OF THE *
  * ABOVE STATEMENT.                                                        *
  ***************************************************************************

   AUTHOR:

       Oliver Sutton
       University of Leicester, United Kingdom
       E-mail: ojs4@le.ac.uk

   REFERENCE:

    -  The virtual element method in 50 lines of MATLAB
       NUMERICAL ALGORITHMS, 75 (2017), PP. 1141-1159

   SOFTWARE REVISION DATE:

       V2.0, November 2016

   SOFTWARE LANGUAGE:

       MATLAB 9.1


============================================================================
SOFTWARE
============================================================================
This software provides all the functions needed to compute approximate
solutions to Poisson's problem using the lowest order virtual element method 
on polygonal meshes.

============================================================================
PACKAGE
============================================================================

The directory contains the following files

README.txt                         : this file
vem.m                              : the main function implementing the virtual 
                                     element method, with specifiable boundary 
                                     conditions and forcing term
square_domain_rhs.m                : an implementation of a sample forcing 
                                     function, as used for the example problem 
                                     on the square-shaped domain in the paper
square_domain_boundary_condition.m : an implementation of a sample boundary 
                                     condition function, as used in the example
                                     problem on the square-shaped domain in the
                                     paper
L_domain_rhs.m                     : an implementation of a sample forcing 
                                     function, as used for the example problem 
                                     on the L-shaped domain in the paper
L_domain_boundary_condition.m      : an implementation of a sample boundary 
                                     condition function, as used in the example
                                     problem on the L-shaped domain in the
                                     paper
plot_solution.m                    : uses the MATLAB 'patch' function to plot
                                     the virtual element solution using its 
                                     values at the vertices of the mesh

The 'meshes' subdirectory also contains the following files

L-domain.mat         : contains a description of a Voronoi polygonal mesh of 
                       an L-shaped domain
non-convex.mat       : contains a description of a mesh of a square-shaped
                       domain consisting of non-convex polygonal elements
smoothed-voronoi.mat : contains a description of a mesh of a square-shaped 
                       domain, formed of a Voronoi mesh which has been smoothed 
                       using Lloyd's algorithm as implemented by PolyMesher
squares.mat          : contains a description of a mesh of a square-shaped 
                       domain consisting of square elements
triangles.mat        : contains a description of a mesh of a square-shaped
                       domain consisting of triangular elements
voronoi.mat          : contains a description of a Voronoi mesh of a 
                       square-shaped domain, formed using random centroids

An explanation of the data structures used to describe the meshes in these
files is provided in the paper “The virtual element method in 50 lines of
MATLAB”, along with illustrations of each mesh (shown in Figure 1).

============================================================================
HOW TO INSTALL
============================================================================

Unpack vem_50lines.zip. The directory vem_50lines will be created with all
the needed files inside. Add the directory vem_50lines to the path in
Matlab or change the current working directory to vem_50lines.

============================================================================
HOW TO USE
============================================================================

Running the method simply involves calling the 'vem' function with the
following three arguments:
    1. the path to a mesh file, e.g. 'meshes/voronoi.mat'
    2. a function handle to a function implementing the PDE right hand side,
       e.g. @square_domain_rhs
    3. a function handle to a function implementing the PDE boundary 
       condition, e.g. @square_domain_boundary_condition


For example, Figure 3(a) in the paper 'The virtual element method in 50 
lines of MATLAB' can be produce by calling:

u = vem('meshes/voronoi.mat',@square_domain_rhs, ...
	@square_domain_boundary_condition);
view(150,30)

Similarly, Figure 3(b) can be produced by running:

u = vem('meshes/L-domain.mat', @L_domain_rhs, @L_domain_boundary_condition);
view(120,30)

These compute the solution to a Poisson problem on a square domain and an
L-shaped domain, respectively.

