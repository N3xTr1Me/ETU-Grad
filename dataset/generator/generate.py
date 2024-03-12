from radar import Radar
from environment import Environment, Aircraft
from dataset.generator.test_generation import write_test, read_test


def main():

    scaner = Radar()
    environment = Environment([Aircraft(59000, 28, 2, (99, 88))])

    results = scaner.scan(environment, 6)

    for res in results:

        write_test(res, results[res])

    # test = read_test("12_03_2024 - 17-00-19", 2)

    print()


if __name__ == "__main__":
    main()
