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

class ORInterface:
    def formula(self):
        raise Exception('Function Not implemented!')

class ConstraintInterface(ORInterface):
    def __init__(self,solver:pywraplp.Solver,bound:tuple):
        self.restriction = solver.Constraint(*bound)

    def formula(self):
        return self.restriction

class ObjectiveInterface(ORInterface):
    def __init__(self,solver:pywraplp.Solver):
        self.objective = solver.Objective()

    def formula(self):
        return self.objective
