import re
from dataclasses import dataclass
from functools import cached_property
from itertools import combinations_with_replacement
from typing import Iterable

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

        while not any(combination.is_valid() for combination in combination_list):
            combination_list = self._compute_lowest_joltage(combination_list)

        return min(
            combination.nb_pushes
            for combination in combination_list
            if combination.is_valid()
        )

    def _get_ordered_requirements(self, machine: Machine) -> list[tuple[int, int]]:
        """
        Order requirements depending on the lowest number of buttons with the same value.
        We'll proceed recursively until no button left to build the list.
        As we'll always pop the last one, the next value to take will be at the end
        """
        ordered_requirements: list[tuple[int, int]] = []

        remaining_buttons = machine.buttons.copy()
        while len(remaining_buttons) > 0:
            # Get the index value which is in less buttons
            buttons_by_indexes = {
                index: [button for button in remaining_buttons if index in button]
                for index, _ in enumerate(machine.joltage_requirements)
            }
            choosen_index = min(
                (index for index, buttons in buttons_by_indexes.items() if buttons),
                key=lambda index: len(buttons_by_indexes[index]),
            )

            # We'll add it in the ordered requirements along with corresponding value
            ordered_requirements.append(
                (choosen_index, machine.joltage_requirements[choosen_index])
            )

            # Update remaining buttons
            for button in buttons_by_indexes[choosen_index]:
                remaining_buttons.remove(button)

        # Ensure lower values will be "poped" first
        ordered_requirements.sort(key=lambda v: v[1], reverse=True)

        return ordered_requirements

    def _compute_lowest_joltage(
        self, combination_list: list[Combination]
    ) -> list[Combination]:
        new_combination_list: list[Combination] = []

        for combination in combination_list:
            index, target_value = combination.ordered_requirements.pop()
            current_target_value = target_value - combination.current_joltage[index]

            choosen_buttons, remaining_buttons = [], []
            for button in combination.current_buttons:
                if index in button:
                    choosen_buttons.append(button)
                else:
                    remaining_buttons.append(button)

            choosen_buttons_combinations = self._get_possible_buttons_combinations(
                combination, choosen_buttons, current_target_value
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

        return new_combination_list

    def _get_possible_buttons_combinations(
        self,
        combination: Combination,
        choosen_buttons: list[tuple[int, ...]],
        current_target_value: int,
    ) -> list[list[tuple[int, ...]]]:
        # Each button has a max presses depending on the actual joltage.
        # We'll combine these to ensure proper coverage
        buttons_max: dict[tuple[int, ...], int] = {
            buttons_list: min(
                (
                    combination.joltage_requirements[button]
                    - combination.current_joltage[button]
                )
                for button in buttons_list
            )
            for buttons_list in choosen_buttons
        }

        # Buttons with 0 should be rejected
        for buttons_list, max_pushes in buttons_max.items():
            if max_pushes == 0:
                choosen_buttons.remove(buttons_list)

        if not choosen_buttons:
            return [[tuple()]]

        return list(
            combinations_with_replacement(choosen_buttons, current_target_value)
        )

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
