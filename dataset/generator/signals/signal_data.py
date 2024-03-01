from dataset.generator.radar.beams import Beam

from dataclasses import dataclass


@dataclass(init=True)
class Signal:

    beam: Beam
    period: int


@dataclass(init=True)
class SignalResponse:

    """
    Ответный сигнал, отраженный от самолета.
    """

    # Основные характеристики
    period: int         # Период исходного сигнала.
    beam_id: int        # Номер луча.

    true_delay: float   # Просто задержка до получения ответного сигнала.
    delay: float        # Задержка до получения ответного сигнала, поделенная на период этого сигнала.

    # Дополнительные характеристики
    speed: int          # (Радиальная) скорость, с которой движется объект отражения.
    angle: float        # Угол, относительно положения радара.

    u_first: float      # Энергия сигнала в первом канале.
    u_second: float     # Энергия сигнала во втором канале.
