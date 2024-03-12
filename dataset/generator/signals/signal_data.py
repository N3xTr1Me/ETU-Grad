from dataclasses import dataclass

from typing import List


@dataclass(init=True)
class SignalResponse:

    """
    Ответный сигнал, отраженный от самолета.
    """

    # Основные характеристики
    period: int         # Период исходного сигнала.
    beam_id: int        # Номер луча.

    delay: float        # Задержка до получения ответного сигнала, поделенная на период этого сигнала.

    # Дополнительные характеристики
    speed: int          # (Радиальная) скорость, с которой движется объект отражения.
    angle: float        # Угол, относительно положения радара.

    u_first: float      # Энергия сигнала в первом канале.
    u_second: float     # Энергия сигнала во втором канале.
    true_delay: float   # Просто задержка до получения ответного сигнала.


@dataclass(init=True)
class TravelingSignal:
    data: List[SignalResponse]
    arrives_in: int
