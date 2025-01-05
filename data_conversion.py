def create_request(employee_name: str, shift: str, day_of_week: str, weight: int) -> tuple:
    shift_mapping = {"libre": 0, "mañana": 1, "tarde": 2, "noche": 3}
    days_mapping = {"lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3, "viernes": 4, "sábado": 5, "domingo": 6}
    employee_mapping = {"Pepito": 0, "Juanita": 1, "Carlos": 2, "Ana": 3, "Maria": 4, "Miguel": 5, "Juan": 6, "Sara": 7}

    if employee_name not in employee_mapping:
        raise ValueError(f"Empleado '{employee_name}' no encontrado.")
    if shift.lower() not in shift_mapping:
        raise ValueError(f"Turno '{shift}' no es válido. Usa 'mañana', 'tarde' o 'noche'.")
    if day_of_week.lower() not in days_mapping:
        raise ValueError(f"Día '{day_of_week}' no reconocido. Usa: {', '.join(days_mapping.keys())}")

    return (employee_mapping[employee_name], shift_mapping[shift.lower()], days_mapping[day_of_week.lower()], weight)


def create_fixed_assignment(employee_name: str, shift: str, day_of_week: str) -> tuple:
    shift_mapping = {"libre": 0, "mañana": 1, "tarde": 2, "noche": 3}
    days_mapping = {"lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3, "viernes": 4, "sábado": 5, "domingo": 6}
    employee_mapping = {"Pepito": 0, "Juanita": 1, "Carlos": 2, "Ana": 3, "Maria": 4, "Miguel": 5, "Juan": 6, "Sara": 7}

    if employee_name not in employee_mapping:
        raise ValueError(f"Empleado '{employee_name}' no encontrado.")
    if shift.lower() not in shift_mapping:
        raise ValueError(f"Turno '{shift}' no es válido. Usa 'mañana', 'tarde' o 'noche'.")
    if day_of_week.lower() not in days_mapping:
        raise ValueError(f"Día '{day_of_week}' no reconocido. Usa: {', '.join(days_mapping.keys())}")

    return (employee_mapping[employee_name], shift_mapping[shift.lower()], days_mapping[day_of_week.lower()])


def create_shift_constraint(shift: str, hard_min: int, soft_min: int, min_penalty: int, soft_max: int, hard_max: int,
                            max_penalty: int) -> tuple:
    shift_mapping = {"libre": 0, "mañana": 1, "tarde": 2, "noche": 3}

    if shift.lower() not in shift_mapping:
        raise ValueError(f"Turno '{shift}' no es válido. Usa 'libre', 'mañana', 'tarde' o 'noche'.")

    return (shift_mapping[shift.lower()], hard_min, soft_min, min_penalty, soft_max, hard_max, max_penalty)


def create_weekly_sum_constraint(shift: str, hard_min: int, soft_min: int, min_penalty: int, soft_max: int,
                                 hard_max: int, max_penalty: int) -> tuple:
    shift_mapping = {"libre": 0, "mañana": 1, "tarde": 2, "noche": 3}

    if shift.lower() not in shift_mapping:
        raise ValueError(f"Turno '{shift}' no es válido. Usa 'libre', 'mañana', 'tarde' o 'noche'.")

    return (shift_mapping[shift.lower()], hard_min, soft_min, min_penalty, soft_max, hard_max, max_penalty)


def create_penalized_transition(previous_shift: str, next_shift: str, penalty: int) -> tuple:
    shift_mapping = {"mañana": 1, "tarde": 2, "noche": 3}

    if previous_shift.lower() not in shift_mapping:
        raise ValueError(f"Turno previo '{previous_shift}' no válido.")
    if next_shift.lower() not in shift_mapping:
        raise ValueError(f"Turno siguiente '{next_shift}' no válido.")

    return (shift_mapping[previous_shift.lower()], shift_mapping[next_shift.lower()], penalty)


def create_daily_demand(morning: int, afternoon: int, night: int) -> tuple:
    return (morning, afternoon, night)