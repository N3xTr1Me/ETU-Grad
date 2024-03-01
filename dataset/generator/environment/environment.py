from ..signals import ResponseQueue, Signal, SignalResponse
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

    def create_response(self, period: int, beam_id: int, t: int, aircraft: Aircraft) -> SignalResponse:

        true_dist = aircraft.true_distance(t)

        return SignalResponse(
            period,                                 # Период сигнала.
            beam_id,                                # Номер луча.
            self.get_delay(true_dist),              # Задержка до получения сигнала радаром.
            self.get_delay(true_dist % period),     # Задержка, поделенная на период сигнала.
            aircraft.get_speed(),                   # Скорость самолета.
            aircraft.get_angle(),                   # Угол, относительно радара.
            aircraft.get_first_channel_energy(),    # Энергия по первому каналу обработки.
            aircraft.get_second_channel_energy()    # Энергия по второму каналу обработки.
        )

    def send_signal(self, original: Signal, t: int) -> None:

        # Сигнал отражается только от самолетов, которые находятся в пределах определенного угла.
        for aircraft in self.__objects:

            if original.beam.in_range(aircraft.get_angle()):

                response_signal = self.create_response(
                    original.period,
                    original.beam.get_id(),
                    t,
                    aircraft
                )

                self.__responses.insert(
                    response_signal,
                    round(response_signal.true_delay)
                )

    def move_responses(self) -> None:
        # ВСЕ сигналы в очереди перемещаются в пространстве.
        self.__responses.travel()

    def get_response(self) -> List[SignalResponse]:

        return self.__responses.extract()
