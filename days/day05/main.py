from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 05 - Common Part
    ###########################
    def solve(self) -> tuple[int, int]:
        self._compute_puzzle_input()
        return super().solve()

    def _compute_puzzle_input(self) -> None:
        self.fresh_id_ranges: list[tuple[int, int]] = []
        self.available_ingredient_ids: set[int] = set()

        # Input : list of fresh ID ranges, one blank line, list of ingredient IDs
        is_ingredient_id = False
        for line in self.lines:
            if not line:
                is_ingredient_id = True
                continue

            if is_ingredient_id:
                self.available_ingredient_ids.add(int(line))
            else:
                range_min, range_max = line.split("-")
                self.fresh_id_ranges.append((int(range_min), int(range_max)))

    ###########################
    # DAY 05 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return sum(
            1
            for ingredient_id in self.available_ingredient_ids
            if self._is_ingredient_fresh(ingredient_id)
        )

    def _is_ingredient_fresh(self, ingredient_id: int) -> bool:
        return any(
            fresh_id_min <= ingredient_id <= fresh_id_max
            for fresh_id_min, fresh_id_max in self.fresh_id_ranges
        )

    ###########################
    # DAY 05 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        # Compute ranges overlaps to ensure numbers can't be counted twice
        while self._compute_ranges_overlaps():
            pass

        return sum(
            (fresh_id_max - fresh_id_min) + 1
            for fresh_id_min, fresh_id_max in self.fresh_id_ranges
        )

    def _compute_ranges_overlaps(self) -> bool:
        """Compute ranges for overlaps. Returns true if at least one overlap has been found"""

        had_at_least_one_overlap = False
        new_ranges: list[tuple[int, int]] = []

        for fresh_id_range in self.fresh_id_ranges:
            is_overlapping = False

            # If there is an overlap, merge the ranges together
            for i, new_range in enumerate(new_ranges):
                if not self._are_ranges_overlapping(fresh_id_range, new_range):
                    continue

                new_ranges[i] = self._compute_merged_range(fresh_id_range, new_range)
                is_overlapping = True
                had_at_least_one_overlap = True
                break

            # No overlap at all -> just add it to the list
            if not is_overlapping:
                new_ranges.append(fresh_id_range)

        self.fresh_id_ranges = new_ranges
        return had_at_least_one_overlap

    def _are_ranges_overlapping(
        self, first_range: tuple[int, int], second_range: tuple[int, int]
    ) -> bool:
        return (
            first_range[1] >= second_range[0] and first_range[0] <= second_range[1]
        ) or (second_range[1] >= first_range[0] and second_range[0] <= first_range[1])

    def _compute_merged_range(
        self, first_range: tuple[int, int], second_range: tuple[int, int]
    ) -> tuple[int, int]:
        return (
            min(first_range[0], second_range[0]),
            max(first_range[1], second_range[1]),
        )
