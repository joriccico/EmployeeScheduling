from ortools.sat.python import cp_model

class Constraint:
    """Clase para métodos estáticos relacionados con restricciones."""

    @staticmethod
    def negated_bounded_span(
            works: list[cp_model.BoolVarT], start: int, length: int
    ) -> list[cp_model.BoolVarT]:
        """Filters an isolated sub-sequence of variables assined to True.

        Extract the span of Boolean variables [start, start + length), negate them,
        and if there is variables to the left/right of this span, surround the span by
        them in non negated form.

        Args:
          works: a list of variables to extract the span from.
          start: the start to the span.
          length: the length of the span.

        Returns:
          a list of variables which conjunction will be false if the sub-list is
          assigned to True, and correctly bounded by variables assigned to False,
          or by the start or end of works.
        """
        sequence = []
        # left border (start of works, or works[start - 1])
        if start > 0:
            sequence.append(works[start - 1])
        for i in range(length):
            sequence.append(~works[start + i])
        # right border (end of works or works[start + length])
        if start + length < len(works):
            sequence.append(works[start + length])
        return sequence

    @staticmethod
    def add_soft_sequence_constraint(
            model: cp_model.CpModel,
            works: list[cp_model.BoolVarT],
            hard_min: int,
            soft_min: int,
            min_cost: int,
            soft_max: int,
            hard_max: int,
            max_cost: int,
            prefix: str,
    ) -> tuple[list[cp_model.BoolVarT], list[int]]:
        """Sequence constraint on true variables with soft and hard bounds.

        This constraint look at every maximal contiguous sequence of variables
        assigned to true. If forbids sequence of length < hard_min or > hard_max.
        Then it creates penalty terms if the length is < soft_min or > soft_max.

        Args:
          model: the sequence constraint is built on this model.
          works: a list of Boolean variables.
          hard_min: any sequence of true variables must have a length of at least
            hard_min.
          soft_min: any sequence should have a length of at least soft_min, or a
            linear penalty on the delta will be added to the objective.
          min_cost: the coefficient of the linear penalty if the length is less than
            soft_min.
          soft_max: any sequence should have a length of at most soft_max, or a linear
            penalty on the delta will be added to the objective.
          hard_max: any sequence of true variables must have a length of at most
            hard_max.
          max_cost: the coefficient of the linear penalty if the length is more than
            soft_max.
          prefix: a base name for penalty literals.

        Returns:
          a tuple (variables_list, coefficient_list) containing the different
          penalties created by the sequence constraint.
        """
        cost_literals = []
        cost_coefficients = []

        # Forbid sequences that are too short.
        for length in range(1, hard_min):
            for start in range(len(works) - length + 1):
                model.add_bool_or(Constraint.negated_bounded_span(works, start, length))

        # Penalize sequences that are below the soft limit.
        if min_cost > 0:
            for length in range(hard_min, soft_min):
                for start in range(len(works) - length + 1):
                    span = Constraint.negated_bounded_span(works, start, length)
                    name = f": under_span(start={start}, length={length})"
                    lit = model.new_bool_var(prefix + name)
                    span.append(lit)
                    model.add_bool_or(span)
                    cost_literals.append(lit)
                    # We filter exactly the sequence with a short length.
                    # The penalty is proportional to the delta with soft_min.
                    cost_coefficients.append(min_cost * (soft_min - length))

        # Penalize sequences that are above the soft limit.
        if max_cost > 0:
            for length in range(soft_max + 1, hard_max + 1):
                for start in range(len(works) - length + 1):
                    span = Constraint.negated_bounded_span(works, start, length)
                    name = f": over_span(start={start}, length={length})"
                    lit = model.new_bool_var(prefix + name)
                    span.append(lit)
                    model.add_bool_or(span)
                    cost_literals.append(lit)
                    # Cost paid is max_cost * excess length.
                    cost_coefficients.append(max_cost * (length - soft_max))

        # Just forbid any sequence of true variables with length hard_max + 1
        for start in range(len(works) - hard_max):
            model.add_bool_or([~works[i] for i in range(start, start + hard_max + 1)])
        return cost_literals, cost_coefficients

    @staticmethod
    def add_soft_sum_constraint(
            model: cp_model.CpModel,
            works: list[cp_model.BoolVarT],
            hard_min: int,
            soft_min: int,
            min_cost: int,
            soft_max: int,
            hard_max: int,
            max_cost: int,
            prefix: str,
    ) -> tuple[list[cp_model.IntVar], list[int]]:
        """sum constraint with soft and hard bounds.

        This constraint counts the variables assigned to true from works.
        If forbids sum < hard_min or > hard_max.
        Then it creates penalty terms if the sum is < soft_min or > soft_max.

        Args:
          model: the sequence constraint is built on this model.
          works: a list of Boolean variables.
          hard_min: any sequence of true variables must have a sum of at least
            hard_min.
          soft_min: any sequence should have a sum of at least soft_min, or a linear
            penalty on the delta will be added to the objective.
          min_cost: the coefficient of the linear penalty if the sum is less than
            soft_min.
          soft_max: any sequence should have a sum of at most soft_max, or a linear
            penalty on the delta will be added to the objective.
          hard_max: any sequence of true variables must have a sum of at most
            hard_max.
          max_cost: the coefficient of the linear penalty if the sum is more than
            soft_max.
          prefix: a base name for penalty variables.

        Returns:
          a tuple (variables_list, coefficient_list) containing the different
          penalties created by the sequence constraint.
        """
        cost_variables = []
        cost_coefficients = []
        sum_var = model.new_int_var(hard_min, hard_max, "")
        # This adds the hard constraints on the sum.
        model.add(sum_var == sum(works))

        # Penalize sums below the soft_min target.
        if soft_min > hard_min and min_cost > 0:
            delta = model.new_int_var(-len(works), len(works), "")
            model.add(delta == soft_min - sum_var)
            # TODO(user): Compare efficiency with only excess >= soft_min - sum_var.
            excess = model.new_int_var(0, 7, prefix + ": under_sum")
            model.add_max_equality(excess, [delta, 0])
            cost_variables.append(excess)
            cost_coefficients.append(min_cost)

        # Penalize sums above the soft_max target.
        if soft_max < hard_max and max_cost > 0:
            delta = model.new_int_var(-7, 7, "")
            model.add(delta == sum_var - soft_max)
            excess = model.new_int_var(0, 7, prefix + ": over_sum")
            model.add_max_equality(excess, [delta, 0])
            cost_variables.append(excess)
            cost_coefficients.append(max_cost)

        return cost_variables, cost_coefficients
