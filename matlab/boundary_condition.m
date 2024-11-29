function boundary_cond = boundary_condition(x, y)
    boundary_cond = x * y * sin(pi * x);
end