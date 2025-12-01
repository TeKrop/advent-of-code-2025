from scripts.utils import AbstractPuzzleSolver
from enum import StrEnum
import operator


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 01 - First Part
    ###########################
    STARTING_POINT = 50
    NB_POINTS = 100

    def _solve_first_part(self) -> int:
        current_point = self.STARTING_POINT
        password = 0

        for line in self.lines:
            line_operator = (
                operator.sub if line[0] == DialRotation.LEFT else operator.add
            )

            current_point = line_operator(current_point, int(line[1:])) % self.NB_POINTS
            if current_point == 0:
                password += 1

        return password

    ###########################
    # DAY 01 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        current_point = self.STARTING_POINT
        password = 0

        for line in self.lines:
            previous_point = current_point
            added_value = int(line[1:]) * (-1 if line[0] == DialRotation.LEFT else 1)

            password += self._get_nb_zero_passes(previous_point, added_value)

            current_point = (previous_point + added_value) % self.NB_POINTS

        return password

    def _get_nb_zero_passes(self, previous_point: int, added_value: int) -> int:
        """
        Returns number of times the dial points to zero.
        For negative values, simulate the mirrored movement (100 - X).
        """
        if added_value >= 0:
            new_value = previous_point + added_value
        else:
            new_value = (self.NB_POINTS - previous_point) % self.NB_POINTS - added_value

        return new_value // self.NB_POINTS


class DialRotation(StrEnum):
    LEFT = "L"
    RIGHT = "R"
