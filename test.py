from macbeth import *
import json
import logging

def test_mc(filename:str)->None:
    logging.basicConfig(
    format='[%(asctime)s][%(levelname)s] - %(message)s',
    level=logging.DEBUG
    )
    file_example = open('examples/{filename}'.format(filename=filename))
    example = json.load(file_example)
    mc1 = ProgramMC1(example)
    response_mc1 = mc1.calculate()
    print(response_mc1)
    mc2 = ProgramMC2(example)
    response_mc2 = mc2.calculate()
    print(response_mc2)

def test_example_1()->None:
    test_mc('example_1.json')


def test_example_2()->None:
    test_mc('example_2.json')

def test_lpmacbeth()->None:
    logging.basicConfig(
        format='[%(asctime)s][%(levelname)s] - %(message)s',
        level=logging.DEBUG
    )
    file_example_2 = open('examples/example_4.json')
    example_2 = json.load(file_example_2)
    lp = LPMacbeth(example_2)
    response = lp.calculate()
    print(response)


def test_example_3()->None:
    test_mc('example_3.json')

def test_example_4()->None:
    test_mc('example_4.json')

if __name__ == "__main__":
    test_lpmacbeth()
    #test_example_1()
    #test_example_2()
    #test_example_3()
    #test_example_4()
