function u = vem(mesh_filepath, rhs, boundary_condition)
    % Compute the virtual element solution of the Poisson problem on the specified mesh
    mesh = load(mesh_filepath); % Load the mesh from a .mat file
    n_dofs = size(mesh.vertices, 1); % Number of degrees of freedom (number of vertices)
    n_polys = 3; % Polynomial degree for virtual element space (degree 1, so 3 polynomials)
    K = sparse(n_dofs, n_dofs); % Stiffness matrix
    F = zeros(n_dofs, 1); % Forcing vector

    linear_polynomials = @(x, y) [1, x, y]; % Linear polynomials
    mod_wrap = @(x, n) mod(x-1, n) + 1; % Helper function for wrapping indices

    for el_id = 1:length(mesh.elements)
        vert_ids = mesh.elements{el_id}; % Global IDs of the vertices of this element
        verts = mesh.vertices(vert_ids, :); % Coordinates of vertices of this element
        n_sides = length(vert_ids); % Number of vertices in the element

        % Geometric information
        area_components = verts(:,1) .* (verts([2:end,1],2) - verts([end,1:end-1],2));
        area = 0.5 * abs(sum(area_components));
        centroid = sum(verts .* verts([2:end,1],2)) + repmat(area_components,1,2) / (2*area);
        diameter = 0; % Initialize diameter
        for i = 1:n_sides
            for j = (i+1):n_sides
                diameter = max(diameter, norm(verts(i,:) - verts(j,:)));
            end
        end

        % Local matrices D and B
        D = zeros(n_sides, n_polys); D(:, 1) = 1;
        B = zeros(n_polys, n_sides); B(1, :) = 1/n_sides;

        for vertex_id = 1:n_sides
            vert = verts(vertex_id, :); % Current vertex
            prev = verts(mod_wrap(vertex_id - 1, n_sides), :); % Previous vertex
            next = verts(mod_wrap(vertex_id + 1, n_sides), :); % Next vertex
            vertex_normal = [next(2) - prev(2), prev(1) - next(1)] / diameter; % Normal vector

            for poly_id = 2:n_polys % Only need to loop over non-constant polynomials
                poly_degree = linear_polynomials(poly_id, 1); % Polynomial degree
                monomial_grad = poly_degree / diameter; % Gradient of the polynomial
                D(vertex_id, poly_id) = dot(vert - centroid, vertex_normal) / diameter;
                B(poly_id, vertex_id) = 0.5 * dot(monomial_grad, vertex_normal);
            end
        end

        % Compute local stiffness and stabilization
        projector = (B*D) \ B; % Ritz projector
        stabilising_term = (eye(n_sides) - D * projector) * (eye(n_sides) - D * projector)';
        G = B*D(:, 1); % Stabilization term
        local_stiffness = projector' * G * projector + stabilising_term;

        % Assemble global stiffness matrix and load vector
        K(vert_ids, vert_ids) = K(vert_ids, vert_ids) + local_stiffness * area / n_sides;
        F(vert_ids) = F(vert_ids) + rhs(centroid) * area / n_sides;
    end

    % Apply boundary conditions
    boundary_vals = boundary_condition(mesh.vertices(mesh.boundary, :)); % Boundary values
    internal_dofs = ~ismember(1:n_dofs, mesh.boundary); % Identify internal DOFs
    u = zeros(n_dofs, 1); % Solution vector initialization
    u(internal_dofs) = K(internal_dofs, internal_dofs) \ F(internal_dofs); % Solve for internal DOFs
    u(mesh.boundary) = boundary_vals; % Set boundary values

    plot_solution(mesh, u); % Visualize the solution
end