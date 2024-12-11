input_path = '..\meshes\';
fname = 'triangles'; % 'squares', 'triangles', 'voronoi', 'smoothed-voronoi', 'non-convex', 'L-domain'

% Chemin complet du fichier mesh
mesh_filepath = fullfile(input_path, fname);

% Appel de la fonction VEM
vem(mesh_filepath, @square_domain_rhs, @square_domain_boundary_condition);

% Enregistrement du plot
output_dir = 'res'; % Dossier de sortie
if ~exist(output_dir, 'dir')
    mkdir(output_dir); % Crée le dossier "res" s'il n'existe pas
end

output_filepath = fullfile(output_dir, [fname, '.png']); % Crée le chemin complet avec l'extension
saveas(gcf, output_filepath); % Enregistre le plot
