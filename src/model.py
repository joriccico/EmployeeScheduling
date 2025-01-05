from ortools.sat.python import cp_model
from constraints import add_soft_sequence_constraint, add_soft_sum_constraint
import data

def create_model():
    model = cp_model.CpModel()
    work = {}
    for e in range(data.num_employees):
        for s in range(len(data.shifts)):
            for d in range(data.num_weeks * 7):
                work[e, s, d] = model.new_bool_var(f"work{e}_{s}_{d}")
    # Implementa las restricciones y objetivos aquí utilizando `add_soft_sequence_constraint`.
    return model, work
