from scripts.utils import AbstractPuzzleSolver
from itertools import combinations
from collections import namedtuple
from functools import cache
from rich import print


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 09 - Common Part
    ###########################
    def solve(self) -> tuple[int, int]:
        self.red_tiles: list[Position] = [
            Position(*(int(coord) for coord in line.split(","))) for line in self.lines
        ]
        return super().solve()

    @cache
    def _get_rectangle_area(self, red_tile_pair: tuple[Position, Position]) -> int:
        width = abs(red_tile_pair[0].x - red_tile_pair[1].x)
        height = abs(red_tile_pair[0].y - red_tile_pair[1].y)
        return (width + 1) * (height + 1)

    ###########################
    # DAY 09 - First Part
    ###########################
    def _solve_first_part(self) -> int:
        return max(
            self._get_rectangle_area(red_tile_pair)
            for red_tile_pair in combinations(self.red_tiles, 2)
        )

    ###########################
    # DAY 09 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        self._compute_grid()
        return max(
            self._get_rectangle_area(red_tile_pair)
            for red_tile_pair in combinations(self.red_tiles, 2)
            if self._is_valid_rectangle(red_tile_pair)
        )

    def _compute_grid(self) -> None:
        # Loop over to assign green tiles
        self.green_and_red_tiles = set()
        for i in range(-1, len(self.red_tiles) - 1):
            current_tile = self.red_tiles[i]
            next_tile = self.red_tiles[i + 1]
            # print(red_tile)
            # print(next_tile)
            # print("---")
            self.green_and_red_tiles |= {
                Position(x, y)
                for x in (
                    range(
                        current_tile.x,
                        next_tile.x,
                        int(
                            (next_tile.x - current_tile.x)
                            / abs(next_tile.x - current_tile.x)
                        ),
                    )
                    if next_tile.x != current_tile.x
                    else [current_tile.x]
                )
                for y in (
                    range(
                        current_tile.y,
                        next_tile.y,
                        int(
                            (next_tile.y - current_tile.y)
                            / abs(next_tile.y - current_tile.y)
                        ),
                    )
                    if next_tile.y != current_tile.y
                    else [current_tile.y]
                )
            }

        print(len(self.green_and_red_tiles))
        # print(self.green_and_red_tiles)

        min_x = min(red_tile.x for red_tile in self.red_tiles)
        max_x = max(red_tile.x for red_tile in self.red_tiles)
        min_y = min(red_tile.y for red_tile in self.red_tiles)
        max_y = max(red_tile.y for red_tile in self.red_tiles)

        print(min_x, max_x)
        print(min_y, max_y)
        # Compute green positions

    def _is_valid_rectangle(self, pair: tuple[Position, Position]) -> bool:
        # Check every coordinates
        return True


Position = namedtuple("Position", ["x", "y"])
