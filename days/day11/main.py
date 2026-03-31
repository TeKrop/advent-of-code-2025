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

        devices = [self.start]
        while not all(device == self.end for device in devices):
            devices = self._get_output_devices(devices)

        return len(devices)

    def _get_output_devices(self, input_devices: list[str]) -> list[str]:
        output_devices: list[str] = []

        for device in input_devices:
            if device == self.end:
                output_devices.append(self.end)
                continue
            output_devices.extend(self.devices[device])

        return output_devices

    ###########################
    # DAY 11 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return 0
