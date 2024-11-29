% 1. Test des fonctions rhs et boundary_condition
x = 1;
y = 1;

% Tester rhs et boundary_condition avec x = y = 1
rhs_value = rhs(x, y);
fprintf('Valeur de rhs(x=%f, y=%f) : %f\n', x, y, rhs_value);
boundary_value = boundary_condition(x, y);
fprintf('Valeur de boundary_condition(x=%f, y=%f) : %f\n', x, y, boundary_value);

% 2. Charger le fichier de maillage Voronoi
mesh_filepath = '../meshes/voronoi.npz';

% Appeler la fonction vem
u = vem(mesh_filepath, @rhs, @boundary_condition);

% Affichage de la solution obtenue
fprintf('La fonction vem a été appelée et a retourné la solution.\n');
