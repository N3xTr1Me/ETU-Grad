from typing import Dict

from dataset.generator.environment import Environment
from dataset.generator.signals.beams import BeamFactory
from dataset.generator.signals.signal_data import SignalResponse

from dataset.generator.radar.checker import DeadZone


class Radar:

    class Config:

        Beam_count = 36
        Signal_periods = [404, 502, 642, 722]

    def __init__(self):
        self.__beams = BeamFactory.create_set(36)
        self.__periods = [404, 502, 642, 722]

    def scan(self, env: Environment, time: int) -> Dict[int, Dict[str, SignalResponse]]:

        scan_result = {}

        # Номер обзора
        survey_id = 1

        for i in range(1, time + 1):

            for j in range(len(self.__beams)):
                for period in self.__periods:

                    env.send_signal(
                        period,
                        self.__beams[j],
                        i
                    )

                # Проверка на мертвые зоны, если остаток попал, то его как бы и не было.
                responses = env.get_response(self.__beams[j])

                if len(responses) > 0:

                    if self.__beams[j].get_id() not in scan_result:
                        scan_result[self.__beams[j].get_id()] = {}

                    for response in responses:

                        # Получаем расстояние из задержки и проверяем его на попадание в мертвую зону по своему периоду.
                        if DeadZone.check(round(response.delay * 15), response.period):
                            continue

                        scan_result[self.__beams[j].get_id()][f"{survey_id},{response.beam_id},{len(responses)}"] = response
                        survey_id += 1

        return scan_result
