from ortools.sat.python import cp_model


def solve_model(model, work, data, obj_bool_vars, obj_bool_coeffs, obj_int_vars, obj_int_coeffs):
    solver = cp_model.CpSolver()
    solution_printer = cp_model.ObjectiveSolutionPrinter()
    status = solver.solve(model, solution_printer)

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("Solution:")
        for e in range(data.num_employees):
            schedule = ""
            for d in range(data.num_days):
                for s in range(data.num_shifts):
                    if solver.boolean_value(work[e, s, d]):
                        schedule += data.shifts[s] + " "
            print(f"Worker {e}: {schedule}")
        print("\nPenalties:")
        for i, var in enumerate(obj_bool_vars):
            if solver.boolean_value(var):
                penalty = obj_bool_coeffs[i]
                print(f"  {var.name}: {penalty}")
