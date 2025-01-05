from ortools.sat.python import cp_model
from google.protobuf import text_format

class ShiftSchedulingSolver:
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

    def print_solution(self, status):
        """Imprime la solución en caso de ser óptima o factible."""
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print()
            header = "          "
            for w in range(self.model.num_weeks):
                header += "M T W T F S S "
            print(header)
            for e in range(self.model.num_employees):
                schedule = ""
                for d in range(self.model.num_days):
                    for s in range(self.model.num_shifts):
                        if self.solver.boolean_value(self.model.work[e, s, d]):
                            schedule += self.model.shifts[s] + " "
                print(f"worker {e}: {schedule}")

            # Imprimir penalizaciones
            print("\nPenalties:")
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

        # Agregar el resumen de la respuesta del solver
        print(self.solver.ResponseStats())

