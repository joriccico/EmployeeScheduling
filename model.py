from ortools.sat.python import cp_model
from constraint import ShiftConstraint

class ShiftSchedulingModel:
    """Encapsula la creación del modelo de programación de turnos."""

    def __init__(self, num_employees, num_weeks):
        # Datos básicos para la planificación.
        self.num_employees = num_employees
        self.num_weeks = num_weeks
        self.num_days = num_weeks * 7
        self.shifts = ["O", "M", "A", "N"]
        self.num_shifts = len(self.shifts)
        self.model = cp_model.CpModel()
        self.work = {}

        self.obj_int_vars = []
        self.obj_int_coeffs = []
        self.obj_bool_vars = []
        self.obj_bool_coeffs = []

    def initialize_variables(self):
        """Inicializa las variables de trabajo (shift assignments)."""
        for e in range(self.num_employees):
            for s in range(self.num_shifts):
                for d in range(self.num_days):
                    self.work[e, s, d] = self.model.new_bool_var(f"work{e}_{s}_{d}")

    def add_constraints(self, fixed_assignments, requests, shift_constraints,
                        weekly_constraints, penalized_transitions, weekly_cover_demands, excess_cover_penalties):
        """Agrega las restricciones al modelo."""
        self.add_one_shift_per_day_constraint()
        self.add_fixed_assignments(fixed_assignments)
        self.add_employee_requests(requests)
        self.add_shift_constraints(shift_constraints)
        self.add_weekly_constraints(weekly_constraints)
        self.add_transition_constraints(penalized_transitions)
        self.add_cover_constraints(weekly_cover_demands, excess_cover_penalties)

    def add_one_shift_per_day_constraint(self):
        """Asegura que cada empleado tenga exactamente un turno por día."""
        for e in range(self.num_employees):
            for d in range(self.num_days):
                self.model.add_exactly_one(self.work[e, s, d] for s in range(self.num_shifts))

    def add_fixed_assignments(self, fixed_assignments):
        """Asigna turnos fijos según las restricciones."""
        for e, s, d in fixed_assignments:
            self.model.add(self.work[e, s, d] == 1)

    def add_employee_requests(self, requests):
        """Agrega las solicitudes de los empleados (positivas y negativas)."""
        for e, s, d, w in requests:
            self.obj_bool_vars.append(self.work[e, s, d])
            self.obj_bool_coeffs.append(w)

    def add_shift_constraints(self, shift_constraints):
        """Agrega restricciones de secuencia para turnos específicos."""
        for ct in shift_constraints:
            shift, hard_min, soft_min, min_cost, soft_max, hard_max, max_cost = ct
            for e in range(self.num_employees):
                works = [self.work[e, shift, d] for d in range(self.num_days)]
                variables, coeffs = ShiftConstraint.add_soft_sequence_constraint(
                    self.model,
                    works,
                    hard_min,
                    soft_min,
                    min_cost,
                    soft_max,
                    hard_max,
                    max_cost,
                    f"shift_constraint(employee {e}, shift {shift})",
                )
                self.obj_bool_vars.extend(variables)
                self.obj_bool_coeffs.extend(coeffs)

    def add_weekly_constraints(self, weekly_constraints):
        """Agrega restricciones semanales a los turnos."""
        for ct in weekly_constraints:
            shift, hard_min, soft_min, min_cost, soft_max, hard_max, max_cost = ct
            for e in range(self.num_employees):
                for w in range(self.num_weeks):
                    works = [self.work[e, shift, d + w * 7] for d in range(7)]
                    variables, coeffs = ShiftConstraint.add_soft_sum_constraint(
                        self.model,
                        works,
                        hard_min,
                        soft_min,
                        min_cost,
                        soft_max,
                        hard_max,
                        max_cost,
                        f"weekly_sum_constraint(employee {e}, shift {shift}, week {w})",
                    )
                    self.obj_int_vars.extend(variables)
                    self.obj_int_coeffs.extend(coeffs)

    def add_transition_constraints(self, penalized_transitions):
        """Agrega restricciones de transiciones penalizadas entre turnos."""
        for previous_shift, next_shift, cost in penalized_transitions:
            for e in range(self.num_employees):
                for d in range(self.num_days - 1):
                    transition = [
                        ~self.work[e, previous_shift, d],
                        ~self.work[e, next_shift, d + 1],
                    ]
                    if cost == 0:
                        self.model.add_bool_or(transition)
                    else:
                        trans_var = self.model.new_bool_var(
                            f"transition (employee={e}, day={d})"
                        )
                        transition.append(trans_var)
                        self.model.add_bool_or(transition)
                        self.obj_bool_vars.append(trans_var)
                        self.obj_bool_coeffs.append(cost)

    def add_cover_constraints(self, weekly_cover_demands, excess_cover_penalties):
        """Asegura que se cumplan las demandas mínimas de turnos."""
        for s in range(1, self.num_shifts):  # Ignoramos el turno "Off" (0)
            for w in range(self.num_weeks):
                for d in range(7):
                    works = [self.work[e, s, w * 7 + d] for e in range(self.num_employees)]
                    min_demand = weekly_cover_demands[d][s - 1]
                    worked = self.model.new_int_var(min_demand, self.num_employees, "")
                    self.model.add(worked == sum(works))
                    over_penalty = excess_cover_penalties[s - 1]
                    if over_penalty > 0:
                        name = f"excess_demand(shift={s}, week={w}, day={d})"
                        excess = self.model.new_int_var(0, self.num_employees - min_demand, name)
                        self.model.add(excess == worked - min_demand)
                        self.obj_int_vars.append(excess)
                        self.obj_int_coeffs.append(over_penalty)

    def set_objective(self):
        """Configura la minimización del objetivo."""
        self.model.minimize(
            sum(self.obj_bool_vars[i] * self.obj_bool_coeffs[i] for i in range(len(self.obj_bool_vars)))
            + sum(self.obj_int_vars[i] * self.obj_int_coeffs[i] for i in range(len(self.obj_int_vars)))
        )
