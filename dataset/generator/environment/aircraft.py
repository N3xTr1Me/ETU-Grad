from dataclasses import dataclass
from typing import Tuple


@dataclass(init=True, repr=True)
class Aircraft:

    """
    Объекты класса симулируют самолеты, приближающиеся к радару, начиная с определенной позиции.

    Предполагается, что система полностью детерменирована и расстояние самолета до радара зависит строго
    от момента времени, а все прочие характеристики не изменяются.
    """

    __start_distance: int               # Начальное расстояние от самолета до радара.
    __movement_speed: int               # ПОСТОЯННАЯ скорость движения самолета.
    __angle: float                      # Угол, относительно положения радара.
    __amplitude: Tuple[float, float]    # Энергия в двух каналах обработки.

    # ------------------------------------------------------------------------------------------------------------------

    def get_speed(self) -> int:

        return self.__movement_speed

    def get_angle(self) -> float:

        return self.__angle

    def get_first_channel_energy(self) -> float:

        return self.__amplitude[0]

    def get_second_channel_energy(self) -> float:

        return self.__amplitude[1]

    # ------------------------------------------------------------------------------------------------------------------

    def true_distance(self, time_moment: int) -> int:

        """
        Истинное расстояние расчитывается вычитанием из начального расстояния произведения скорости объекта на момент
        времени, которое прошло с начала движения.

        Иными словами, предполаагается, что самолет за каждую секунду времени
        приближается к радару на одинаковое расстояние.

        :param time_moment: момент времени в секундах, с начала движения.
        :return:            текущее расстояние от самолета до радара.
        """

        return self.__start_distance - time_moment * self.__movement_speed
