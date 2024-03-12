from dataset.generator.signals import Beam, SignalResponse, SignalQueue
from .aircraft import Aircraft

from typing import List


class Environment:

    """
    Окружающая среда, с которой взаимодействует радар. Определяется набором самолетов, которые движутся к радару.
    """

    def __init__(self, objects: List[Aircraft]) -> None:

        self.__objects = objects
        self.__responses = SignalQueue()

    def _get_delay(self, distance: int) -> float:

        # А здесь уже дискреты: 1 - это 15 метров.
        return distance / 15

    def _create_response(self, period: int, beam_id: int, t: int, aircraft: Aircraft) -> SignalResponse:

        true_dist = aircraft.true_distance(t)

        return SignalResponse(
            period,                                 # Период сигнала.
            beam_id,                                # Номер луча.
            self._get_delay(true_dist),             # Задержка до получения сигнала радаром.
            self._get_delay(true_dist) % period,    # Задержка, поделенная на период сигнала.
            aircraft.get_speed(),                   # Скорость самолета.
            aircraft.get_angle(),                   # Угол, относительно радара.
            aircraft.get_first_channel_energy(),    # Энергия по первому каналу обработки.
            aircraft.get_second_channel_energy()    # Энергия по второму каналу обработки.
        )

    def send_signal(self, period: int, beam: Beam, t: int) -> None:

        # Сигнал отражается только от самолетов, которые находятся в пределах определенного угла.
        for aircraft in self.__objects:

            if beam.in_range(aircraft.get_angle()):

                response_signal = self._create_response(
                    period,
                    beam.get_id(),
                    t,
                    aircraft
                )

                self.__responses.push_signal(
                    response_signal,
                    beam.get_id(),
                    round(response_signal.true_delay / 10_000_000)  # в одной секунде 10.000.000 тактов
                )

    def get_response(self, beam: Beam) -> List[SignalResponse]:

        return self.__responses.pop_signal(beam.get_id())
