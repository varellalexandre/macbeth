from ortools.linear_solver import pywraplp
from enum import Enum
import pandas as pd

class Categories(Enum):
    NONE=0
    NEGLIGIBLE_OR_VERY_WEAK=1
    WEAK=2
    MODERATE=3
    STRONG=4
    VERY_STRONG=5
    EXTREME=6

class Problem(pywraplp.Solver):
    def __init__(
        self,
        name,
        solver_type=pywraplp.Solver.GLOP_LINEAR_PROGRAMMING
    ):
        super(Problem,self).__init__(
            name,
            solver_type
        )

    def schematize(self,**kwargs):
        raise Exception('Schematize not implemented')

class Vars:
    def __init__(self,**kwargs):
        raise Exception('Vars constructor not implemented')


class Constraint:
    def __init__(self,vars:Vars,set:pd.DataFrame,**kwargs):
        raise Exception('Constraint constructor not implemented')
