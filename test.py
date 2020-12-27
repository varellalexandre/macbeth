from macbeth import *
import json
import logging


def test_example_1()->None:
    """logging.basicConfig(
        format='[%(asctime)s][%(levelname)s] - %(message)s',
        level=logging.DEBUG
    )"""
    file_example_1 = open('examples/example_1.json')
    example_1 = json.load(file_example_1)
    mc1 = ProgramMC1(example_1)
    response_mc1 = mc1.calculate()
    print(response_mc1)
    mc2 = ProgramMC2(example_1)
    response_mc2 = mc2.calculate()
    print(response_mc2)


def test_example_2()->None:
    """logging.basicConfig(
        format='[%(asctime)s][%(levelname)s] - %(message)s',
        level=logging.DEBUG
    )"""
    file_example_2 = open('examples/example_2.json')
    example_2 = json.load(file_example_2)
    mc1 = ProgramMC1(example_2)
    response_mc1 = mc1.calculate()
    print(response_mc1)
    mc2 = ProgramMC2(example_2)
    response_mc2 = mc2.calculate()
    print(response_mc2)

def test_example_3()->None:
    """logging.basicConfig(
        format='[%(asctime)s][%(levelname)s] - %(message)s',
        level=logging.DEBUG
    )"""
    file_example_3 = open('examples/example_3.json')
    example_3 = json.load(file_example_3)
    mc1 = ProgramMC1(example_3)
    response_mc1 = mc1.calculate()
    print(response_mc1)
    mc2 = ProgramMC2(example_3)
    response_mc2 = mc2.calculate()
    print(response_mc2)

if __name__ == "__main__":
    test_example_1()
    test_example_2()
    test_example_3()
