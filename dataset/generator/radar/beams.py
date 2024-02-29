from typing import List


class Beam:

    def __init__(self, direction_angle: float, delta: float = 1.5) -> None:

        self.__lower_range = direction_angle - delta
        self.__upper_range = direction_angle + delta

    def in_range(self, angle: float) -> bool:

        if self.__lower_range <= angle <= self.__upper_range:

            return True

        return False


class BeamFactory:

    @staticmethod
    def create_set(n: int = 36) -> List[Beam]:

        beams = []

        for direction in range(n):

            beams.append(
                Beam(direction)
            )

        return beams
