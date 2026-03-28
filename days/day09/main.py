from collections import namedtuple
from dataclasses import dataclass
from functools import cached_property
from itertools import combinations
from typing import Any

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 09 - Common Part
    ###########################
    def solve(self) -> tuple[int, int]:
        self.red_tiles: list[Position] = []
        for line in self.lines:
            pos_x, pos_y = line.split(",")
            self.red_tiles.append(Position(int(pos_x), int(pos_y)))

        self.rectangles: list[Rectangle] = [
            Rectangle(red_tile_pair)
            for red_tile_pair in combinations(self.red_tiles, 2)
        ]
        self.rectangles.sort(reverse=True)

        return super().solve()

    ###########################
    # DAY 09 - First Part
    ###########################
    def _solve_first_part(self) -> int:
        return next(iter(self.rectangles)).area

    ###########################
    # DAY 09 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return 0


Position = namedtuple("Position", ["x", "y"])


@dataclass
class Rectangle:
    """Rectangle representation class for the challenge.

    We're keeping track of the red tile pair, but also defining a few things :
    - Reusable metrics : width and height of the rectangle, min and max positions
    - Comparison with others rectangles using the area
    """

    red_tile_pair: tuple[Position, Position]

    @cached_property
    def min(self) -> Position:
        return Position(
            min(self.red_tile_pair[0].x, self.red_tile_pair[1].x),
            min(self.red_tile_pair[0].y, self.red_tile_pair[1].y),
        )

    @cached_property
    def max(self) -> Position:
        return Position(
            max(self.red_tile_pair[0].x, self.red_tile_pair[1].x),
            max(self.red_tile_pair[0].y, self.red_tile_pair[1].y),
        )

    @cached_property
    def width(self) -> int:
        return self.max.x - self.min.x + 1

    @cached_property
    def height(self) -> int:
        return self.max.y - self.min.y + 1

    @cached_property
    def area(self) -> int:
        return self.width * self.height

    def __lt__(self, other: "Rectangle") -> bool:
        return self.area < other.area

    def __eq__(self, other: Any) -> bool:
        return self.area == other.area

    def __repr__(self) -> str:
        return (
            "Rectangle("
            f"area={self.area}, "
            f"width={self.width}, "
            f"height={self.height}, "
            f"pair={self.red_tile_pair}"
            ")"
        )
