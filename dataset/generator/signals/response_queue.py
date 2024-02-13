from .signal_response import SignalResponse

from dataclasses import dataclass
from typing import List


@dataclass
class SignalNode:

    """
    Внутренний класс для работы очереди ответных сигналов.
    """

    data: List[SignalResponse]
    response_time: int


class ResponseQueue:

    """
    Модифицированная очередь с приоритетом, эмулирующий процесс перемещения сигнала в пространстве.
    Нужен для определения порядка получения ответных сигналов радаром.

    Каждому ответному сигналу присваивает приоритет - время в итерациях (длинной в секунуду),
    через которое радар получит ответ.

    При каждом запросе 'extract()' очередь может вернуть, либо пустой список, либо набор ответных сигналов.
    """

    def __init__(self) -> None:

        self.__queue: List[SignalNode] = []

    def insert(self, signal: SignalResponse, time: int) -> None:

        """
        Добавление ответного сигнала, который должнен быть получен радаром в определенный момент времени.

        Если время получения сигнала радаром совпадает с каким-либо набором, уже находящимся в очереди,
        то добавляемый сигнал присоединяется к этому набору.

        :param signal:  ответный сигнал.
        :param time:    время, через которое сигнал будет получен радаром.
        :return:        None.
        """

        for element in self.__queue:

            if element.response_time == time:

                element.data.append(signal)
                return

        self.__queue.append(
            SignalNode([signal], time)
        )

        self.__queue.sort(
            key=lambda element: element.response_time,
            reverse=True
        )

    def extract(self) -> List[SignalResponse]:

        """
        Получение набора ответных сигналов из очереди.

        Если очередь пуста или в ней нет набора с временем прибытия меньше или ранвным 1, то возвращается пустой список.

        :return: набор объектов класса SignalResponse.
        """

        if not self.__queue:

            return []

        if self.__queue[-1].response_time <= 1:

            return self.__queue.pop().data

        return []

    def travel(self) -> None:

        """
        Эмуляция путешествия сигналов в пространстве.

        Каждый вызов уменьшает время, через которое каждая группа сигналов будет получена радаром на 1.

        :return: None.
        """

        for element in self.__queue:

            element.response_time -= 1
