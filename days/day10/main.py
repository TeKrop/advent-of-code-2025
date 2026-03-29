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
        return sum(
            self.get_lights_fewest_button_presses(machine) for machine in self.machines
        )

    def get_lights_fewest_button_presses(self, machine: Machine) -> int:
        nb_presses = 1
        while not self._has_any_working_lights_combination(machine, nb_presses):
            nb_presses += 1
        return nb_presses

    def _has_any_working_lights_combination(
        self, machine: Machine, nb_presses: int
    ) -> bool:
        possible_combinations = combinations_with_replacement(
            machine.buttons, nb_presses
        )
        return any(
            self._get_processed_lights(machine, buttons) == machine.lights_diagram
            for buttons in possible_combinations
        )

    def _get_processed_lights(
        self, machine: Machine, buttons_list: Iterable[tuple[int, ...]]
    ) -> list[bool]:
        lights: list[bool] = [False for i in range(machine.nb_lights)]
        for buttons in buttons_list:
            for button in buttons:
                lights[button] = not lights[button]
        return lights

    ###########################
    # DAY 10 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return sum(
            self.get_joltage_fewest_button_presses(machine) for machine in self.machines
        )

    def get_joltage_fewest_button_presses(self, machine: Machine) -> int:
        nb_presses = max(machine.joltage_requirements)
        print("------")
        print(nb_presses)
        print(machine)
        while not self._has_any_valid_joltage_combination(machine, nb_presses):
            print("------")
            print(nb_presses)
            print(machine)
            nb_presses += 1
        return nb_presses

    def _has_any_valid_joltage_combination(
        self, machine: Machine, nb_presses: int
    ) -> bool:
        possible_combinations = self._get_joltage_combinations(machine, nb_presses)
        return any(
            self._is_valid_voltage(machine, buttons)
            for buttons in possible_combinations
        )

    def _get_joltage_combinations(self, machine: Machine, nb_presses: int) -> Iterable:
        # Get min combinations. Ex with 7 (), combinations must have :
        # - Toutes les combinations doivent avoir un "3" sinon ça fera moins de 7
        # - Si 8 : 1 combinaison ne doit pas avoir de 3, toutes les autres si
        # - Si 9 : 2 combi doivent ne pas avoir de 3, les 7 autres doivent
        maximum_value = max(machine.joltage_requirements)
        maximum_pos = machine.joltage_requirements.index(maximum_value)
        buttons_without_maximum: list[tuple[int, ...]] = []
        buttons_with_maximum: list[tuple[int, ...]] = []
        for button in machine.buttons:
            if maximum_pos in button:
                buttons_with_maximum.append(button)
            else:
                buttons_without_maximum.append(button)

        nb_buttons_without_max_needed = nb_presses - maximum_value
        nb_buttons_with_max_needed = nb_presses - nb_buttons_without_max_needed

        buttons_with_combinations = list(
            combinations_with_replacement(
                buttons_with_maximum, nb_buttons_with_max_needed
            )
        )
        buttons_without_combinations = list(
            combinations_with_replacement(
                buttons_without_maximum, nb_buttons_without_max_needed
            )
        )

        print("buttons_with_combinations :", len(buttons_with_combinations))
        print("buttons_without_combinations :", len(buttons_without_combinations))
        print(
            "Buttons combi total :",
            len(buttons_with_combinations) * len(buttons_without_combinations),
        )

        combined_combinations = [
            buttons_with + buttons_without
            for buttons_with in buttons_with_combinations
            for buttons_without in buttons_without_combinations
        ]

        return combined_combinations

    def _is_valid_voltage(
        self, machine: Machine, buttons_list: Iterable[tuple[int, ...]]
    ) -> bool:
        joltage: list[int] = [0] * machine.nb_joltage_levels

        for buttons in buttons_list:
            for button in buttons:
                joltage[button] += 1
                if joltage[button] > machine.joltage_requirements[button]:
                    return False

        return joltage == machine.joltage_requirements


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
        self.joltage_requirements: list[int] = [
            int(joltage) for joltage in matches.group(3).split(",")
        ]

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

    @cached_property
    def nb_joltage_levels(self) -> int:
        return len(self.joltage_requirements)
