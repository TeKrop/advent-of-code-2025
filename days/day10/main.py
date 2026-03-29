import re
from functools import cached_property
from itertools import combinations_with_replacement
from typing import Iterable

from rich import print

from scripts.utils import AbstractPuzzleSolver

MACHINE_REGEXP = re.compile(r"^\[([.#]+)\] ((?:\(\d(?:,\d+)*\) )+){(\d+(?:,\d+)*)}$")
BUTTONS_REGEXP = re.compile(r"\((\d+(?:,\d+)*)\)")


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 10 - Common Part
    ###########################
    def solve(self) -> tuple[int, int]:
        self.machines = [Machine(line) for line in self.lines]
        return super().solve()

    ###########################
    # DAY 10 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return sum(machine.get_fewest_button_presses() for machine in self.machines)

    ###########################
    # DAY 10 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return 0


class Machine:
    def __init__(self, line: str) -> None:
        matches = MACHINE_REGEXP.match(line)
        if not matches:
            raise ValueError("Input is not valid")

        self.lights_diagram: list[bool] = [
            light_status == "#" for light_status in matches.group(1)
        ]
        self.buttons: list[tuple[int, ...]] = [
            tuple(int(wiring) for wiring in button_wiring.split(","))
            for button_wiring in BUTTONS_REGEXP.findall(matches.group(2))
        ]
        self.joltage_requirements: tuple[int, ...] = tuple(
            int(joltage) for joltage in matches.group(3).split(",")
        )

    def __repr__(self) -> str:
        return (
            "Machine("
            f"lights_diagram={self.lights_diagram}, "
            f"buttons={self.buttons}, "
            f"joltage_requirements={self.joltage_requirements}"
            ")"
        )

    @cached_property
    def nb_lights(self) -> int:
        return len(self.lights_diagram)

    def get_fewest_button_presses(self) -> int:
        nb_presses = 1
        while True:
            if nb_presses > self.nb_lights:
                raise ValueError("No possible solution found for machine")
            if self._has_any_working_combination(nb_presses):
                break
            nb_presses += 1
        return nb_presses

    def _has_any_working_combination(self, nb_presses: int) -> bool:
        possible_combinations = combinations_with_replacement(self.buttons, nb_presses)
        return any(
            self._get_processed_lights(buttons) == self.lights_diagram
            for buttons in possible_combinations
        )

    def _get_processed_lights(
        self, buttons_list: Iterable[tuple[int, ...]]
    ) -> list[bool]:
        lights: list[bool] = [False for i in range(self.nb_lights)]
        for buttons in buttons_list:
            for button in buttons:
                lights[button] = not lights[button]
        return lights
