input_path = 'C:\Users\corme\OneDrive\Bureau\Projet VEM\github\Virtual-element-method\meshes\'
fname = 'L-domain.mat' % #'squares.mat', 'triangles.mat', 'voronoi.mat', 'smoothed-voronoi.mat', 'non-convex.mat', 'L-domain.mat'

mesh_filepath = fullfile(input_path,fname);

vem(mesh_filepath, @square_domain_rhs, @square_domain_boundary_condition);