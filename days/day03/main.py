from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 03 - Common Part
    ###########################

    def _get_bank_joltage(self, bank: str) -> int:
        battery_pos = 0
        bank_joltage = ""

        for i in range(1, self.nb_batteries_per_bank + 1):
            battery_pos, battery_joltage = self._get_next_battery(bank, battery_pos, i)
            bank_joltage += battery_joltage
            battery_pos += 1

        return int(bank_joltage)

    def _get_next_battery(
        self, bank: str, starting_pos: int, battery_count: int
    ) -> tuple[int, str]:
        # Ensure we properly limit the bank chunk exploration
        max_position = self.nb_batteries_per_bank - battery_count
        bank_chunk = (
            bank[starting_pos + 1 : -max_position]
            if max_position > 0
            else bank[starting_pos + 1 :]
        )

        # Init with first value of bank chunk
        battery_pos = starting_pos
        battery_joltage = bank[battery_pos]

        for pos, joltage in enumerate(bank_chunk, start=battery_pos + 1):
            if joltage > battery_joltage:
                battery_pos = pos
                battery_joltage = joltage

        return battery_pos, battery_joltage

    ###########################
    # DAY 03 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        self.nb_batteries_per_bank = 2
        return sum(self._get_bank_joltage(line) for line in self.lines)

    ###########################
    # DAY 03 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        self.nb_batteries_per_bank = 12
        return sum(self._get_bank_joltage(line) for line in self.lines)
