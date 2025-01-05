from ortools.sat.python import cp_model
from constraints import add_soft_sequence_constraint, add_soft_sum_constraint

def build_model(data):
    model = cp_model.CpModel()
    work = {
        (e, s, d): model.new_bool_var(f"work{e}_{s}_{d}")
        for e in range(data.num_employees)
        for s in range(data.num_shifts)
        for d in range(data.num_days)
    }

    for e in range(data.num_employees):
        for d in range(data.num_days):
            model.add_exactly_one(work[e, s, d] for s in range(data.num_shifts))

    for e, s, d in data.fixed_assignments:
        model.add(work[e, s, d] == 1)

    obj_bool_vars, obj_bool_coeffs, obj_int_vars, obj_int_coeffs = [], [], [], []

    for e, s, d, w in data.requests:
        obj_bool_vars.append(work[e, s, d])
        obj_bool_coeffs.append(w)

    for ct in data.shift_constraints:
        shift, hard_min, soft_min, min_cost, soft_max, hard_max, max_cost = ct
        for e in range(data.num_employees):
            works = [work[e, shift, d] for d in range(data.num_days)]
            vars, coeffs = add_soft_sequence_constraint(
                model, works, hard_min, soft_min, min_cost, soft_max, hard_max, max_cost,
                f"shift_constraint(employee {e}, shift {shift})",
            )
            obj_bool_vars.extend(vars)
            obj_bool_coeffs.extend(coeffs)

    return model, work, obj_bool_vars, obj_bool_coeffs, obj_int_vars, obj_int_coeffs
