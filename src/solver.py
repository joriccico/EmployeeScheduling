from ortools.sat.python import cp_model

def solve_model(model):
    solver = cp_model.CpSolver()
    status = solver.solve(model)
    return solver, status
