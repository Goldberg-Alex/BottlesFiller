import random
from collections import defaultdict
from itertools import count
from unittest import TestCase
import matplotlib.pyplot as plt
import numpy as np

from .main import Solver, print_solution


class Test_solver(TestCase):
    def validate_solution(self, solution, required_amount):
        self.assertNotEqual(solution, [], f"there should be a solution")
        self.assertTrue(any(amount == required_amount for amount in solution[-1].bottles.values()),
                        f"one of the bottles should have the required amount")

        self.assertTrue(all(state.is_valid() for state in solution), "all states should be valid")

    def test_solve_3_5_required_4(self):
        solution, closed_set = Solver().solve(required_amount=4, capacities=[3, 5])
        self.validate_solution(solution=solution, required_amount=4)

    def test_solve_3_5_8_required_4(self):
        solution, closed_set = Solver().solve(required_amount=4, capacities=[3, 5, 8])
        self.validate_solution(solution=solution, required_amount=4)

    def test_solve_3_5_8_required_6(self):
        solution, closed_set = Solver().solve(required_amount=6, capacities=[3, 5, 8])
        self.validate_solution(solution=solution, required_amount=6)

    def test_solve_3_8_required_6(self):
        solution, closed_set = Solver().solve(required_amount=6, capacities=[3, 8])
        self.validate_solution(solution=solution, required_amount=6)

    def test_random_small(self):
        max_num_bottles = 5
        max_capacity = 20
        num_bottles = int(np.random.randint(low=2, high=max_num_bottles, size=1))
        capacities = random.sample(range(2, max_capacity), k=num_bottles)
        required_amount = int(np.random.randint(low=1, high=np.max(capacities) - 1, size=1))

        solution, closed_set = Solver().solve(required_amount=required_amount, capacities=capacities)
        self.validate_solution(solution=solution, required_amount=required_amount)

    def test_random_statistics(self):
        max_num_bottles = 5
        max_capacity = 20
        results = []
        longest_solution=[]
        longest_required_amount = 0
        longest_closed = []

        for _ in range(1000):

            num_bottles = int(np.random.randint(low=2, high=max_num_bottles, size=1))
            capacities = random.sample(range(2, max_capacity), k=num_bottles)
            required_amount = int(np.random.randint(low=1, high=np.max(capacities) - 1, size=1))

            solution, closed_set = Solver().solve(required_amount=required_amount, capacities=capacities)
            if solution:
                self.validate_solution(solution=solution, required_amount=required_amount)
            results.append(
                {"capacities": capacities, "required_amount": required_amount, "solution_length": len(solution),
                 "checked_states": len(closed_set)})
            if len(solution) > len(longest_solution):
                longest_solution = solution
                longest_required_amount = required_amount
                longest_closed = closed_set

        solution_distribution = defaultdict(int)
        for solution in results:
            solution_distribution[solution["solution_length"]] += 1

        number_solved = sum(solution['solution_length'] > 0 for solution in results)
        print(f"{number_solved=}")
        import pandas as pd

        df = pd.DataFrame({"steps": list(solution_distribution.keys()), "amount": list(solution_distribution.values())})

        # print(df)
        # print(f"{solution_distribution}")

        # print_solution(solution=longest_solution,closed_states=longest_closed,required_amount=longest_required_amount)

        plt.figure()
        plt.bar(df["steps"], df["amount"])
        plt.show()