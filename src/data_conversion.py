from mappings import Mappings


def create_request(employee_name: str, shift: str, day_of_week: str, weight: int) -> tuple:
    if employee_name not in Mappings.EMPLOYEES:
        raise ValueError(f"Empleado '{employee_name}' no encontrado.")
    if shift.lower() not in Mappings.SHIFT:
        raise ValueError(f"Turno '{shift}' no es válido. Usa 'mañana', 'tarde' o 'noche'.")
    if day_of_week.lower() not in Mappings.DAYS:
        raise ValueError(f"Día '{day_of_week}' no reconocido. Usa: {', '.join(Mappings.DAYS.keys())}")

    return (
    Mappings.EMPLOYEES[employee_name], Mappings.SHIFT[shift.lower()], Mappings.DAYS[day_of_week.lower()], weight)


def create_fixed_assignment(employee_name: str, shift: str, day_of_week: str) -> tuple:
    if employee_name not in Mappings.EMPLOYEES:
        raise ValueError(f"Empleado '{employee_name}' no encontrado.")
    if shift.lower() not in Mappings.SHIFT:
        raise ValueError(f"Turno '{shift}' no es válido. Usa 'mañana', 'tarde' o 'noche'.")
    if day_of_week.lower() not in Mappings.DAYS:
        raise ValueError(f"Día '{day_of_week}' no reconocido. Usa: {', '.join(Mappings.DAYS.keys())}")

    return Mappings.EMPLOYEES[employee_name], Mappings.SHIFT[shift.lower()], Mappings.DAYS[day_of_week.lower()]


def create_shift_constraint(shift: str, hard_min: int, soft_min: int, min_penalty: int, soft_max: int, hard_max: int,
                            max_penalty: int) -> tuple:
    if shift.lower() not in Mappings.SHIFT:
        raise ValueError(f"Turno '{shift}' no es válido. Usa 'libre', 'mañana', 'tarde' o 'noche'.")

    return (Mappings.SHIFT[shift.lower()], hard_min, soft_min, min_penalty, soft_max, hard_max, max_penalty)


def create_weekly_sum_constraint(shift: str, hard_min: int, soft_min: int, min_penalty: int, soft_max: int,
                                 hard_max: int, max_penalty: int) -> tuple:
    if shift.lower() not in Mappings.SHIFT:
        raise ValueError(f"Turno '{shift}' no es válido. Usa 'libre', 'mañana', 'tarde' o 'noche'.")

    return (Mappings.SHIFT[shift.lower()], hard_min, soft_min, min_penalty, soft_max, hard_max, max_penalty)


def create_penalized_transition(previous_shift: str, next_shift: str, penalty: int) -> tuple:
    if previous_shift.lower() not in Mappings.SHIFT:
        raise ValueError(f"Turno previo '{previous_shift}' no válido.")
    if next_shift.lower() not in Mappings.SHIFT:
        raise ValueError(f"Turno siguiente '{next_shift}' no válido.")

    return (Mappings.SHIFT[previous_shift.lower()], Mappings.SHIFT[next_shift.lower()], penalty)


def create_daily_demand(morning: int, afternoon: int, night: int) -> tuple:
    # No hay mappings necesarios aquí, pero el formato del retorno es consistente con el diseño.
    return (morning, afternoon, night)