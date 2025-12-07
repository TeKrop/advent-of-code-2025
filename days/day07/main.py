from scripts.utils import AbstractPuzzleSolver
from enum import StrEnum


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 07 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        # Initialize beam positions with initial at first line
        beam_positions: set[int] = {self.lines[0].index("S")}
        nb_splits: int = 0

        # Explore others lines one by one
        # Considerations : no ^ at first or end position of a line, no ^^ as well
        for line in self.lines[1:]:
            new_beam_positions: set[int] = set()

            for beam_pos in beam_positions:
                match line[beam_pos]:
                    case Entity.EMPTY_SPACE:
                        new_beam_positions.add(beam_pos)
                    case Entity.SPLITTER:
                        nb_splits += 1
                        new_beam_positions.add(beam_pos + 1)
                        new_beam_positions.add(beam_pos - 1)
                    case _:
                        raise ValueError(f"Unknown entity {line[beam_pos]}")

            beam_positions = new_beam_positions

        return nb_splits

    ###########################
    # DAY 07 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        # Initialize timelines positions with initial at first line
        timelines: dict[int, int] = {pos: 0 for pos in range(len(self.lines))}
        timelines[self.lines[0].index("S")] = 1

        # Explore others lines one by one and adjust number of times
        # where we're at the given position. We'll sum them up at the end.
        # Considerations : no ^ at first or end position of a line, no ^^ as well
        for line in self.lines[1:]:
            new_timelines: dict[int, int] = timelines.copy()

            for timeline_pos, nb_times in timelines.items():
                if nb_times == 0:
                    continue

                match line[timeline_pos]:
                    case Entity.EMPTY_SPACE:
                        continue
                    case Entity.SPLITTER:
                        new_timelines[timeline_pos] -= nb_times
                        new_timelines[timeline_pos + 1] += nb_times
                        new_timelines[timeline_pos - 1] += nb_times
                    case _:
                        raise ValueError(f"Unknown entity {line[timeline_pos]}")

            timelines = new_timelines

        return sum(timelines.values())


class Entity(StrEnum):
    EMPTY_SPACE = "."
    SPLITTER = "^"
