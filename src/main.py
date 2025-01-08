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
    num_weeks = 3 # Setmanes per predir

    # Torns fixos (obligats)
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

    # Preferències dels treballadors. IMPORTANT: Negatiu -> Torn desitjat. Positiu -> Torn no desitjat
    requests = [
        create_request("Ana", "libre", "sábado", -2),
        create_request("Miguel", "noche", "jueves", -2),
        create_request("Carlos", "noche", "viernes", 4),
    ]

    # Mínim i màxim de torns del mateix tipus (per exemple matí) en dies consecutius
    shift_constraints = [
        # Dies lliures consecutius: Obligat -> Entre 1 i 2. Preferència -> Entre 1 i 2 (penalització: 0 | 0)
        create_shift_constraint("libre", 1, 1, 0, 2, 2, 0),

        # Torns de nit consecutius: Obligat -> Entre 1 i 4. Preferència -> Entre 2 i 3 (penalització: 20 | 5)
        create_shift_constraint("noche", 1, 2, 20, 3, 4, 5),
    ]

    # Mínim i màxim de torns del mateix tipus (per exemple matí) en la mateixa setmana
    weekly_constraints = [
        # Dies lliures setmanals: Obligat -> Entre 1 i 3. Preferència -> Entre 2 i 2 (penalització: 7 | 4)
        create_weekly_sum_constraint("libre", 1, 2, 7, 2, 3, 4),

        # Dies lliures setmanals: Obligat -> Entre 0 i 4. Preferència -> Entre 1 i 4 (penalització: 3 | 0)
        create_weekly_sum_constraint("noche", 0, 1, 3, 4, 4, 0),
    ]

    # Transicions de torn en dies consecutius penalitzades. IMPORTANT: 0 vol dir prohibit (màxima penalització)
    penalized_transitions = [
        # Tarda a nit té penalització de 4 (avui torn de tarda, demà torn de nit té una penalització de 4)
        create_penalized_transition("tarde", "noche", 4),

        # Nit a matí té penalització de 0 (avui torn de nit, demà torn de matí prohibit)
        create_penalized_transition("noche", "mañana", 0),
    ]

    # Nombre de persones per torn (obligades)
    weekly_cover_demands = [
        create_daily_demand(2, 3, 1),  # Dilluns. 2 matí, 3 tarda, 1 nit
        create_daily_demand(2, 3, 1),  # Dimarts. 2 matí, 3 tarda, 1 nit
        create_daily_demand(2, 2, 2),  # Dimecres. 2 matí, 2 tarda, 2 nit
        create_daily_demand(2, 3, 1),  # Dijous. 2 matí, 3 tarda, 1 nit
        create_daily_demand(2, 2, 2),  # Divendres. 2 matí, 2 tarda, 2 nit
        create_daily_demand(1, 2, 3),  # Dissabte. 1 matí, 2 tarda, 3 nit
        create_daily_demand(1, 3, 1),  # Diumenge. 1 matí, 3 tarda, 1 nit
    ]

    # Penalització per excés de personal en (matí, tarda, nit)
    excess_cover_penalties = (2, 2, 5) # Excés de personal en el torn de nit penalitza més que els torns de matí i tarda

    # Inicializar modelo
    model = Model(num_employees, num_weeks)
    model.initialize_variables()
    model.add_constraints(fixed_assignments, requests, shift_constraints, weekly_constraints, penalized_transitions,
                          weekly_cover_demands, excess_cover_penalties)

    model.set_objective()

    # Resolver modelo
    solver = Solver(model)
    status = solver.solve(_PARAMS.value, _OUTPUT_PROTO.value)
    print()
    solver.print_fixed_assignments(fixed_assignments)
    solver.print_solution(status)


if __name__ == "__main__":
    app.run(main)
