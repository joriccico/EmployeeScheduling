# mappings.py
class Mappings:
    SHIFT = {"libre": 0, "mañana": 1, "tarde": 2, "noche": 3}
    ID_TO_SHIFT = {v: k for k, v in SHIFT.items()}
    DAYS = {"lunes": 0, "martes": 1, "miércoles": 2, "jueves": 3, "viernes": 4, "sábado": 5, "domingo": 6}
    EMPLOYEES = {
        "Pepito": 0, "Juanita": 1, "Carlos": 2, "Ana": 3,
        "Maria": 4, "Miguel": 5, "Juan": 6, "Sara": 7
    }
    ID_TO_WORKER = {v: k for k, v in EMPLOYEES.items()}
