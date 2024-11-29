function plot_solution(mesh, u)
    figure;
    trisurf(mesh.elements, mesh.vertices(:, 1), mesh.vertices(:, 2), u, 'EdgeColor', 'none');
    xlabel('x');
    ylabel('y');
    zlabel('u_h');
    title('Virtual Element Solution');
    colorbar;
    view(3);
end