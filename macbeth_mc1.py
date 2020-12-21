from macbeth_interfaces import *
from constraints import *


class ProgramMC1Vars(Vars):
    def __init__(self,solver:pywraplp.Solver,set:list):
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
        for element in set:
            var = solver.NumVar(
                -solver.infinity(),
                solver.infinity(),
                element
            )
            setattr(
                self,
                element,
                var
            )



class ProgramMC1Constraints(Constraint):
    def __init__(
        self,
        solver:pywraplp.Solver,
        vars:Vars,
        set:pd.DataFrame
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
        set:pd.DataFrame
    ):
        self.solver = solver
        self.objective = solver.Objective()
        self.objective.SetCoefficient(vars.Cmin,1)
        self.objective.SetMinimization()

class ProgramMC1(Problem):
    def __init__(self,set:pd.DataFrame):
        super(ProgramMC1,self).__init__(
            'MC1'
        )
        self.vars_object = ProgramMC1Vars
        self.objective_object = ProgramMC1Objective
        self.constraints_object = ProgramMC1Constraints
        self.set = set


    def schematize(self):
        ordered_prefs = [row[0] for idx,row in self.set.iterrows()]
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
        print("Cmin",vars.Cmin.solution_value())
        for category in ordered_prefs:
            print("{category}".format(category=category))
            print(
                getattr(
                    vars,
                    "{category}".format(category=category)
                ).solution_value()
            )


if __name__ == '__main__':
    frame = pd.read_excel('exemplo MacBeth.xlsx')
    mc1 = ProgramMC1(frame)
    mc1.schematize()
