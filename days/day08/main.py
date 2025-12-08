from scripts.utils import AbstractPuzzleSolver, DataType, min_and_max
from math import prod, dist
from itertools import combinations
from collections import namedtuple


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 08 - Common Part
    ###########################
    def solve(self) -> tuple[int, int]:
        self.sorted_pairs = self._compute_junction_boxes_pairs()
        return super().solve()

    def _compute_junction_boxes_pairs(
        self,
    ) -> dict[tuple[JunctionBox, JunctionBox], int]:
        """Return sorted boxes combinations ordered by distance ascendant"""
        junction_boxes = {
            JunctionBox(*(int(coord) for coord in line.split(",")))
            for line in self.lines
        }

        possible_pairs = {
            junction_boxes: dist(junction_boxes[0], junction_boxes[1])
            for junction_boxes in combinations(junction_boxes, 2)
        }

        return dict(sorted(possible_pairs.items(), key=lambda item: item[1]))

    def _update_circuits(
        self,
        circuits: list[set[JunctionBox]],
        pair: tuple[JunctionBox, JunctionBox],
    ) -> None:
        # Check the items locations if they exist in the circuit
        found = [-1, -1]
        for i, circuit in enumerate(circuits):
            if pair[0] in circuit:
                found[0] = i

            if pair[1] in circuit:
                found[1] = i

        # If connection is already made within one circuit, nothing to do
        if found[0] == found[1] and found[0] != -1:
            return

        # No item is any of the circuits, create new one with the pair
        if found == [-1, -1]:
            circuits.append(set(pair))
            return

        # Now we know at least one of the items has been found
        if found[0] == -1:
            # First not found, it means the second has been found
            circuits[found[1]].add(pair[0])
        elif found[1] == -1:
            # Second not found, it means the first has been found
            circuits[found[0]].add(pair[1])
        else:
            # First and second found in different circuits, merge the circuits
            merged_circuit = circuits[found[0]] | circuits[found[1]]

            # Ensure to remove the upper value first, else reindexation
            # will occur and second value will be incorrect
            min_value, max_value = min_and_max(found[0], found[1])
            del circuits[max_value]
            del circuits[min_value]
            circuits.append(merged_circuit)

    ###########################
    # DAY 08 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        self.pairs_to_connect = 10 if self.data_type == DataType.EXAMPLE else 1000

        circuits: list[set[JunctionBox]] = []

        for i_pair, pair in enumerate(self.sorted_pairs.keys()):
            # Stop when we went over enough pairs to connect
            if i_pair == self.pairs_to_connect:
                break

            self._update_circuits(circuits, pair)

        # Find 3 top circuits length
        circuits_length = sorted([len(circuit) for circuit in circuits], reverse=True)

        return prod(circuits_length[0:3])

    ###########################
    # DAY 08 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        circuits: list[set[JunctionBox]] = []
        nb_boxes = len(self.lines)

        last_pair: tuple[JunctionBox, JunctionBox] | None = None
        for pair in self.sorted_pairs.keys():
            # Stop when we have one circuit containing all the boxes
            if len(circuits) == 1 and len(circuits[0]) == nb_boxes:
                break

            # Ensure we keep track of the pair allowing the full circuit
            last_pair = pair

            # Update circuits with the new pair
            self._update_circuits(circuits, pair)

        return last_pair[0].x * last_pair[1].x


JunctionBox = namedtuple("JunctionBox", ["x", "y", "z"])
