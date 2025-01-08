from ortools.sat.python import cp_model
from google.protobuf import text_format

from mappings import Mappings

class Solver:
    """Se encarga de resolver el problema del modelo."""

    def __init__(self, model):
        self.model = model
        self.solver = cp_model.CpSolver()

    def solve(self, params, output_proto):
        """Resuelve el modelo especificado."""
        if output_proto:
            print(f"Writing proto to {output_proto}")
            with open(output_proto, "w") as text_file:
                text_file.write(str(self.model.model))
        if params:
            text_format.Parse(params, self.solver.parameters)
        solution_printer = cp_model.ObjectiveSolutionPrinter()
        return self.solver.solve(self.model.model, solution_printer)

    def print_fixed_assignments(self, fixed_assignments):
        """Imprime las asignaciones fijas antes de resolver el problema."""
        print("=== Fixed Assignments ===")

        header = " " * 15 + "| "  # Espaciado inicial para alineación correcta
        header += " | ".join(f"{day:<11}" for day in self.model.day_names)
        header += " |"
        print(header)
        print("—" * len(header))  # Línea horizontal que cruza todo el ancho del encabezado

        # Agrupar las asignaciones fijas por turnos y luego por días
        fixed_schedule = {shift_name: [[] for _ in range(7)] for shift_name in Mappings.ID_TO_SHIFT.values()}

        for emp_id, shift_id, day in fixed_assignments:
            shift_name = Mappings.ID_TO_SHIFT[shift_id]  # Convierte el ID del turno al nombre (ej: "Morning")
            fixed_schedule[shift_name][day].append(
                Mappings.ID_TO_WORKER[emp_id])  # Añade al empleado al día correspondiente

        # Imprimir cada turno por separado
        for shift_name, rows in fixed_schedule.items():

            max_lines = max(len(rows[day]) for day in range(7))  # Filas necesarias para cada día
            for line in range(max_lines):
                row = f"{shift_name:<15}" if line == 0 else " " * 15  # Imprimir el turno una vez
                row += "| "
                for day in range(7):
                    if line < len(rows[day]):  # Hay un empleado asignado
                        row += f"{rows[day][line]:<11} | "
                    else:  # Espacio vacío
                        row += " " * 11 + " | "
                print(row)

            print("—" * len(header))  # Separador después de cada turno

    def print_solutionSchedule(self):
        # Imprime por semana
        print("=== Solution Schedule ===")
        for week in range(self.model.num_weeks):
            print(f"Week {week + 1}")
            # Encabezado con nombres de los días
            header = " " * 15 + "| "  # Espaciado inicial para alineación correcta
            header += " | ".join(f"{day:<11}" for day in self.model.day_names)
            header += " |"
            print(header)
            print("—" * len(header))  # Línea horizontal que cruza todo el ancho del encabezado

            # Imprime los turnos para cada día de la semana
            previous_group = None  # Para comprobar el grupo de turnos
            for shift_index, shift_name in enumerate(self.model.shifts):
                # Ignorar el turno "Off"
                if shift_name.lower() == "off":
                    continue

                # Separación entre grupos de turnos
                current_group = "Morning" if "Morning" in shift_name else \
                    "Afternoon" if "Afternoon" in shift_name else \
                        "Night" if "Night" in shift_name else "Other"
                if current_group != previous_group and previous_group is not None:
                    print("—" * len(header))  # Línea de separación
                previous_group = current_group

                # Construir filas de empleados asignados para cada día
                rows = [[] for _ in range(7)]  # 7 días en una semana
                max_lines = 1  # Máximo número de líneas en cualquier columna
                for d in range(week * 7, (week + 1) * 7):  # Días de la semana actual
                    # Encuentra empleados asignados al turno actual
                    employees = [
                        Mappings.ID_TO_WORKER[e]
                        for e in range(self.model.num_employees)
                        if self.solver.boolean_value(self.model.work[e, shift_index, d])
                    ]
                    rows[d % 7] = employees
                    max_lines = max(max_lines, len(employees))

                # Imprime línea por línea para el turno
                for line in range(max_lines):
                    row = f"{shift_name if line == 0 else '':<15}" + "| "  # Nombre del turno solo en la primera línea
                    for day in range(7):  # Repite por los 7 días
                        if line < len(rows[day]):  # Hay un empleado asignado en esta línea
                            row += f"{rows[day][line]:<11} | "
                        else:  # Espacio vacío
                            row += " " * 11 + " | "
                    print(row)

            print("—" * len(header))  # Línea horizontal al final de cada semana
            print() if week < self.model.num_weeks-1 else None # Línea vacía entre semanas

    def print_penalties(self):
        # Imprimir penalizaciones
        print("=== Penalties ===")
        for i, var in enumerate(self.model.obj_bool_vars):
            if self.solver.boolean_value(var):
                penalty = self.model.obj_bool_coeffs[i]
                if penalty > 0:
                    print(f"  {var.name} violated, penalty={penalty}")
                else:
                    print(f"  {var.name} fulfilled, gain={-penalty}")

        for i, int_var in enumerate(self.model.obj_int_vars):
            if self.solver.value(int_var) > 0:
                penalty = self.model.obj_int_coeffs[i]
                print(f"  {int_var.Name()} violated by {self.solver.value(int_var)}, linear penalty={penalty}")

    def print_solution(self, status):
        """Imprime la solución en caso de ser óptima o factible."""
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print()
            self.print_solutionSchedule()
            print()
            self.print_penalties()
            print()
            # Agregar el resumen de la respuesta del solver
            print(self.solver.ResponseStats())

