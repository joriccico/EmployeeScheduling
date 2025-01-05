from absl import app, flags
from model import Model
from solver import Solver
from data_conversion import create_shift_constraint, create_request, create_penalized_transition, create_weekly_sum_constraint, create_daily_demand, create_fixed_assignment

# Definiciones de los parámetros de la línea de comandos
_OUTPUT_PROTO = flags.DEFINE_string(
    "output_proto", "", "Output file to write the cp_model proto to."
)
_PARAMS = flags.DEFINE_string(
    "params", "max_time_in_seconds:2.0", "Sat solver parameters."
)

def main(_):
    # Datos originales del problema
    num_employees = 8
    num_weeks = 3

    fixed_assignments = [
        create_fixed_assignment("Pepito", "libre", "lunes"),
        create_fixed_assignment("Juanita", "libre", "lunes"),
        create_fixed_assignment("Carlos", "mañana", "lunes"),
        create_fixed_assignment("Ana", "mañana", "lunes"),
        create_fixed_assignment("Maria", "tarde", "lunes"),
        create_fixed_assignment("Miguel", "tarde", "lunes"),
        create_fixed_assignment("Juan", "tarde", "jueves"),
        create_fixed_assignment("Sara", "noche", "lunes"),
        create_fixed_assignment("Pepito", "mañana", "martes"),
        create_fixed_assignment("Juanita", "mañana", "martes"),
        create_fixed_assignment("Carlos", "tarde", "martes"),
        create_fixed_assignment("Ana", "tarde", "martes"),
        create_fixed_assignment("Maria", "tarde", "martes"),
        create_fixed_assignment("Miguel", "libre", "martes"),
        create_fixed_assignment("Juan", "libre", "martes"),
        create_fixed_assignment("Sara", "noche", "martes"),
    ]

    requests = [
        create_request("Ana", "libre", "sábado", -2),
        create_request("Miguel", "noche", "jueves", -2),
        create_request("Carlos", "noche", "viernes", 4),
    ]

    shift_constraints = [
        create_shift_constraint("libre", 1, 1, 0, 2, 2, 0),
        create_shift_constraint("noche", 1, 2, 20, 3, 4, 5),
    ]

    weekly_constraints = [
        create_weekly_sum_constraint("libre", 1, 2, 7, 2, 3, 4),
        create_weekly_sum_constraint("noche", 0, 1, 3, 4, 4, 0),
    ]

    penalized_transitions = [
        create_penalized_transition("tarde", "noche", 4),
        create_penalized_transition("noche", "mañana", 0),
    ]

    weekly_cover_demands = [
        create_daily_demand(2, 3, 1),  # Lunes
        create_daily_demand(2, 3, 1),  # Martes
        create_daily_demand(2, 2, 2),  # Miércoles
        create_daily_demand(2, 3, 1),  # Jueves
        create_daily_demand(2, 2, 2),  # Viernes
        create_daily_demand(1, 2, 3),  # Sábado
        create_daily_demand(1, 3, 1),  # Domingo
    ]

    excess_cover_penalties = (2, 2, 5)

    # Inicializar modelo
    model = Model(num_employees, num_weeks)
    model.initialize_variables()
    model.add_constraints(fixed_assignments, requests, shift_constraints, weekly_constraints, penalized_transitions,
                          weekly_cover_demands, excess_cover_penalties)

    #model.obj_bool_coeffs = [coef // 2 for coef in model.obj_bool_coeffs]
    #model.obj_int_coeffs = [coef // 2 for coef in model.obj_int_coeffs]

    model.set_objective()

    # Resolver modelo
    solver = Solver(model)
    status = solver.solve(_PARAMS.value, _OUTPUT_PROTO.value)
    solver.print_solution(status)


if __name__ == "__main__":
    app.run(main)