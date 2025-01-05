class Data:
    def __init__(self):
        self.shifts = ["O", "M", "A", "N"]
        self.num_employees = 8
        self.num_weeks = 3
        self.num_days = self.num_weeks * 7
        self.num_shifts = len(self.shifts)

        self.fixed_assignments = [
            (0, 0, 0), (1, 0, 0), (2, 1, 0), (3, 1, 0),
            (4, 2, 0), (5, 2, 0), (6, 2, 3), (7, 3, 0),
            (0, 1, 1), (1, 1, 1), (2, 2, 1), (3, 2, 1),
            (4, 2, 1), (5, 0, 1), (6, 0, 1), (7, 3, 1),
        ]

        self.requests = [
            (3, 0, 5, -2), (5, 3, 10, -2), (2, 3, 4, 4),
        ]

        self.shift_constraints = [
            (0, 1, 1, 0, 2, 2, 0), (3, 1, 2, 20, 3, 4, 5),
        ]

        self.weekly_sum_constraints = [
            (0, 1, 2, 7, 2, 3, 4), (3, 0, 1, 3, 4, 4, 0),
        ]

        self.penalized_transitions = [
            (2, 3, 4), (3, 1, 0),
        ]

        self.weekly_cover_demands = [
            (2, 3, 1), (2, 3, 1), (2, 2, 2), (2, 3, 1),
            (2, 2, 2), (1, 2, 3), (1, 3, 1),
        ]

        self.excess_cover_penalties = (2, 2, 5)
