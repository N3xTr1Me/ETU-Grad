from signals import SignalResponse

from typing import Dict, List

from csv import writer, reader
from datetime import datetime
from pathlib import Path



class TestConfig:

    test_folder = "./test-cases/"
    test_subjects = [
        {"distance": 45000, "speed": 29, "angle": 15, "u1": 180, "u2": 120}
    ]
    header = [
        "обзор",
        "луч",
        "N целей",
        "период",
        "луч",
        "дальность",
        "скорость",
        "угол",
        "энергия 1",
        "энергия 2",
        "Истинная задержка"
    ]


def _prepare_data(key: str, value: SignalResponse) -> List[int | float]:

    result = list(map(int, key.split(",")))

    for prop in value.__dict__.values():

        result.append(prop)

    return result


def write_test(beam_id: int, test_data: Dict[str, SignalResponse]) -> None:

    file = Path(
        TestConfig.test_folder + datetime.now().strftime("%d_%m_%Y - %H-%M-%S/")
    )

    file.mkdir(parents=True, exist_ok=True)

    file = file / f"beam_{beam_id}.csv"

    with file.open("w", newline='') as testfile:

        encoder = writer(testfile)

        # заголовок
        encoder.writerow(TestConfig.header)

        # Сами сигналы
        for case in test_data:

            encoder.writerow(_prepare_data(case, test_data[case]))


def read_test(generation: str, beam_id: int) -> List[List[str]]:

    file = Path(
        TestConfig.test_folder + generation + "/" + f"beam_{beam_id}.csv"
    )

    if not file.exists():

        raise FileNotFoundError(f"{file.absolute()} - not found!")

    with file.open("r") as src:

        decoder = reader(src, delimiter=",")

        result = list(decoder)

    result.pop(0)

    return result
