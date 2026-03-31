from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 11 - First Part
    ###########################
    def solve(self) -> tuple[int, int]:
        self.devices: dict[str, tuple[str, ...]] = {}

        for line in self.lines:
            device_name, outputs = line.split(":")
            self.devices[device_name] = tuple(outputs.strip().split())

        return super().solve()

    ###########################
    # DAY 11 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        self.start: str = "you"
        self.end: str = "out"

        devices, nb_out = [self.start], 0

        while len(devices) > 0:
            devices, nb_out = self._process_output_devices(devices, nb_out)

        return nb_out

    def _process_output_devices(
        self, input_devices: list[str], nb_out: int
    ) -> tuple[list[str], int]:
        output_devices: list[str] = []

        for input_device in input_devices:
            for output_device in self.devices[input_device]:
                if output_device == self.end:
                    nb_out += 1
                else:
                    output_devices.append(output_device)

        return output_devices, nb_out

    ###########################
    # DAY 11 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return 0
