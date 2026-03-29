import re
from dataclasses import dataclass
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
        print("----")
        print(machine)
        ordered_requirements = self._get_ordered_requirements(machine)

        # Initialize the first combination, and then we'll explode it at each iteration
        combination_list = [
            Combination(
                current_buttons=machine.buttons.copy(),
                current_joltage=[0] * machine.nb_joltage_levels,
                nb_pushes=0,
                ordered_requirements=ordered_requirements,
                joltage_requirements=machine.joltage_requirements,
            )
        ]

        # print("COMBINATION", len(combination_list))
        # print(combination_list)

        while not any(combination.is_valid() for combination in combination_list):
            combination_list = self._compute_lowest_joltage(combination_list)
            # print("COMBINATION", len(combination_list))
            # print(combination_list)

        print("COMBINATION", len(combination_list))
        result = min(
            combination.nb_pushes
            for combination in combination_list
            if combination.is_valid()
        )
        print(result)
        return result

    def _get_ordered_requirements(self, machine: Machine) -> list[tuple[int, int]]:
        # Order requirements by descending value, we'll
        # always pop the last one when getting buttons
        ordered_requirements: list[tuple[int, int]] = [
            (index, value) for index, value in enumerate(machine.joltage_requirements)
        ]
        ordered_requirements.sort(key=lambda v: v[1], reverse=True)

        return ordered_requirements

    def _compute_lowest_joltage(
        self, combination_list: list[Combination]
    ) -> list[Combination]:
        # TODO : submethods to make it cleaner
        new_combination_list: list[Combination] = []

        for combination in combination_list:
            index, target_value = combination.ordered_requirements.pop()

            choosen_buttons, remaining_buttons = [], []
            for button in combination.current_buttons:
                if index in button:
                    choosen_buttons.append(button)
                else:
                    remaining_buttons.append(button)

            current_target_value = target_value - combination.current_joltage[index]
            choosen_buttons_combinations = list(
                combinations_with_replacement(choosen_buttons, current_target_value)
            )

            for buttons_list in choosen_buttons_combinations:
                try:
                    updated_joltage = self._apply_joltage(combination, buttons_list)
                except ValueError:
                    continue

                # Button combination is OK, let's save updated combination
                new_combination_list.append(
                    Combination(
                        current_buttons=remaining_buttons,
                        current_joltage=updated_joltage,
                        nb_pushes=combination.nb_pushes + current_target_value,
                        ordered_requirements=combination.ordered_requirements.copy(),
                        joltage_requirements=combination.joltage_requirements,
                    )
                )

            # print("new_combination_list :", len(new_combination_list))

        return new_combination_list

    def _apply_joltage(
        self, combination: Combination, buttons_list: Iterable[tuple[int, ...]]
    ) -> list[int]:
        updated_joltage = combination.current_joltage.copy()

        for buttons in buttons_list:
            for button in buttons:
                updated_joltage[button] += 1
                if updated_joltage[button] > combination.joltage_requirements[button]:
                    raise ValueError("Joltage requirements are not met")

        return updated_joltage


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


@dataclass
class Combination:
    current_buttons: list[tuple[int, ...]]
    current_joltage: list[int]
    nb_pushes: int
    ordered_requirements: list[tuple[int, int]]
    joltage_requirements: list[int]

    def is_valid(self) -> bool:
        return self.current_joltage == self.joltage_requirements
