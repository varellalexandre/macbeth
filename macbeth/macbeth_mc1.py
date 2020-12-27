from .macbeth_interfaces import *
from .constraints import *
import logging


class ProgramMC1Vars(Vars):
    def __init__(
        self,
        solver:pywraplp.Solver,
        set:list
    ):
        self.s0 = solver.NumVar(0,0,'s0')
        self.s1 = solver.NumVar(1,1,'s1')
        for category in range(2,6):
            var = solver.NumVar(
                -solver.infinity(),
                solver.infinity(),
                's{category}'.format(category=category)
            )
            setattr(
                self,
                's{category}'.format(category=category),
                var
            )
        self.theta = solver.NumVar(0,solver.infinity(),'theta')
        self.Cmin = solver.NumVar(0,solver.infinity(),'Cmin')
        for num,element in enumerate(set):
            var = solver.NumVar(
                0,
                solver.infinity(),
                "u(x_{})".format(num)
            )
            setattr(
                self,
                "u(x_{})".format(num),
                var
            )



class ProgramMC1Constraints(Constraint):
    def __init__(
        self,
        solver:pywraplp.Solver,
        vars:Vars,
        set:dict
    ):
        constraints = [
            Constraint_2,
            Constraint_3,
            Constraint_5
        ]
        for constraint in constraints:
            constraint(
                solver = solver,
                vars = vars,
                set = set
            )

class ProgramMC1Objective:
    def __init__(
        self,
        solver:pywraplp.Solver,
        vars:Vars,
        set:dict
    ):
        self.solver = solver
        self.objective = solver.Objective()
        self.objective.SetCoefficient(vars.Cmin,1)
        self.objective.SetMinimization()

class ProgramMC1(Problem):
    def __init__(self,set:dict):
        super(ProgramMC1,self).__init__(
            'MC1'
        )
        self.vars_object = ProgramMC1Vars
        self.objective_object = ProgramMC1Objective
        self.constraints_object = ProgramMC1Constraints
        self.set = set


    def calculate(self)->dict:
        ordered_prefs = self.set['ordered_prefs']
        vars = self.vars_object(
            self,
            ordered_prefs
        )
        constraints = self.constraints_object(
            self,
            vars,
            self.set,
        )
        objective = self.objective_object(
            self,
            vars,
            self.set,
        )
        self.Solve()
        logging.debug("Cmin")
        logging.debug(vars.Cmin.solution_value())
        return_dict = dict()
        return_dict['Cmin'] = vars.Cmin.solution_value()
        for pos,category in enumerate(ordered_prefs):
            logging.debug("{category}".format(category=category))
            return_dict["u(x_{})".format(pos)] = getattr(
                                                    vars,
                                                    "u(x_{})".format(pos)
                                                ).solution_value()
            logging.debug(
                return_dict["u(x_{})".format(pos)]
            )
        for category in range(6):
            logging.debug('s{category}'.format(category=category))
            return_dict[
                's{category}'.format(category=category)
            ] = getattr(
                vars,
                's{category}'.format(category=category)
            ).solution_value()
            logging.debug(
                return_dict['s{category}'.format(category=category)]
            )
        return return_dict
