from macbeth_interfaces import *
from constraints import *

class ProgramMC4Vars(Vars):
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
