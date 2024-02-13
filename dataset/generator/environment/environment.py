from ..signals import ResponseQueue, SignalResponse
from .aircraft import Aircraft

from typing import List


class Environment:

    """
    Окружающая среда, с которой взаимодействует радар. Определяется набором самолетов, которые движутся к радару.
    """

    class Config:

        """
        Внутренняя конфигурация окружащей среды.

        Определяет константы, которые используются в расчетах.
        """

        light_speed: int = 299792458    # Скорость света.

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, objects: List[Aircraft]) -> None:

        self.__objects = objects
        self.__responses = ResponseQueue()

    def get_delay(self, distance: int) -> float:

        return 2 * distance / self.Config.light_speed

    def create_response(self, period: int, t: int, aircraft: Aircraft) -> SignalResponse:

        true_dist = aircraft.true_distance(t)

        return SignalResponse(
            period,                                 # Период сигнала.
            self.get_delay(true_dist),              # Задержка до получения сигнала радаром.
            self.get_delay(true_dist % period),     # Задержка, поделенная на период сигнала.
            aircraft.get_speed(),                   # Скорость самолета.
            aircraft.get_angle(),                   # Угол, относительно радара.
            aircraft.get_first_channel_energy(),    # Энергия по первому каналу обработки.
            aircraft.get_second_channel_energy()    # Энергия по второму каналу обработки.
        )

    def send_signal(self, period: int, t: int) -> None:

        # Сигнал отражается от всех существующих самолетов.
        for aircraft in self.__objects:

            response_signal = self.create_response(period, t, aircraft)

            self.__responses.insert(
                response_signal,
                round(response_signal.true_delay)
            )

        # ВСЕ сигналы в очереди перемещаются в пространстве.
        self.__responses.travel()

    def get_response(self) -> List[SignalResponse]:

        return self.__responses.extract()
