from scripts.utils import AbstractPuzzleSolver
from typing import Callable
from dataclasses import dataclass
import operator


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 06 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        problems = self._get_grouped_problems()
        return sum(problem.get_grand_total() for problem in problems)

    def _get_grouped_problems(self) -> list[Problem]:
        nb_problems = len(self.line.split())
        problems = [Problem(numbers=[]) for i in range(nb_problems)]

        for line in self.lines[:-1]:
            values = line.split()
            for i, value in enumerate(values):
                problems[i].numbers.append(int(value))

        operators = self.lines[-1].split()
        for i, char in enumerate(operators):
            problems[i].operator = operator.add if char == "+" else operator.mul

        return problems

    ###########################
    # DAY 06 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        problems = self._get_columns_problems()
        return sum(problem.get_grand_total() for problem in problems)

    def _get_columns_problems(self) -> list[Problem]:
        nb_problems = len(self.line.split())
        problems = [Problem(numbers=[]) for i in range(nb_problems)]

        current_problem = 0
        nb_columns = max(len(line) for line in self.lines)

        for i in range(nb_columns - 1, -1, -1):
            current_number = ""
            for line in self.lines:
                # Space char or out of bounds, go next
                if i > len(line) - 1 or line[i] == " ":
                    continue
                # Operator, store it
                elif line[i] in ("+", "*"):
                    problems[current_problem].operator = (
                        operator.add if line[i] == "+" else operator.mul
                    )
                # Number, assemble digits
                else:
                    current_number += line[i]

            # Empty column
            if not current_number:
                continue

            problems[current_problem].numbers.append(int(current_number))
            if problems[current_problem].operator is not None:
                current_problem += 1

        return problems


@dataclass
class Problem:
    numbers: list[int]
    operator: Callable | None = None

    def get_grand_total(self) -> int:
        total = self.numbers[0]
        for number in self.numbers[1:]:
            total = self.operator(total, number)
        return total
