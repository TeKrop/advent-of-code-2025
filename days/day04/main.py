from scripts.utils import AbstractPuzzleSolver
from enum import StrEnum
from functools import cached_property
from typing import Generator


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 04 - Common Part
    ###########################
    nb_max_rolls: int = 4

    positions_to_check: list[tuple[int, int]] = [
        (i, j) for i in range(-1, 2) for j in range(-1, 2) if not (i == 0 and j == 0)
    ]

    @cached_property
    def nb_lines(self) -> int:
        return len(self.lines)

    @cached_property
    def nb_columns(self) -> int:
        return len(self.line)

    def solve(self) -> tuple[int, int]:
        self.diagram = [[char for char in line] for line in self.lines]
        return super().solve()

    def _get_removable_rolls(
        self, diagram: list[list[str]]
    ) -> Generator[tuple[int, int]]:
        return (
            (x, y)
            for y, line in enumerate(diagram)
            for x, char in enumerate(line)
            if (
                char == Symbol.ROLL_OF_PAPER
                and self._is_roll_of_paper_accessible(diagram, x, y)
            )
        )

    def _is_roll_of_paper_accessible(
        self, diagram: list[list[str]], x: int, y: int
    ) -> bool:
        nb_adjacent_rolls = 0
        is_roll_of_paper_accessible = True

        for i, j in self.positions_to_check:
            # Ensure we'll have a valid position (not outside of the diagram)
            if y + i in (-1, self.nb_lines) or x + j in (-1, self.nb_lines):
                continue

            if diagram[y + i][x + j] != Symbol.ROLL_OF_PAPER:
                continue

            nb_adjacent_rolls += 1
            if nb_adjacent_rolls == self.nb_max_rolls:
                is_roll_of_paper_accessible = False
                break

        return is_roll_of_paper_accessible

    ###########################
    # DAY 04 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return sum(1 for _ in self._get_removable_rolls(self.diagram))

    ###########################
    # DAY 04 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        nb_total_removable_rolls = 0
        next_diagram = self.diagram

        has_removable_rolls = True
        while has_removable_rolls:
            has_removable_rolls = False

            for x, y in self._get_removable_rolls(self.diagram):
                has_removable_rolls = True
                nb_total_removable_rolls += 1
                next_diagram[y][x] = Symbol.EMPTY.value

            self.diagram = next_diagram

        return nb_total_removable_rolls


class Symbol(StrEnum):
    EMPTY = "."
    ROLL_OF_PAPER = "@"
