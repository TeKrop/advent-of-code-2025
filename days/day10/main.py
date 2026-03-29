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

        # Autre réflexion : prendre l'indice le moins fréquent dans les boutons.
        # Exemple avec le cas de 0 à 7 avec 239 en maximum
        # -> (0,4,5,6) (1,3,6) (0,1,2,3,4,5,6) (0,3,6,7) (1,2,3,4,6,7) (1,2,4,5) {206,71,52,235,56,42,239,196}
        # - Une fois les deux avec 7 pris en compte, on compte le nombre de combinaisons potentiellement valides
        #   - Certaines combinaisons ne le seront pas car valeur trop élevée sur un autre indice.
        #       - Facilement identifiable : (0,3,6,7) seul est OK, mais (1,2,3,4,6,7) ne pourra être là que 52 fois "2"
        #   - Chaque combinaison donnera déjà un état de joltage
        #   - On peut très bien prendre UN SEUL des deux en combinaisons mais X fois si c'est OK
        #       - Cas limite à éviter pour la complexité dans la sélection initiale
        # - On obtient une liste limitée des possibilités avec les deux
        #   - Cette liste sera multipliée avec les suivantes pour donner les possibles
        #   - Ou alors on fera du test en direct avec le prochain groupe pour limiter le nombre dès que possible
        # -> [.##.##.#] (0,4,5,6) (1,3,6) (0,1,2,3,4,5,6) (1,2,4,5) {206,71,52,235,56,42,239,196}
        # - On réduit la liste initiale en retirant les deux, puis on prend le suivant moins fréquent
        # - On fonctionne récursivement :
        #   - pour chaque combinaison (les "2" par exemple), on va tenter de les apposer aux possibles actuels + joltage
        #       - Si à un moment donné ça dépasse, la combinaison n'est pas possible et on continue

        # remaining_requirements = machine.joltage_requirements.copy()
        # minimum_value = min(remaining_requirements)
        # minimum_pos = remaining_requirements.index(minimum_value)

        # buttons_without_choosen: list[tuple[int, ...]] = []
        # buttons_with_choosen: list[tuple[int, ...]] = []
        # for button in machine.buttons:
        #     if minimum_pos in button:
        #         buttons_with_choosen.append(button)
        #     else:
        #         buttons_without_choosen.append(button)

        # nb_buttons_with_choosen_needed = minimum_value
        # print("nb_buttons_with_choosen_needed", nb_buttons_with_choosen_needed)

        # nb_buttons_without_choosen_needed = nb_presses - minimum_value
        # print("nb_buttons_without_choosen_needed", nb_buttons_without_choosen_needed)

        # starting_joltage: list[int] = [0] * machine.nb_joltage_levels
        # buttons_with_combinations = list(
        #     combinations_with_replacement(
        #         buttons_with_choosen, nb_buttons_with_choosen_needed
        #     )
        # )
        # print("buttons_with_combinations", len(buttons_with_combinations))
        # valid_buttons_with_combinations: dict[tuple[int, ...], list[int]] = {}
        # cpt = 0
        # for buttons_list in buttons_with_combinations:
        #     cpt += 1
        #     if cpt % 100000 == 0:
        #         print(cpt)
        #     try:
        #         updated_joltage = self._apply_joltage(
        #             machine, buttons_list, starting_joltage
        #         )
        #     except ValueError:
        #         continue
        #     valid_buttons_with_combinations[buttons_list] = updated_joltage

        # print("valid_buttons_with_combinations :", len(valid_buttons_with_combinations))

        starting_joltage: list[int] = [0] * machine.nb_joltage_levels
        remaining_buttons: list[tuple[int, ...]] = machine.buttons.copy()
        remaining_presses: int = nb_presses
        remaining_requirements: list[int] = machine.joltage_requirements.copy()
        valid_buttons_with_combinations, used_buttons, nb_pushes_used = (
            self._get_valid_buttons(
                machine,
                remaining_buttons,
                remaining_requirements,
                remaining_presses,
                starting_joltage,
            )
        )

        # TODO : iterate
        # Remove already used buttons
        for button in used_buttons:
            remaining_buttons.remove(button)

        # Update remaining number of pushes
        remaining_presses -= nb_pushes_used

        for actual_buttons, actual_joltage in valid_buttons_with_combinations.items():
            valid_buttons_with_combinations, used_buttons, nb_pushes_used = (
                self._get_valid_buttons(
                    machine,
                    remaining_buttons,
                    remaining_requirements,
                    remaining_presses,
                    actual_joltage,
                )
            )

        # Now do recursively the remaining stuff
        buttons_without_combinations = list(
            combinations_with_replacement(current_buttons, remaining_presses)
        )

        print("buttons_without_combinations :", len(buttons_without_combinations))
        print(
            "Valid buttons combi total :",
            len(valid_buttons_with_combinations) * len(buttons_without_combinations),
        )

        combined_combinations = [
            buttons_with + buttons_without
            for buttons_with in valid_buttons_with_combinations.keys()
            for buttons_without in buttons_without_combinations
        ]

        return combined_combinations

    def _get_valid_buttons(
        self,
        machine: Machine,
        buttons: list[tuple[int, ...]],
        joltage_requirements: list[int],
        nb_remaining_presses: int,
        starting_joltage: list[int],
    ) -> tuple[dict[list[tuple[int, ...]], list[int]], list[tuple[int, ...]], int]:
        remaining_requirements = joltage_requirements.copy()
        minimum_value = min(remaining_requirements)
        minimum_pos = remaining_requirements.index(minimum_value)

        buttons_without_choosen: list[tuple[int, ...]] = []
        buttons_with_choosen: list[tuple[int, ...]] = []
        for button in buttons:
            if minimum_pos in button:
                buttons_with_choosen.append(button)
            else:
                buttons_without_choosen.append(button)

        nb_pushes_with_choosen_needed = minimum_value
        print("nb_pushes_with_choosen_needed", nb_pushes_with_choosen_needed)

        nb_pushes_without_choosen_needed = (
            nb_remaining_presses - nb_pushes_with_choosen_needed
        )
        print("nb_pushes_without_choosen_needed", nb_pushes_without_choosen_needed)

        buttons_with_combinations = list(
            combinations_with_replacement(
                buttons_with_choosen, nb_pushes_with_choosen_needed
            )
        )
        print("buttons_with_combinations", len(buttons_with_combinations))
        valid_buttons_with_combinations: dict[list[tuple[int, ...]], list[int]] = {}
        for buttons_list in buttons_with_combinations:
            try:
                updated_joltage = self._apply_joltage(
                    machine, buttons_list, starting_joltage
                )
            except ValueError:
                continue
            valid_buttons_with_combinations[buttons_list] = updated_joltage

        print("valid_buttons_with_combinations :", len(valid_buttons_with_combinations))

        return (
            valid_buttons_with_combinations,
            buttons_with_choosen,
            nb_pushes_with_choosen_needed,
        )

    def _apply_joltage(
        self,
        machine: Machine,
        buttons_list: Iterable[tuple[int, ...]],
        starting_joltage: list[int],
    ) -> list[int]:
        updated_joltage = starting_joltage.copy()

        for buttons in buttons_list:
            for button in buttons:
                updated_joltage[button] += 1
                if updated_joltage[button] > machine.joltage_requirements[button]:
                    raise ValueError("Joltage requirements are not met")

        return updated_joltage

    def _is_valid_voltage(
        self, machine: Machine, buttons_list: Iterable[tuple[int, ...]]
    ) -> bool:
        joltage: list[int] = [0] * machine.nb_joltage_levels

        try:
            updated_joltage = self._apply_joltage(machine, buttons_list, joltage)
        except ValueError:
            return False

        return updated_joltage == machine.joltage_requirements


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
