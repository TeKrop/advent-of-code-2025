from scripts.utils import AbstractPuzzleSolver
from functools import cache
from typing import Callable


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 02 - Common Part
    ###########################

    def _solve(self, invalid_check_method: Callable) -> int:
        return sum(
            self._get_invalid_ids_sum(
                product_id_range, invalid_check_method=invalid_check_method
            )
            for product_id_range in self.line.split(",")
        )

    def _get_invalid_ids_sum(
        self, product_id_range: str, invalid_check_method: Callable
    ) -> int:
        first, second = product_id_range.split("-")
        first_product_id, second_product_id = int(first), int(second)

        return sum(
            product_id
            for product_id in range(first_product_id, second_product_id + 1)
            if invalid_check_method(product_id)
        )

    @cache
    def _get_nb_digits(self, number: int) -> int:
        if number == 0:
            return 1

        count = 0
        while number > 0:
            count += 1
            number //= 10

        return count

    def _has_repeating_pattern(self, number: int, nb_pattern: int) -> bool:
        nb_digits = self._get_nb_digits(number)
        pattern = number // 10 ** (nb_digits - nb_pattern)

        delta = number

        for i in range(nb_digits - nb_pattern, -1, -nb_pattern):
            delta -= pattern * 10**i

        return delta == 0

    ###########################
    # DAY 02 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return self._solve(invalid_check_method=self._has_sequence_repeated_twice)

    def _has_sequence_repeated_twice(self, product_id: int) -> bool:
        is_invalid = False

        nb_digits = self._get_nb_digits(product_id)
        if nb_digits % 2 == 1:
            return is_invalid

        nb_pattern = nb_digits // 2
        if self._has_repeating_pattern(product_id, nb_pattern):
            is_invalid = True

        return is_invalid

    ###########################
    # DAY 02 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return self._solve(
            invalid_check_method=self._has_sequence_repeated_at_least_twice
        )

    def _has_sequence_repeated_at_least_twice(self, product_id: int) -> bool:
        nb_digits = self._get_nb_digits(product_id)

        # We can't have more than half the digits for a pattern
        nb_max_pattern = nb_digits // 2

        is_invalid = False

        for nb_pattern in range(1, nb_max_pattern + 1):
            # Ignore pattern length if number of digits is not divisible by it
            if nb_digits % nb_pattern != 0:
                continue

            # As soon as a repeating pattern is detected, stop right there
            if self._has_repeating_pattern(product_id, nb_pattern):
                is_invalid = True
                break

        return is_invalid
