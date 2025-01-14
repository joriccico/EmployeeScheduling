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

    @staticmethod
    def calculate_day_index(week: int, day_of_week: str) -> int:
        """Retorna l'índex absolut d'un dia basat en la setmana i el dia de la setmana."""
        if day_of_week.lower() not in Mappings.DAYS:
            raise ValueError(f"Día '{day_of_week}' no reconocido.")

        return (week - 1) * 7 + Mappings.DAYS[day_of_week.lower()]
