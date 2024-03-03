from typing import List


class Beam:

    def __init__(self, number: int, direction_angle: float, delta: float = 1.5) -> None:

        self.__id = number

        self.__lower_range = direction_angle - delta
        self.__upper_range = direction_angle + delta

    def in_range(self, angle: float) -> bool:

        if self.__lower_range <= angle <= self.__upper_range:

            return True

        return False

    def get_id(self) -> int:

        return self.__id


class BeamFactory:

    @staticmethod
    def create_set(n: int = 36) -> List[Beam]:

        beams = []

        for direction in range(n):

            # В данном случае нумерация лучей совпадает с их центральным угловым направлением (бисектриса угла).
            beams.append(
                Beam(direction, direction)
            )

        return beams
