from macbeth_interfaces import *


class Program_MC1_Vars:
    def __init__(self,solver:pywraplp.Solver):
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

class Program_MC1_Constraints:
    def __init__(
        self,
        solver:pywraplp.Solver,
        vars:Program_MC1_Vars,
        set:pd.DataFrame
    ):
        ordered_prefs = [row[0] for idx,row in set.iterrows()]
        for x,name_x in enumerate(ordered_prefs):
            next = x+1
            for y,name_y in enumerate(ordered_prefs[next:]):
                print(name_x,name_y,set[name_y][x])

class Program_MC1:

    def __init__(self,set:pd.DataFrame):
        self.solver = pywraplp.Solver(
            'MC1',
            pywraplp.Solver.GLOP_LINEAR_PROGRAMMING
        )
        self.vars_object = Program_MC1_Vars
        self.objective_object = ObjectiveInterface
        self.constraints_object = Program_MC1_Constraints
        self.set = set


    def schematize(self):
        vars = self.vars_object(self.solver)
        constraints = self.constraints_object(
            self.solver,
            vars,
            self.set,
        )


class Macbeth:
    def __init__(self):
        pass

if __name__ == '__main__':
    frame = pd.read_excel('exemplo MacBeth.xlsx')
    mc1 = Program_MC1(frame)
    mc1.schematize()
