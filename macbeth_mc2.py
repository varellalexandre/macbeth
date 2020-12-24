from macbeth_interfaces import *
from constraints import *

class ProgramMC2Vars(Vars):
    def __init__(
        self,
        solver:pywraplp.Solver,
        ordered_prefs:list,
        set:pd.DataFrame,
        Cmin:int=0
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
        self.Cmin = solver.NumVar(0,Cmin,'Cmin')
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

        for x,name_x in enumerate(ordered_prefs):
            next = x+1
            for y,name_y in enumerate(ordered_prefs[next:]):
                value = set[name_y][x]
                vars = [
                    'ep',
                    'n',
                    'alfa',
                    'gama',
                    'beta',
                    'mi'
                ]
                for var in vars:
                    setattr(
                        self,
                        "{var}(x{x}_x{y})".format(
                            var=var,
                            x=x,
                            y=(y+next)
                        ),
                        solver.NumVar(
                            0,
                            solver.infinity(),
                            "{var}(x{x}_x{y})".format(
                                var=var,
                                x=x,
                                y=(y+next)
                            )
                        )
                    )

class ProgramMC2Objective:
    def __init__(
        self,
        solver:pywraplp.Solver,
        vars:Vars,
        set:pd.DataFrame
    ):
        self.solver = solver
        self.objective = solver.Objective()
        ordered_prefs = [row[0] for idx,row in set.iterrows()]
        for x,name_x in enumerate(ordered_prefs):
            next = x+1
            for y,name_y in enumerate(ordered_prefs[next:]):
                value = set[name_y][x]
                if value < 6:
                    self.objective.SetCoefficient(
                        getattr(
                            vars,
                            "ep(x{x}_x{y})".format(
                                x=x,
                                y=(y+next)
                            )
                        ),
                        1
                    )
                    self.objective.SetCoefficient(
                        getattr(
                            vars,
                            "n(x{x}_x{y})".format(
                                x=x,
                                y=(y+next)
                            )
                        ),
                        1
                    )
                else:
                    self.objective.SetCoefficient(
                        getattr(
                            vars,
                            "alfa(x{x}_x{y})".format(
                                x=x,
                                y=(y+next)
                            )
                        ),
                        1
                    )
        self.objective.SetMinimization()

class ProgramMC2Constraints(Constraint):
    def __init__(
        self,
        solver:pywraplp.Solver,
        vars:Vars,
        set:pd.DataFrame
    ):
        constraints = [
            Constraint_2,
            Constraint_3,
            Constraint_5,
            Constraint_7,
            Constraint_8,
            Constraint_9
        ]
        for constraint in constraints:
            constraint(
                solver = solver,
                vars = vars,
                set = set
            )

class ProgramMC2(Problem):
    def __init__(self,set:pd.DataFrame):
        super(ProgramMC2,self).__init__(
            'MC2'
        )
        self.vars_object = ProgramMC2Vars
        self.objective_object = ProgramMC2Objective
        self.constraints_object = ProgramMC2Constraints
        self.set = set

    def schematize(self):
        ordered_prefs = [row[0] for idx,row in self.set.iterrows()]
        vars = self.vars_object(
            self,
            ordered_prefs,
            self.set
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
        logging.debug("Cmin",vars.Cmin.solution_value())
        for pos,category in enumerate(ordered_prefs):
            logging.debug("{category}".format(category=category))
            logging.debug(
                getattr(
                    vars,
                    "u(x_{})".format(pos)
                ).solution_value()
            )
        for category in range(6):
            logging.debug('s{category}'.format(category=category))
            logging.debug(
                getattr(
                    vars,
                    's{category}'.format(category=category)
                ).solution_value()
            )

if __name__ == '__main__':
    frame = pd.read_excel('exemplo MacBeth.xlsx')
    mc2 = ProgramMC2(frame)
    mc2.schematize()
