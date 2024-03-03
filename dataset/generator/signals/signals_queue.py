from .signal_data import SignalResponse, TravelingSignal

from typing import Dict, List


class SignalQueue:

    def __init__(self) -> None:

        self.__signals: Dict[int, List[TravelingSignal]] = {}

    def push_signal(self, response: SignalResponse, beam_id: int, travel_time: int) -> None:

        addition = TravelingSignal([response], travel_time)

        # Если по лучу уже есть сигналы, то
        if beam_id in self.__signals:

            # Пройдем по ним
            for i in range(len(self.__signals[beam_id])):

                signal = self.__signals[beam_id][i]

                # Если где-то уже есть группа сигналов с таким же временем прибытия, то добавим в группу.
                if signal.arrives_in == travel_time:

                    signal.data.append(response)
                    return

                # Если мы наткнулись на группу, чье время прибытия больше текущего, то это значит, что наш сигнал придет
                # раньше нее, соответственно вставим новую группу, состоящую из нашего сигнала перед той, что встретили.
                elif signal.arrives_in > travel_time:

                    self.__signals[beam_id].insert(
                        i,
                        addition
                    )
                    return

            # Если ни одно условие в цикле не выполнилось, то это значит, что наш сигнал придет позже всех существующих.
            # Соответственно добавим его в конец очереди.
            self.__signals[beam_id].append(
                addition
            )

        else:

            # Если же по лучу нет ни одного сигнала, то создадим новую очередь.
            self.__signals[beam_id] = [
                addition
            ]

    def pop_signal(self, beam_id: int) -> List[SignalResponse]:

        # Если нет сигналов по лучу, то вернем пустой список
        if beam_id not in self.__signals:
            return []

        # Если ближайшая группа сигналов имеет время прибытия отличное от 0, то на текущей итерации ответ мы не получим.
        if self.__signals[beam_id][0].arrives_in > 0:

            for signal in self.__signals[beam_id]:
                signal.arrives_in -= 1

            return []

        return self.__signals[beam_id].pop(0).data
